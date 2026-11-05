import hashlib
from functools import lru_cache
import secrets
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.analytics import PENDING_EVENT_COOKIE, read_pending_events
from app.config import settings
from app.constants import is_demo_user
from app.deps import CSRF_COOKIE, is_pro
from app.i18n.strings import DEFAULT_LANG, SUPPORTED_LANGS, get_strings
from app.models import User

templates = Jinja2Templates(directory="app/templates")
templates.env.globals["is_demo_user"] = is_demo_user  # blog yazar satırı: demo -> "Joryu Ekibi"

# style.css içerik hash'i: link'e ?v= olarak eklenir; CSS değişince tarayıcı
# önbelleği ve SW eski stili sunmaz (açılışta bir kez okunur)
templates.env.globals["css_v"] = hashlib.sha256(Path("app/static/css/style.css").read_bytes()).hexdigest()[:10]



@lru_cache(maxsize=None)
def asset(path: str) -> str:
    """Statik dosya URL'si + içerik hash'i (?v=): dosya değişince tarayıcı/SW önbelleği yenilenir."""
    static_root = Path("app/static").resolve()
    target = (static_root / path).resolve()
    if not target.is_relative_to(static_root):
        raise ValueError(f"asset path outside static: {path}")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()[:10]
    return f"/static/{path}?v={digest}"


templates.env.globals["asset"] = asset

# Kesintisiz pratik serisinin başlangıcı — landing'deki gün sayacı buradan türer
PRACTICE_START = date(2025, 8, 11)


def practice_days() -> int:
    today = datetime.now(ZoneInfo("Europe/Istanbul")).date()
    return (today - PRACTICE_START).days + 1


def resolve_lang(request: Request, lang_param: str | None = None) -> str:
    if lang_param in SUPPORTED_LANGS:
        return lang_param
    cookie_lang = request.cookies.get("lang")
    if cookie_lang in SUPPORTED_LANGS:
        return cookie_lang
    accept = request.headers.get("accept-language", "")
    for part in accept.split(","):
        code = part.strip().split(";")[0].split("-")[0].lower()
        if code in SUPPORTED_LANGS:
            return code
    return DEFAULT_LANG


def render(request: Request, template: str, user: User | None = None, **context):
    lang = resolve_lang(request, request.query_params.get("lang"))
    csrf_token = request.cookies.get(CSRF_COOKIE) or secrets.token_urlsafe(32)
    # Bekleyen GA4 olayı yalnız tam sayfada ve admin dışında tüketilir;
    # HTMX partial'ları (_*.html) cookie'yi yutup olayı kaybetmesin
    consume_event = (
        PENDING_EVENT_COOKIE in request.cookies
        and not template.startswith("_")
        and not request.url.path.startswith("/admin")
    )
    ga_events = read_pending_events(request) if consume_event else []
    response = templates.TemplateResponse(
        request,
        template,
        {
            "t": get_strings(lang),
            "lang": lang,
            "other_lang": "tr" if lang == "en" else "en",
            "user": user,
            "user_is_pro": is_pro(user),
            "waitlist_only": settings.waitlist_only,
            "pro_enabled": settings.pro_enabled,
            "practice_days": practice_days(),
            "csrf_token": csrf_token,
            "ga_events": ga_events,
            **context,
        },
    )
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="lax")
    response.set_cookie(
        CSRF_COOKIE,
        csrf_token,
        max_age=60 * 60 * 24 * 30,
        samesite="lax",
        secure=settings.env == "production",
    )
    if consume_event:
        response.delete_cookie(PENDING_EVENT_COOKIE)
    return response
