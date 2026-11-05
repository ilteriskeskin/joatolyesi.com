"""Günün tekniği: dashboard kartı ve hatırlatma maili aynı seçimi kullanır.

Seçim deterministik: (tarih, kullanıcı) çiftinden türer, aynı gün aynı teknik
çıkar; tek sorgu (kullanıcının branşı + aikijo yedeği)."""

import hashlib
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.constants import SELECTABLE_DISCIPLINES
from app.models import Kata, User

FALLBACK_DISCIPLINE = "aikijo"


def choose_daily_kata(katas: list[Kata], user: User, today: date) -> Kata | None:
    """Saf seçim: branş havuzu (yoksa aikijo) -> videosu olanlar öncelikli
    (hiçbiri yoksa teknikler, yoksa hepsi) -> tarih+kullanıcı hash'i."""
    pool = [k for k in katas if k.discipline == user.discipline] or [
        k for k in katas if k.discipline == FALLBACK_DISCIPLINE
    ]
    if not pool:
        return None
    with_video = [k for k in pool if k.video_url]
    pool = with_video or [k for k in pool if k.kind == "teknik"] or pool
    pool = sorted(pool, key=lambda k: k.slug)
    digest = hashlib.sha256(f"{today.isoformat()}:{user.id}".encode()).hexdigest()
    return pool[int(digest, 16) % len(pool)]


async def pick_daily_kata(db: AsyncSession, user: User, today: date) -> Kata | None:
    stmt = select(Kata).where(
        Kata.discipline.in_({user.discipline, FALLBACK_DISCIPLINE} & set(SELECTABLE_DISCIPLINES))
    )
    if settings.pro_enabled:
        stmt = stmt.where(Kata.is_free)
    katas = list((await db.execute(stmt)).scalars().all())
    return choose_daily_kata(katas, user, today)
