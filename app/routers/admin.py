import hmac
import re
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Form, Query, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.constants import DISCIPLINES
from app.db import get_db
from app.deps import ADMIN_PREVIEW_COOKIE, has_admin_preview
from app.i18n.strings import DEFAULT_LANG, get_strings
from app.mail import send_email
from app.models import Kata, User, Waitlist
from app.render import render
from app.security import create_reset_token
from app.stats import practice_stats, streak_info, total_practice_days

router = APIRouter()

# youtube watch / youtu.be / shorts / embed → embed formatına çevir
YOUTUBE_RE = re.compile(
    r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)([\w-]{11})"
)


def _token_ok(token: str) -> bool:
    return hmac.compare_digest(token, settings.admin_token)


def normalize_video_url(url: str) -> str | None:
    url = url.strip()
    if not url:
        return None
    m = YOUTUBE_RE.search(url)
    if m:
        return f"https://www.youtube.com/embed/{m.group(1)}"
    if url.startswith("https://"):
        return url[:500]
    return None


@router.get("/admin", response_class=HTMLResponse)
async def admin_index(
    request: Request,
    token: str = Query(default=""),
    mail_sent: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    waitlist_count = (await db.execute(select(Waitlist))).scalars().all()
    health = {
        "env": settings.env,
        "waitlist_only": settings.waitlist_only,
        "pro_enabled": settings.pro_enabled,
        "resend_configured": bool(settings.resend_api_key),
        "vapid_configured": bool(settings.vapid_private_key and settings.vapid_public_key),
        "sentry_configured": bool(settings.sentry_dsn),
        "lemon_squeezy_configured": bool(settings.ls_webhook_secret),
        "base_url": settings.base_url,
    }
    return render(
        request,
        "admin_index.html",
        token=token,
        health=health,
        waitlist_count=len(waitlist_count),
        mail_sent=mail_sent,
        preview_active=has_admin_preview(request),
    )


@router.get("/admin/preview")
async def admin_preview_on(token: str = Query(default=""), next: str = Query(default="/app")):
    """WAITLIST_ONLY=true iken sahibin app'i canlıda görebilmesi için çerez set eder."""
    if not _token_ok(token):
        return Response(status_code=404)
    if not next.startswith("/") or next.startswith("//"):
        next = "/app"
    response = RedirectResponse(next, status_code=303)
    response.set_cookie(
        ADMIN_PREVIEW_COOKIE,
        settings.admin_token,
        max_age=60 * 60 * 24 * 30,
        httponly=True,
        samesite="lax",
        secure=settings.env == "production",
    )
    return response


@router.get("/admin/preview/off")
async def admin_preview_off(token: str = Query(default="")):
    if not _token_ok(token):
        return Response(status_code=404)
    response = RedirectResponse(f"/admin?token={token}", status_code=303)
    response.delete_cookie(ADMIN_PREVIEW_COOKIE)
    return response


@router.post("/admin/test-email")
async def admin_test_email(
    token: str = Form(...),
    to: str = Form(...),
):
    if not _token_ok(token):
        return Response(status_code=404)
    await send_email(
        to=to,
        subject="Joryu — test e-postası",
        html="<p>Bu, admin panelinden gönderilen bir test e-postasıdır. Ulaştıysa e-posta gönderimi çalışıyor demektir.</p>",
    )
    status = "configured" if settings.resend_api_key else "unconfigured"
    return RedirectResponse(f"/admin?token={token}&mail_sent={status}", status_code=303)


@router.get("/admin/waitlist/view", response_class=HTMLResponse)
async def admin_waitlist_view(
    request: Request,
    token: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    result = await db.execute(select(Waitlist).order_by(Waitlist.created_at.desc()))
    rows = result.scalars().all()
    return render(request, "admin_waitlist.html", token=token, rows=rows)


@router.get("/admin/docs", response_class=HTMLResponse)
async def admin_docs(request: Request, token: str = Query(default="")):
    if not _token_ok(token):
        return Response(status_code=404)
    routes = []
    for r in request.app.routes:
        path = getattr(r, "path", None)
        methods = getattr(r, "methods", None)
        if not path or not methods or path.startswith("/static"):
            continue
        endpoint = getattr(r, "endpoint", None)
        doc = (endpoint.__doc__ or "").strip().splitlines()[0] if endpoint and endpoint.__doc__ else ""
        routes.append({"path": path, "methods": sorted(methods - {"HEAD", "OPTIONS"}), "doc": doc})
    routes.sort(key=lambda r: r["path"])
    return render(request, "admin_docs.html", token=token, routes=routes)


USERS_PAGE_SIZE = 30


@router.get("/admin/users", response_class=HTMLResponse)
async def admin_users(
    request: Request,
    token: str = Query(default=""),
    q: str = Query(default=""),
    page: int = Query(default=1, ge=1),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    stmt = select(User).order_by(User.created_at.desc())
    count_stmt = select(func.count(User.id))
    q = q.strip()
    if q:
        pattern = f"%{q}%"
        cond = or_(User.email.ilike(pattern), User.username.ilike(pattern))
        stmt = stmt.where(cond)
        count_stmt = count_stmt.where(cond)
    total = (await db.execute(count_stmt)).scalar_one()
    stmt = stmt.offset((page - 1) * USERS_PAGE_SIZE).limit(USERS_PAGE_SIZE)
    users = (await db.execute(stmt)).scalars().all()
    return render(
        request,
        "admin_users.html",
        token=token,
        users=users,
        q=q,
        page=page,
        total=total,
        page_size=USERS_PAGE_SIZE,
        total_pages=max(1, -(-total // USERS_PAGE_SIZE)),
    )


@router.get("/admin/users/{user_id}", response_class=HTMLResponse)
async def admin_user_detail(
    user_id: uuid.UUID,
    request: Request,
    token: str = Query(default=""),
    saved: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        return Response(status_code=404)
    stats = await practice_stats(db, user.id)
    days = await total_practice_days(db, user.id)
    streak = await streak_info(db, user.id)
    return render(
        request,
        "admin_user_detail.html",
        token=token,
        user_row=user,
        disciplines=DISCIPLINES,
        stats=stats,
        practice_days=days,
        streak=streak["streak"],
        saved=saved,
    )


@router.post("/admin/users/{user_id}")
async def admin_user_update(
    user_id: uuid.UUID,
    token: str = Form(...),
    username: str = Form(""),
    display_name: str = Form(""),
    discipline: str = Form(""),
    is_public: str = Form(""),
    reminders_enabled: str = Form(""),
    email_verified: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        return Response(status_code=404)
    user.username = username.strip() or None
    user.display_name = display_name.strip() or None
    if discipline in DISCIPLINES:
        user.discipline = discipline
    user.is_public = is_public == "on"
    user.reminders_enabled = reminders_enabled == "on"
    user.email_verified_at = datetime.now(UTC) if email_verified == "on" else None
    await db.commit()
    return RedirectResponse(f"/admin/users/{user_id}?token={token}&saved=1", status_code=303)


@router.post("/admin/users/{user_id}/send-reset")
async def admin_user_send_reset(
    user_id: uuid.UUID,
    token: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        return Response(status_code=404)
    strings = get_strings(user.lang or DEFAULT_LANG)
    reset_token = create_reset_token(user.id, user.password_hash)
    link = f"{settings.base_url}/reset?token={reset_token}"
    await send_email(user.email, strings["mail_reset_subject"], strings["mail_reset_body"].format(link=link))
    return RedirectResponse(f"/admin/users/{user_id}?token={token}&saved=reset_sent", status_code=303)


@router.post("/admin/users/{user_id}/delete")
async def admin_user_delete(
    user_id: uuid.UUID,
    token: str = Form(...),
    confirm_email: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    user = (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none()
    if user is None:
        return Response(status_code=404)
    if confirm_email.strip().lower() != user.email.lower():
        return RedirectResponse(f"/admin/users/{user_id}?token={token}&saved=delete_mismatch", status_code=303)
    await db.delete(user)  # practice_logs, enrollments, subscription, push, follows cascade ile silinir
    await db.commit()
    return RedirectResponse(f"/admin/users?token={token}", status_code=303)


@router.get("/admin/katas", response_class=HTMLResponse)
async def admin_katas(
    request: Request,
    token: str = Query(default=""),
    saved: str = Query(default=""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    result = await db.execute(select(Kata).order_by(Kata.discipline, Kata.sort_order))
    katas = list(result.scalars().all())
    return render(request, "admin_katas.html", katas=katas, token=token, saved=saved)


@router.post("/admin/katas/{slug}")
async def admin_kata_save(
    slug: str,
    token: str = Form(...),
    video_url: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    if not _token_ok(token):
        return Response(status_code=404)
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return Response(status_code=404)
    kata.video_url = normalize_video_url(video_url)
    await db.commit()
    return RedirectResponse(f"/admin/katas?token={token}&saved={slug}#{slug}", status_code=303)
