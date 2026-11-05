"""GA4 dönüşüm olayları için sunucu tarafı yardımcıları.

Redirect ile biten akışlarda (kayıt, kata sayfasından pratik kaydı) gtag
sunucuda çağrılamaz. Bunun yerine kısa ömürlü, tek seferlik bir cookie
bırakılır; bir sonraki tam sayfa render'ı (app/render.py) cookie'yi okur,
olayı şablona verir ve cookie'yi siler — yenilemede olay tekrar gönderilmez.

Olay parametrelerinde kişisel veri (e-posta, kullanıcı adı, id, not) yok:
yalnız beyaz listedeki olay adları ve branş/dakika/kaynak değerleri.
"""

import re

from fastapi import Request, Response

from app.constants import DISCIPLINES

PENDING_EVENT_COOKIE = "ga_evt"
PENDING_EVENT_MAX_AGE = 300  # 5 dk: redirect sonrası ilk sayfaya yeter

PRACTICE_SOURCES = ("dashboard", "kata", "first_session", "program", "daily_kata")
PROGRAM_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")  # program slug'ı: küçük harf, rakam, tire


def _clean_minutes(value: int | str) -> int | None:
    try:
        minutes = int(value)
    except (TypeError, ValueError):
        return None
    return minutes if 1 <= minutes <= 600 else None


def sign_up_params(discipline: str) -> dict | None:
    if discipline not in DISCIPLINES:
        return None
    return {"method": "email", "discipline": discipline}


def practice_logged_params(discipline: str, minutes: int | str, source: str) -> dict | None:
    clean_minutes = _clean_minutes(minutes)
    if discipline not in DISCIPLINES or clean_minutes is None or source not in PRACTICE_SOURCES:
        return None
    return {"discipline": discipline, "minutes": clean_minutes, "source": source}


def program_enroll_params(program: str) -> dict | None:
    if len(program) > 60 or not PROGRAM_SLUG_RE.match(program):
        return None
    return {"program": program}


def program_day_complete_params(program: str, day: int | str) -> dict | None:
    base = program_enroll_params(program)
    try:
        day_number = int(day)
    except (TypeError, ValueError):
        return None
    if base is None or not 1 <= day_number <= 366:
        return None
    return {**base, "day": day_number}


def _encode_event(name: str, params: dict) -> str | None:
    """Değerler cookie-güvenli karakterler (küçük harf, rakam, alt çizgi, tire)
    olduğundan alanlar '|' ile ayrılır."""
    if name == "sign_up":
        return f"sign_up|{params['discipline']}"
    if name == "practice_logged":
        return f"practice_logged|{params['discipline']}|{params['minutes']}|{params['source']}"
    if name == "program_enroll":
        return f"program_enroll|{params['program']}"
    if name == "program_day_complete":
        return f"program_day_complete|{params['program']}|{params['day']}"
    return None


def set_pending_events(response: Response, events: list[tuple[str, dict]]) -> None:
    """Olayları tek seferlik cookie'ye yazar; birden fazla olay '~' ile ayrılır
    (ör. program günü tamamlama: program_day_complete + practice_logged)."""
    values = [v for v in (_encode_event(n, p) for n, p in events) if v]
    if not values:
        return
    response.set_cookie(
        PENDING_EVENT_COOKIE, "~".join(values), max_age=PENDING_EVENT_MAX_AGE, httponly=True, samesite="lax"
    )


def set_pending_event(response: Response, name: str, params: dict) -> None:
    set_pending_events(response, [(name, params)])


def _decode_event(raw: str) -> dict | None:
    parts = raw.split("|")
    params: dict | None = None
    if parts[0] == "sign_up" and len(parts) == 2:
        params = sign_up_params(parts[1])
    elif parts[0] == "practice_logged" and len(parts) == 4:
        params = practice_logged_params(parts[1], parts[2], parts[3])
    elif parts[0] == "program_enroll" and len(parts) == 2:
        params = program_enroll_params(parts[1])
    elif parts[0] == "program_day_complete" and len(parts) == 3:
        params = program_day_complete_params(parts[1], parts[2])
    if params is None:
        return None
    return {"name": parts[0], "params": params}


def read_pending_events(request: Request) -> list[dict]:
    """Cookie'deki olayları doğrular; istemci kontrollü olduğu için yalnız beyaz
    listedeki biçimler kabul edilir (en çok 3 olay), gerisi yok sayılır."""
    raw = request.cookies.get(PENDING_EVENT_COOKIE)
    if not raw:
        return []
    decoded = (_decode_event(part) for part in raw.split("~")[:3])
    return [e for e in decoded if e]
