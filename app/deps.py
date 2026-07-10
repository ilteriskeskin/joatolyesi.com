from datetime import UTC, datetime

from fastapi import Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.models import Subscription, User
from app.security import SESSION_COOKIE, read_session_token

PRO_STATUSES = {"on_trial", "active", "past_due", "cancelled"}


class AuthRequired(Exception):
    pass


class ProRequired(Exception):
    pass


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
    user_id = read_session_token(token)
    if user_id is None:
        return None
    result = await db.execute(
        select(User).options(selectinload(User.subscription)).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def require_user(user: User | None = Depends(get_current_user)) -> User:
    if user is None:
        raise AuthRequired()
    return user


async def require_pro(user: User = Depends(require_user)) -> User:
    if not is_pro(user):
        raise ProRequired()
    return user
