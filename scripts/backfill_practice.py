"""Geçmiş pratik verisi doldurma:

1. Gerçek hesap (OWNER_EMAIL) için PRACTICE_START'tan bugüne her gün bir
   pratik kaydı ekler — seri/kuşak, gerçekte çalışılan gün sayısını yansıtsın.
2. seed_blog.py ile oluşturulan demo kullanıcılara, her birine farklı bir
   seri uzunluğu vererek (DEMO_STREAKS) farklı kuşak seviyeleri kazandırır —
   topluluk sayfası ve profiller boş görünmesin diye.
3. Demo kullanıcılar arasında birkaç takip ilişkisi kurar.

İdempotent: bir (kullanıcı, gün) çifti zaten kayıtlıysa atlanır, tekrar
çalıştırmak zarar vermez.

Çalıştırma:  docker compose exec app python scripts/backfill_practice.py
"""

import asyncio
import random
from datetime import date, timedelta

from sqlalchemy import select

from app.db import async_session
from app.models import Follow, PracticeLog, User
from app.render import PRACTICE_START

OWNER_EMAIL = "aliilteriskeskin@gmail.com"
OWNER_DISCIPLINE = "aikijo"

# username -> (son N gün kesintisiz seri, sonuçta hangi kuşağa denk geldiği)
DEMO_STREAKS = {
    "suburi-defteri": 8,        # beyaz kuşak (henüz 30 günü doldurmamış)
    "tatami-notlari": 45,       # sarı kuşak (30+)
    "sabah-keiko": 150,         # yeşil kuşak (120+)
    "poomsae-calismasi": 220,   # mavi kuşak (200+)
    "kenshin-yolda": 400,       # siyah kuşak (365+)
}

# Basit bir takip zinciri — topluluk sayfası boş görünmesin
FOLLOW_CHAIN = [
    "suburi-defteri", "tatami-notlari", "sabah-keiko", "poomsae-calismasi", "kenshin-yolda",
]


async def _existing_dates(db, user_id) -> set[date]:
    result = await db.execute(
        select(PracticeLog.practiced_on).where(PracticeLog.user_id == user_id)
    )
    return set(result.scalars().all())


async def _backfill_range(db, user_id: str, discipline: str, start: date, end: date) -> int:
    existing = await _existing_dates(db, user_id)
    added = 0
    day = start
    while day <= end:
        if day not in existing:
            db.add(
                PracticeLog(
                    user_id=user_id,
                    practiced_on=day,
                    discipline=discipline,
                    minutes=random.randint(15, 45),
                )
            )
            added += 1
        day += timedelta(days=1)
    return added


async def main() -> None:
    today = date.today()
    async with async_session() as db:
        owner = (await db.execute(select(User).where(User.email == OWNER_EMAIL))).scalar_one_or_none()
        if owner is None:
            print(f"UYARI: {OWNER_EMAIL} bulunamadı, sahibin pratik geçmişi atlandı.")
        else:
            added = await _backfill_range(db, owner.id, OWNER_DISCIPLINE, PRACTICE_START, today)
            print(f"sahip: {added} gün eklendi ({PRACTICE_START} → {today})")

        users_by_username: dict[str, User] = {}
        for username, streak_days in DEMO_STREAKS.items():
            user = (await db.execute(select(User).where(User.username == username))).scalar_one_or_none()
            if user is None:
                print(f"UYARI: demo kullanıcı yok, önce scripts/seed_blog.py çalıştır: {username}")
                continue
            users_by_username[username] = user
            start = today - timedelta(days=streak_days - 1)
            added = await _backfill_range(db, user.id, user.discipline, start, today)
            print(f"{username}: {added} gün eklendi ({streak_days} günlük seri)")

        for i, username in enumerate(FOLLOW_CHAIN):
            follower = users_by_username.get(username)
            followee = users_by_username.get(FOLLOW_CHAIN[(i + 1) % len(FOLLOW_CHAIN)])
            if not follower or not followee or follower.id == followee.id:
                continue
            existing_follow = (
                await db.execute(
                    select(Follow).where(Follow.follower_id == follower.id, Follow.followee_id == followee.id)
                )
            ).scalar_one_or_none()
            if existing_follow is None:
                db.add(Follow(follower_id=follower.id, followee_id=followee.id))
                print(f"takip eklendi: {username} -> {FOLLOW_CHAIN[(i + 1) % len(FOLLOW_CHAIN)]}")

        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
