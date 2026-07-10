from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.deps import is_pro
from app.i18n.strings import DEFAULT_LANG, SUPPORTED_LANGS, get_strings
from app.models import User

templates = Jinja2Templates(directory="app/templates")


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
            **context,
        },
    )
    response.set_cookie("lang", lang, max_age=60 * 60 * 24 * 365, samesite="lax")
    return response
