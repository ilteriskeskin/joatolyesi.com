import hmac
import re

from fastapi import APIRouter, Depends, Form, Query, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.mail import send_email
from app.models import Kata, Waitlist
from app.render import render

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
    )


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
