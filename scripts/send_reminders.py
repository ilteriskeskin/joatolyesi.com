"""Günlük pratik hatırlatması: BUGÜN pratik kaydetmemiş kullanıcılara
kısa bir hatırlatma — e-posta (opt-in: reminders_enabled) ve/veya push
bildirimi (opt-in: aktif bir PushSubscription varlığı). E-posta içeriği
kişiseldir (program günü / enroll sonrası gün 1/3/7 "kaldığın yerden devam" / "bugün son gün" / günün tekniği), bkz. app/reminders.py.

Cron (sunucuda, akşam 18:00 UTC ≈ 21:00 TR):
    0 18 * * * docker compose --project-directory /root/joryu exec -T app \
        python scripts/send_reminders.py >> /var/log/joryu-reminders.log 2>&1
"""

import asyncio
import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db import async_session
from app.mail import send_email
from app.models import Enrollment, PracticeLog, PushSubscription, User
from app.push import send_push
from app.reminders import build_push, build_reminder, unsubscribe_headers
from app.stats import streak_info


logger = logging.getLogger("joryu.reminders")


async def _send_email_reminder(user_id, today) -> None:
    # Her kullanıcı kendi oturumunda: bir kullanıcının hatası ötekilerin oturumunu bozmaz
    async with async_session() as db:
        user = (
            await db.execute(select(User).options(selectinload(User.subscription)).where(User.id == user_id))
        ).scalar_one()
        info = await streak_info(db, user.id)
        reminder = await build_reminder(db, user, today, info)
        await send_email(user.email, reminder["subject"], reminder["html"], headers=unsubscribe_headers(user))
        if reminder["kind"] == "program_comeback":
            # Gönderim başarılıysa adımı işaretle: script aynı gün tekrar koşsa ikinci mail gitmez
            enrollment = await db.get(Enrollment, reminder["enrollment_id"])
            enrollment.last_comeback_step = reminder["step"]
            await db.commit()
        print(f"  mail -> {user.email} (seri: {info['streak']}, tür: {reminder['kind']})")


async def _send_push_reminder(user_id, today) -> None:
    async with async_session() as db:
        user = (
            await db.execute(
                select(User)
                .options(selectinload(User.push_subscriptions), selectinload(User.subscription))
                .where(User.id == user_id)
            )
        ).scalar_one()
        info = await streak_info(db, user.id)
        push = await build_push(db, user, today, info)
        try:
            for sub in user.push_subscriptions:
                subscription_info = {
                    "endpoint": sub.endpoint,
                    "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                }
                alive = await send_push(subscription_info, push["title"], push["body"], url=push["url"])
                if not alive:
                    await db.delete(sub)
        finally:
            # Döngü yarıda kesilse bile ölü abonelik silmeleri kaybolmasın
            await db.commit()
        print(f"  push -> {user.email} (seri: {info['streak']})")


async def main() -> None:
    today = datetime.now(UTC).date()
    async with async_session() as db:
        logged_today = select(PracticeLog.user_id).where(PracticeLog.practiced_on == today)

        # E-posta: yalnız opt-in kullanıcılar
        result = await db.execute(select(User.id).where(User.reminders_enabled, User.id.not_in(logged_today)))
        email_ids = list(result.scalars().all())
        # Push: aktif bir aboneliği olan (kaydetmemiş) kullanıcılar
        result = await db.execute(
            select(User.id)
            .join(PushSubscription, PushSubscription.user_id == User.id)
            .where(User.id.not_in(logged_today))
            .distinct()
        )
        push_ids = list(result.scalars().all())

    print(f"E-posta hatırlatması: {len(email_ids)} kullanıcı")
    for user_id in email_ids:
        try:
            await _send_email_reminder(user_id, today)
        except Exception:
            logger.exception("E-posta hatırlatması başarısız user_id=%s", user_id)
            continue
        await asyncio.sleep(0.6)  # Resend rate limiti

    print(f"Push hatırlatması: {len(push_ids)} kullanıcı")
    for user_id in push_ids:
        try:
            await _send_push_reminder(user_id, today)
        except Exception:
            logger.exception("Push hatırlatması başarısız user_id=%s", user_id)
            continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
