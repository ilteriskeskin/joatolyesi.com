from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from app.constants import SELECTABLE_DISCIPLINES
from app.deps import get_current_user, waitlist_gate
from app.guide_content import GUIDE, get_guide
from app.models import User
from app.render import render
from app.tips_content import TIPS

router = APIRouter(dependencies=[Depends(waitlist_gate)])

# Dış kaynaklar: dergi, kulüp, video kanalı gibi siteler. Zamanla elle genişletilir.
RESOURCES = [
    {"name": "Aikido Dergisi", "url": "https://aikidodergisi.com/", "note_tr": "Aikido üzerine Türkçe dergi ve içerik.", "note_en": "Turkish aikido magazine and articles."},
    {"name": "Bosayna", "url": "https://www.bosayna.com/", "note_tr": "Kobudo / silah sanatları üzerine kaynak site.", "note_en": "Resource site on kobudo / weapon arts."},
]


@router.get("/guide", response_class=HTMLResponse)
async def guide_index(request: Request, user: User | None = Depends(get_current_user)):
    """Branş rehberi — giriş istemez (SEO + üyelik öncesi değer)."""
    # Karate/taekwondo rehber içeriği kalıyor (/guide/karate hâlâ erişilebilir),
    # sadece index kartlarından gizleniyor — ürün artık silahlı pratiğe odaklı.
    disciplines = [d for d in SELECTABLE_DISCIPLINES if d in GUIDE]
    return render(request, "guide_index.html", user=user, disciplines=disciplines, guide=GUIDE)


@router.get("/resources", response_class=HTMLResponse)
async def resources(request: Request, user: User | None = Depends(get_current_user)):
    """Faydalı dış kaynaklar — giriş istemez."""
    return render(request, "resources.html", user=user, resources=RESOURCES)


@router.get("/tips", response_class=HTMLResponse)
async def tips(request: Request, user: User | None = Depends(get_current_user)):
    """Günün ipucu — tarihe göre deterministik döner, giriş istemez."""
    day_of_year = datetime.now(UTC).timetuple().tm_yday
    today_tip = TIPS[day_of_year % len(TIPS)]
    return render(request, "tips.html", user=user, today_tip=today_tip, all_tips=TIPS)


@router.get("/guide/{discipline}", response_class=HTMLResponse)
async def guide_discipline(
    discipline: str, request: Request, user: User | None = Depends(get_current_user)
):
    content = get_guide(discipline)
    if content is None:
        return render(request, "404.html", user=user)
    return render(request, "guide_discipline.html", user=user, d=discipline, g=content)
