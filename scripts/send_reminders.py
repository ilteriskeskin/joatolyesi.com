"""Günlük pratik hatırlatması: BUGÜN pratik kaydetmemiş kullanıcılara
kısa bir hatırlatma — e-posta (opt-in: reminders_enabled) ve/veya push
bildirimi (opt-in: aktif bir PushSubscription varlığı).

Cron (sunucuda, akşam 18:00 UTC ≈ 21:00 TR):
    0 18 * * * docker compose --project-directory /root/joryu exec -T app \
        python scripts/send_reminders.py >> /var/log/joryu-reminders.log 2>&1
"""

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.config import settings
from app.db import async_session
from app.i18n.strings import get_strings
from app.mail import send_email
from app.models import PracticeLog, PushSubscription, User
from app.push import send_push
from app.stats import streak_info


async def main() -> None:
    today = datetime.now(UTC).date()
    async with async_session() as db:
        logged_today = select(PracticeLog.user_id).where(PracticeLog.practiced_on == today)

        # E-posta: yalnız opt-in kullanıcılar
        result = await db.execute(
            select(User).where(User.reminders_enabled, User.id.not_in(logged_today))
        )
        email_users = list(result.scalars().all())
        print(f"E-posta hatırlatması: {len(email_users)} kullanıcı")
        for user in email_users:
            info = await streak_info(db, user.id)
            strings = get_strings(user.lang or "tr")
            await send_email(
                user.email,
                strings["mail_reminder_subject"],
                strings["mail_reminder_body"].format(streak=info["streak"], link=f"{settings.base_url}/app"),
            )
            print(f"  mail -> {user.email} (seri: {info['streak']})")
            await asyncio.sleep(0.6)  # Resend rate limiti

        # Push: aktif bir aboneliği olan (kaydetmemiş) kullanıcılar
        result = await db.execute(
            select(User)
            .options(selectinload(User.push_subscriptions))
            .join(PushSubscription, PushSubscription.user_id == User.id)
            .where(User.id.not_in(logged_today))
            .distinct()
        )
        push_users = list(result.scalars().all())
        print(f"Push hatırlatması: {len(push_users)} kullanıcı")
        for user in push_users:
            info = await streak_info(db, user.id)
            strings = get_strings(user.lang or "tr")
            title = strings["push_reminder_title"]
            body = strings["push_reminder_body"].format(streak=info["streak"])
            for sub in user.push_subscriptions:
                subscription_info = {
                    "endpoint": sub.endpoint,
                    "keys": {"p256dh": sub.p256dh, "auth": sub.auth},
                }
                alive = await send_push(subscription_info, title, body, url="/app")
                if not alive:
                    await db.delete(sub)
            print(f"  push -> {user.email} (seri: {info['streak']})")
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
