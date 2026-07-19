"""Haftalık özet e-postası + haftanın enleri bildirimi.

Geçen hafta (Pazartesi-Pazar) en az 1 gün pratik kaydetmiş, hatırlatmaları
açık (reminders_enabled) kullanıcılara "bu hafta X gün, Y dakika, en çok
Z branşı" özeti gönderir. Ayrıca her branşta geçen haftanın en çok
çalışanına (herkese açık profili olan, en az 2 farklı gün çalışmış)
"birincisin" e-postası + push bildirimi gönderir.

Cron (sunucuda, Pazartesi sabahı):
    0 8 * * 1 docker compose --project-directory /root/joryu exec -T app \
        python scripts/send_weekly_digest.py >> /var/log/joryu-weekly.log 2>&1
"""

import asyncio
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select

from app.config import settings
from app.constants import DISCIPLINES
from app.db import async_session
from app.i18n.strings import get_strings
from app.mail import send_email
from app.models import PracticeLog, PushSubscription, User
from app.push import send_push

# En az bu kadar farklı gün çalışmışsa "haftanın birincisi" bildirimi
# gönderilir — tek seanslık, minik bir kayıt yüzünden kutlama gitmesin.
MIN_DAYS_FOR_LEADER = 2


async def main() -> None:
    today = datetime.now(UTC).date()
    this_monday = today - timedelta(days=today.weekday())
    week_start = this_monday - timedelta(days=7)
    week_end = this_monday - timedelta(days=1)
    print(f"Geçen hafta: {week_start} → {week_end}")

    async with async_session() as db:
        # --- Haftalık özet: reminders_enabled + geçen hafta en az 1 gün ---
        result = await db.execute(
            select(
                PracticeLog.user_id,
                func.count(func.distinct(PracticeLog.practiced_on)),
                func.sum(PracticeLog.minutes),
            )
            .where(PracticeLog.practiced_on.between(week_start, week_end))
            .group_by(PracticeLog.user_id)
        )
        totals_by_user = {row[0]: (row[1], row[2]) for row in result.all()}

        top_result = await db.execute(
            select(PracticeLog.user_id, PracticeLog.discipline, func.sum(PracticeLog.minutes))
            .where(PracticeLog.practiced_on.between(week_start, week_end))
            .group_by(PracticeLog.user_id, PracticeLog.discipline)
        )
        top_discipline_by_user: dict = {}
        best_minutes: dict = {}
        for user_id, discipline, minutes in top_result.all():
            if minutes > best_minutes.get(user_id, -1):
                best_minutes[user_id] = minutes
                top_discipline_by_user[user_id] = discipline

        if totals_by_user:
            opted_in = await db.execute(
                select(User).where(User.reminders_enabled, User.id.in_(totals_by_user.keys()))
            )
            digest_count = 0
            for user in opted_in.scalars().all():
                days, minutes = totals_by_user[user.id]
                strings = get_strings(user.lang or "tr")
                discipline = top_discipline_by_user.get(user.id, "other")
                await send_email(
                    user.email,
                    strings["mail_weekly_subject"],
                    strings["mail_weekly_body"].format(
                        days=days, minutes=minutes,
                        discipline=strings[f"discipline_{discipline}"],
                        link=f"{settings.base_url}/app",
                    ),
                )
                digest_count += 1
                await asyncio.sleep(0.6)  # Resend rate limiti
            print(f"Haftalık özet: {digest_count} kullanıcıya gönderildi")
        else:
            print("Haftalık özet: geçen hafta hiç kayıt yok, atlandı")

        # --- Haftanın enleri: branş başına en çok dakika yapan ---
        leader_result = await db.execute(
            select(
                PracticeLog.discipline, User,
                func.count(func.distinct(PracticeLog.practiced_on)).label("days"),
                func.sum(PracticeLog.minutes).label("minutes"),
            )
            .join(User, PracticeLog.user_id == User.id)
            .where(PracticeLog.practiced_on.between(week_start, week_end))
            .group_by(PracticeLog.discipline, User.id)
            .order_by(func.sum(PracticeLog.minutes).desc())
        )
        leaders: dict = {}
        for discipline, person, days, minutes in leader_result.all():
            if discipline in leaders or days < MIN_DAYS_FOR_LEADER:
                continue
            leaders[discipline] = person

        leader_count = 0
        for discipline in DISCIPLINES:
            person = leaders.get(discipline)
            if person is None:
                continue
            strings = get_strings(person.lang or "tr")
            label = strings[f"discipline_{discipline}"]
            await send_email(
                person.email,
                strings["mail_weekly_leader_subject"],
                strings["mail_weekly_leader_body"].format(discipline=label, link=f"{settings.base_url}/practitioners"),
            )
            subs = (
                await db.execute(select(PushSubscription).where(PushSubscription.user_id == person.id))
            ).scalars().all()
            title = strings["push_weekly_leader_title"]
            body = strings["push_weekly_leader_body"].format(discipline=label)
            for sub in subs:
                subscription_info = {"endpoint": sub.endpoint, "keys": {"p256dh": sub.p256dh, "auth": sub.auth}}
                alive = await send_push(subscription_info, title, body, url="/practitioners")
                if not alive:
                    await db.delete(sub)
            leader_count += 1
            print(f"  birinci -> {person.email} ({discipline})")
            await asyncio.sleep(0.6)

        print(f"Haftanın enleri: {leader_count} bildirim gönderildi")
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
