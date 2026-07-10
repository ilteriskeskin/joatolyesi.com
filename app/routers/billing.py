import json
import uuid
from datetime import datetime
from urllib.parse import quote

from fastapi import APIRouter, Depends, Header, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.deps import is_pro, require_user
from app.models import Subscription, User
from app.render import render
from app.security import verify_ls_signature

router = APIRouter()


def _checkout_url(base: str, user: User) -> str:
    if not base:
        return ""
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}checkout[custom][user_id]={user.id}&checkout[email]={quote(user.email)}"


@router.get("/billing", response_class=HTMLResponse)
async def billing(request: Request, user: User = Depends(require_user)):
    return render(
        request,
        "billing.html",
        user=user,
        pro=is_pro(user),
        subscription=user.subscription,
        checkout_monthly=_checkout_url(settings.ls_checkout_url_monthly, user),
        checkout_yearly=_checkout_url(settings.ls_checkout_url_yearly, user),
    )


def _parse_ts(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


@router.post("/webhooks/lemonsqueezy")
async def ls_webhook(
    request: Request,
    x_signature: str = Header(default=""),
    db: AsyncSession = Depends(get_db),
):
    raw = await request.body()
    if not verify_ls_signature(raw, x_signature):
        return Response(status_code=401)

    payload = json.loads(raw)
    event = payload.get("meta", {}).get("event_name", "")
    if not event.startswith("subscription_"):
        return Response(status_code=200)  # order_created vb. şimdilik ilgi dışı

    custom = payload.get("meta", {}).get("custom_data") or {}
    user_id = custom.get("user_id")
    attrs = payload.get("data", {}).get("attributes", {})
    ls_sub_id = str(payload.get("data", {}).get("id", ""))
    if not ls_sub_id:
        return Response(status_code=400)

    result = await db.execute(select(Subscription).where(Subscription.ls_subscription_id == ls_sub_id))
    sub = result.scalar_one_or_none()

    if sub is None:
        try:
            user_uuid = uuid.UUID(str(user_id))
        except (ValueError, TypeError):
            return Response(status_code=400)
        user_result = await db.execute(select(User).where(User.id == user_uuid))
        if user_result.scalar_one_or_none() is None:
            return Response(status_code=400)
        sub = Subscription(user_id=user_uuid, ls_subscription_id=ls_sub_id, status="active")
        db.add(sub)

    sub.status = attrs.get("status", sub.status)
    sub.variant_name = attrs.get("variant_name") or sub.variant_name
    sub.renews_at = _parse_ts(attrs.get("renews_at")) or sub.renews_at
    sub.ends_at = _parse_ts(attrs.get("ends_at"))
    await db.commit()
    return Response(status_code=200)
