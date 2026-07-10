import hmac
import re

from fastapi import APIRouter, Depends, Form, Query, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.models import Kata
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


@router.get("/admin/katas", response_class=HTMLResponse)
async def admin_katas(
    request: Request,
    token: str = Query(...),
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
