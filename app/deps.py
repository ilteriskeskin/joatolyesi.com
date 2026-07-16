import hmac
from datetime import UTC, datetime

from fastapi import Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.db import get_db
from app.models import Subscription, User
from app.security import SESSION_COOKIE, password_fingerprint, read_session_token

PRO_STATUSES = {"on_trial", "active", "past_due", "cancelled"}

# WAITLIST_ONLY açıkken admin panelinden /admin/preview ile set edilen çerez;
# sahibi uygulamayı canlıda diğer ziyaretçiler göremeden test edebilsin diye.
ADMIN_PREVIEW_COOKIE = "admin_preview"


class AuthRequired(Exception):
    pass


class ProRequired(Exception):
    pass


class WaitlistGate(Exception):
    """WAITLIST_ONLY açıkken app rotalarına admin önizlemesi olmadan erişim."""


def has_admin_preview(request: Request) -> bool:
    return hmac.compare_digest(request.cookies.get(ADMIN_PREVIEW_COOKIE, ""), settings.admin_token)


async def waitlist_gate(request: Request) -> None:
    """WAITLIST_ONLY=true iken app rotalarını kapatır — admin önizleme
    çerezi geçerliyse (bkz. /admin/preview) sahibi yine de görebilir."""
    if not settings.waitlist_only:
        return
    if has_admin_preview(request):
        return
    raise WaitlistGate()


def is_pro(user: User | None) -> bool:
    if user is None or user.subscription is None:
        return False
    sub: Subscription = user.subscription
    if sub.status not in PRO_STATUSES:
        return False
    # İptal edilen abonelik dönem sonuna kadar Pro kalır
    if sub.status == "cancelled":
        return sub.ends_at is not None and sub.ends_at > datetime.now(UTC)
    return True


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)) -> User | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    parsed = read_session_token(token)
    if parsed is None:
        return None
    user_id, fingerprint = parsed
    result = await db.execute(
        select(User).options(selectinload(User.subscription)).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    # Parola değiştiyse eski oturumlar düşer
    if user is not None and fingerprint != password_fingerprint(user.password_hash):
        return None
    return user


async def require_user(user: User | None = Depends(get_current_user)) -> User:
    if user is None:
        raise AuthRequired()
    return user


CSRF_COOKIE = "csrf"


async def csrf_protect(request: Request) -> None:
    """Double-submit cookie: formdaki csrf_token (veya X-CSRF-Token header'ı)
    cookie ile eşleşmeli. Cookie render() içinde her sayfada set edilir."""
    cookie = request.cookies.get(CSRF_COOKIE, "")
    token = request.headers.get("x-csrf-token", "")
    if not token:
        form = await request.form()
        token = str(form.get("csrf_token", ""))
    if not cookie or not token or not hmac.compare_digest(cookie, token):
        raise HTTPException(status_code=403, detail="CSRF verification failed")


async def require_pro(user: User = Depends(require_user)) -> User:
    if not is_pro(user):
        raise ProRequired()
    return user
