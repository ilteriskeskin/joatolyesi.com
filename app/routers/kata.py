from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.deps import ProRequired, is_pro, require_user
from app.models import Kata, User
from app.render import render

router = APIRouter()


@router.get("/kata", response_class=HTMLResponse)
async def kata_list(request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)):
    available_result = await db.execute(select(Kata.discipline).distinct())
    available = sorted(available_result.scalars().all())

    # Varsayılan görünüm kullanıcının branşı; ?d= ile diğerlerine geçilir
    d = request.query_params.get("d")
    if d == "all":
        selected = None
    elif d in available:
        selected = d
    else:
        selected = user.discipline if user.discipline in available else None

    stmt = select(Kata).order_by(Kata.sort_order, Kata.title_en)
    if selected:
        stmt = stmt.where(Kata.discipline == selected)
    result = await db.execute(stmt)
    return render(
        request,
        "kata_list.html",
        user=user,
        katas=list(result.scalars().all()),
        available=available,
        selected=selected,
    )


@router.get("/kata/{slug}", response_class=HTMLResponse)
async def kata_detail(
    slug: str, request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return render(request, "404.html", user=user)
    if not kata.is_free and not is_pro(user):
        raise ProRequired()
    return render(request, "kata_detail.html", user=user, kata=kata)
