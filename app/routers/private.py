"""Sahibine özel sayfalar (/ozel/...).

Yalnız OWNER_EMAIL ile giriş yapmış kullanıcı görür. Giriş yapmamış ziyaretçi
login'e yönlenir; giriş yapmış başka biri 404 alır (sayfanın varlığı belli olmaz).
Sayfalar arama motorlarına kapalıdır (noindex) ve tarayıcıda önbelleklenmez.
"""

from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.config import settings
from app.deps import get_current_user
from app.models import User

router = APIRouter()

PAGES_DIR = Path("app/private_pages")
PRIVATE_HEADERS = {
    "X-Robots-Tag": "noindex, nofollow",
    "Cache-Control": "private, no-store",
}


def is_owner(user: User | None) -> bool:
    owner = settings.owner_email.strip().lower()
    return bool(owner) and user is not None and user.email.strip().lower() == owner


@router.get("/ozel/90-gun", response_class=HTMLResponse)
async def program_90(user: User | None = Depends(get_current_user)) -> Response:
    if not settings.owner_email.strip():
        return Response(status_code=404)
    if user is None:
        return RedirectResponse("/login?next=/ozel/90-gun", status_code=303)
    if not is_owner(user):
        return Response(status_code=404)
    # Küçük statik dosya; her istekte okumak bellek tutmaktan ucuz (512 MB sunucu)
    html = (PAGES_DIR / "program_90.html").read_text(encoding="utf-8")
    return HTMLResponse(html, headers=PRIVATE_HEADERS)
