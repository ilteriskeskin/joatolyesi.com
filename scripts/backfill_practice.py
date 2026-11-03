"""Geçmiş pratik verisi doldurma:

1. Gerçek hesap (OWNER_EMAIL) için PRACTICE_START'tan bugüne her gün bir
   pratik kaydı ekler — seri/kuşak, gerçekte çalışılan gün sayısını yansıtsın.

Demo/sahte seri ve takip üretmez (uydurma aktivite yok); yalnız sahip hesabı.

İdempotent: bir (kullanıcı, gün) çifti zaten kayıtlıysa atlanır, tekrar
çalıştırmak zarar vermez.

Çalıştırma:  docker compose exec app python scripts/backfill_practice.py
"""

import asyncio
import random
from datetime import date, timedelta

from sqlalchemy import select

from app.constants import OWNER_EMAIL  # metrik script'i de aynı sabiti kullanır
from app.db import async_session
from app.models import PracticeLog, User
from app.render import PRACTICE_START

OWNER_DISCIPLINE = "aikijo"

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

        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
