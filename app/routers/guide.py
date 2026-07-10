from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.constants import DISCIPLINES
from app.deps import get_current_user
from app.guide_content import GUIDE, get_guide
from app.models import User
from app.render import render

router = APIRouter()


@router.get("/guide", response_class=HTMLResponse)
async def guide_index(request: Request, user: User | None = Depends(get_current_user)):
    """Branş rehberi — giriş istemez (SEO + üyelik öncesi değer)."""
    disciplines = [d for d in DISCIPLINES if d in GUIDE]
    return render(request, "guide_index.html", user=user, disciplines=disciplines, guide=GUIDE)


@router.get("/guide/{discipline}", response_class=HTMLResponse)
async def guide_discipline(
    discipline: str, request: Request, user: User | None = Depends(get_current_user)
):
    content = get_guide(discipline)
    if content is None:
        return render(request, "404.html", user=user)
    return render(request, "guide_discipline.html", user=user, d=discipline, g=content)
