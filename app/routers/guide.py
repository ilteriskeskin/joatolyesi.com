from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.constants import DISCIPLINES
from app.deps import get_current_user, waitlist_gate
from app.guide_content import GUIDE, get_guide
from app.models import User
from app.render import render

router = APIRouter(dependencies=[Depends(waitlist_gate)])

# Dış kaynaklar: dergi, kulüp, video kanalı gibi siteler. Zamanla elle genişletilir.
RESOURCES = [
    {"name": "Aikido Dergisi", "url": "https://aikidodergisi.com/", "note_tr": "Aikido üzerine Türkçe dergi ve içerik.", "note_en": "Turkish aikido magazine and articles."},
    {"name": "Bosayna", "url": "https://www.bosayna.com/", "note_tr": "Kobudo / silah sanatları üzerine kaynak site.", "note_en": "Resource site on kobudo / weapon arts."},
]


@router.get("/guide", response_class=HTMLResponse)
async def guide_index(request: Request, user: User | None = Depends(get_current_user)):
    """Branş rehberi — giriş istemez (SEO + üyelik öncesi değer)."""
    disciplines = [d for d in DISCIPLINES if d in GUIDE]
    return render(request, "guide_index.html", user=user, disciplines=disciplines, guide=GUIDE)


@router.get("/resources", response_class=HTMLResponse)
async def resources(request: Request, user: User | None = Depends(get_current_user)):
    """Faydalı dış kaynaklar — giriş istemez."""
    return render(request, "resources.html", user=user, resources=RESOURCES)


@router.get("/guide/{discipline}", response_class=HTMLResponse)
async def guide_discipline(
    discipline: str, request: Request, user: User | None = Depends(get_current_user)
):
    content = get_guide(discipline)
    if content is None:
        return render(request, "404.html", user=user)
    return render(request, "guide_discipline.html", user=user, d=discipline, g=content)
