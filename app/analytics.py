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

PRACTICE_SOURCES = ("dashboard", "kata", "first_session")
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


def set_pending_event(response: Response, name: str, params: dict) -> None:
    """Olayı tek seferlik cookie'ye yazar. Değerler cookie-güvenli karakterler
    (küçük harf, rakam, alt çizgi) olduğundan '|' ile ayrılır."""
    if name == "sign_up":
        value = f"sign_up|{params['discipline']}"
    elif name == "practice_logged":
        value = f"practice_logged|{params['discipline']}|{params['minutes']}|{params['source']}"
    elif name == "program_enroll":
        value = f"program_enroll|{params['program']}"
    elif name == "program_day_complete":
        value = f"program_day_complete|{params['program']}|{params['day']}"
    else:
        return
    response.set_cookie(
        PENDING_EVENT_COOKIE, value, max_age=PENDING_EVENT_MAX_AGE, httponly=True, samesite="lax"
    )


def read_pending_event(request: Request) -> dict | None:
    """Cookie'deki olayı doğrular; istemci kontrollü olduğu için yalnız beyaz
    listedeki biçimler kabul edilir, gerisi yok sayılır."""
    raw = request.cookies.get(PENDING_EVENT_COOKIE)
    if not raw:
        return None
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
