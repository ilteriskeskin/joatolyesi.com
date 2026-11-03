"""GA4 dönüşüm olayları için sunucu tarafı yardımcıları.

Redirect ile biten akışlarda (kayıt, kata sayfasından pratik kaydı) gtag
sunucuda çağrılamaz. Bunun yerine kısa ömürlü, tek seferlik bir cookie
bırakılır; bir sonraki tam sayfa render'ı (app/render.py) cookie'yi okur,
olayı şablona verir ve cookie'yi siler — yenilemede olay tekrar gönderilmez.

Olay parametrelerinde kişisel veri (e-posta, kullanıcı adı, id, not) yok:
yalnız beyaz listedeki olay adları ve branş/dakika/kaynak değerleri.
"""

from fastapi import Request, Response

from app.constants import DISCIPLINES

PENDING_EVENT_COOKIE = "ga_evt"
PENDING_EVENT_MAX_AGE = 300  # 5 dk: redirect sonrası ilk sayfaya yeter

PRACTICE_SOURCES = ("dashboard", "kata")


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


def set_pending_event(response: Response, name: str, params: dict) -> None:
    """Olayı tek seferlik cookie'ye yazar. Değerler cookie-güvenli karakterler
    (küçük harf, rakam, alt çizgi) olduğundan '|' ile ayrılır."""
    if name == "sign_up":
        value = f"sign_up|{params['discipline']}"
    elif name == "practice_logged":
        value = f"practice_logged|{params['discipline']}|{params['minutes']}|{params['source']}"
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
    if params is None:
        return None
    return {"name": parts[0], "params": params}
