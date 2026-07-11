"""Günlük pratik hatırlatması: hatırlatmayı açmış ve BUGÜN pratik
kaydetmemiş kullanıcılara kısa bir e-posta.

Cron (sunucuda, akşam 18:00 UTC ≈ 21:00 TR):
    0 18 * * * docker compose --project-directory /root/joryu exec -T app \
        python scripts/send_reminders.py >> /var/log/joryu-reminders.log 2>&1
"""

import asyncio
from datetime import UTC, datetime

from sqlalchemy import select

from app.config import settings
from app.db import async_session
from app.i18n.strings import get_strings
from app.mail import send_email
from app.models import PracticeLog, User
from app.stats import streak_info


async def main() -> None:
    today = datetime.now(UTC).date()
    async with async_session() as db:
        logged_today = select(PracticeLog.user_id).where(PracticeLog.practiced_on == today)
        result = await db.execute(
            select(User).where(User.reminders_enabled, User.id.not_in(logged_today))
        )
        users = list(result.scalars().all())
        print(f"Hatırlatma gönderilecek: {len(users)} kullanıcı")
        for user in users:
            info = await streak_info(db, user.id)
            strings = get_strings(user.lang or "tr")
            await send_email(
                user.email,
                strings["mail_reminder_subject"],
                strings["mail_reminder_body"].format(streak=info["streak"], link=f"{settings.base_url}/app"),
            )
            print(f"  -> {user.email} (seri: {info['streak']})")
            await asyncio.sleep(0.6)  # Resend rate limiti


if __name__ == "__main__":
    asyncio.run(main())
