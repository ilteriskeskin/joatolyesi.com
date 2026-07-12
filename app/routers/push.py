from fastapi import APIRouter, Depends, Form
from fastapi.responses import JSONResponse, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.deps import csrf_protect, require_user
from app.models import PushSubscription, User

router = APIRouter()


@router.get("/push/vapid-public-key")
async def vapid_public_key():
    """Herkese açık anahtar — tarayıcı PushManager.subscribe() için kullanır."""
    return JSONResponse({"key": settings.vapid_public_key})


@router.post("/push/subscribe", dependencies=[Depends(csrf_protect)])
async def push_subscribe(
    endpoint: str = Form(...),
    p256dh: str = Form(...),
    auth: str = Form(...),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    existing = (
        await db.execute(select(PushSubscription).where(PushSubscription.endpoint == endpoint))
    ).scalar_one_or_none()
    if existing is None:
        db.add(PushSubscription(user_id=user.id, endpoint=endpoint, p256dh=p256dh, auth=auth))
        await db.commit()
    return Response(status_code=204)


@router.post("/push/unsubscribe", dependencies=[Depends(csrf_protect)])
async def push_unsubscribe(
    endpoint: str = Form(...),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    existing = (
        await db.execute(
            select(PushSubscription).where(
                PushSubscription.endpoint == endpoint, PushSubscription.user_id == user.id
            )
        )
    ).scalar_one_or_none()
    if existing is not None:
        await db.delete(existing)
        await db.commit()
    return Response(status_code=204)
