from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.deps import ProRequired, csrf_protect, get_current_user, is_pro, require_user
from app.models import Kata, PracticeLog, User
from app.rate_limit import limiter
from app.render import render

router = APIRouter()


@router.get("/kata", response_class=HTMLResponse)
async def kata_list(request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    available_result = await db.execute(select(Kata.discipline).distinct())
    available = sorted(available_result.scalars().all())

    # Varsayılan görünüm kullanıcının branşı; ?d= ile diğerlerine geçilir
    d = request.query_params.get("d")
    if d == "all":
        selected = None
    elif d in available:
        selected = d
    else:
        selected = user.discipline if user and user.discipline in available else None

    # Kata / teknik sekmesi — branş seçiliyken anlamlı, "tümü" görünümünde karışık kalır
    kind = request.query_params.get("kind")
    if kind not in ("kata", "teknik"):
        kind = "kata"

    stmt = select(Kata).order_by(Kata.sort_order, Kata.title_en)
    if selected:
        stmt = stmt.where(Kata.discipline == selected, Kata.kind == kind)
    result = await db.execute(stmt)
    katas = list(result.scalars().all())

    # Seçili branşta bu türde hiç içerik yoksa (ör. aikido'da kata) diğer türü öner
    other_kind_has_content = False
    if selected and not katas:
        other = "teknik" if kind == "kata" else "kata"
        count = await db.execute(
            select(func.count(Kata.id)).where(Kata.discipline == selected, Kata.kind == other)
        )
        other_kind_has_content = count.scalar_one() > 0

    return render(
        request,
        "kata_list.html",
        user=user,
        katas=katas,
        available=available,
        selected=selected,
        kind=kind,
        other_kind_has_content=other_kind_has_content,
    )


@router.get("/kata/{slug}", response_class=HTMLResponse)
async def kata_detail(
    slug: str, request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return render(request, "404.html", user=user)
    if not kata.is_free and not is_pro(user):
        if user is None:
            return RedirectResponse("/login", status_code=303)
        raise ProRequired()
    logged = request.query_params.get("logged") == "1"
    return render(request, "kata_detail.html", user=user, kata=kata, logged=logged)


@router.post("/kata/{slug}/log", dependencies=[Depends(csrf_protect)])
@limiter.limit("30/minute")
async def kata_quick_log(
    slug: str,
    request: Request,
    minutes: int = Form(20, ge=1, le=600),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Kata sayfasından tek tuşla pratik kaydı: kütüphaneyi pasif arşivden
    aktif antrenman aracına çevirir."""
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return render(request, "404.html", user=user)
    if not kata.is_free and not is_pro(user):
        raise ProRequired()
    db.add(
        PracticeLog(
            user_id=user.id,
            practiced_on=datetime.now(UTC).date(),
            discipline=kata.discipline,
            minutes=minutes,
            notes=kata.title_tr if (user.lang or "tr") == "tr" else kata.title_en,
        )
    )
    await db.commit()
    return RedirectResponse(f"/kata/{slug}?logged=1", status_code=303)
