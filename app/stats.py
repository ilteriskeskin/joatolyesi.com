"""Pratik istatistikleri: seri, toplamlar, GitHub tarzı aktivite ızgarası."""

import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import DISCIPLINES
from app.models import PracticeLog

HEATMAP_WEEKS = 16


async def _practice_dates(db: AsyncSession, user_id: uuid.UUID) -> list:
    """Kullanıcının pratik yaptığı günler, en yeniden eskiye."""
    result = await db.execute(
        select(PracticeLog.practiced_on)
        .where(PracticeLog.user_id == user_id)
        .distinct()
        .order_by(PracticeLog.practiced_on.desc())
    )
    return list(result.scalars().all())


async def compute_streak(db: AsyncSession, user_id: uuid.UUID) -> int:
    dates = await _practice_dates(db, user_id)
    if not dates:
        return 0
    today = datetime.now(UTC).date()
    # Seri canlı sayılır: son kayıt dünden eski değil.
    # (UTC'nin önündeki dilimler "yarın" tarihli kayıt atabilir, o da canlı.)
    if dates[0] < today - timedelta(days=1):
        return 0
    streak = 1
    for prev, curr in zip(dates, dates[1:]):
        if prev - curr == timedelta(days=1):
            streak += 1
        else:
            break
    return streak


async def compute_longest_streak(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Tüm zamanların en uzun serisi — rozetler buna bakar, bozulan seri
    kazanılmış rozeti geri almaz."""
    dates = await _practice_dates(db, user_id)
    if not dates:
        return 0
    longest = current = 1
    for prev, curr in zip(dates, dates[1:]):
        if prev - curr == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


async def practice_stats(db: AsyncSession, user_id: uuid.UUID) -> dict:
    result = await db.execute(
        select(func.count(PracticeLog.id), func.coalesce(func.sum(PracticeLog.minutes), 0)).where(
            PracticeLog.user_id == user_id
        )
    )
    sessions, minutes = result.one()
    return {"total_sessions": sessions, "total_minutes": minutes}


async def build_heatmap(db: AsyncSession, user_id: uuid.UUID) -> list[list[dict]]:
    """Sütun = hafta, satır = gün (Pzt–Paz). Her hücre: tarih, yoğunluk
    kademesi, toplam dakika ve o gün çalışılan branşlar (tooltip için)."""
    today = datetime.now(UTC).date()
    start = today - timedelta(days=HEATMAP_WEEKS * 7 - 1)
    start -= timedelta(days=start.weekday())  # haftanın pazartesisine hizala

    result = await db.execute(
        select(PracticeLog.practiced_on, PracticeLog.discipline, func.sum(PracticeLog.minutes))
        .where(PracticeLog.user_id == user_id, PracticeLog.practiced_on >= start)
        .group_by(PracticeLog.practiced_on, PracticeLog.discipline)
    )
    totals: dict = {}
    disciplines: dict = {}
    for day, discipline, minutes in result.all():
        totals[day] = totals.get(day, 0) + minutes
        disciplines.setdefault(day, set()).add(discipline)

    # UTC'nin önündeki dilimlerden "yarın" tarihli kayıt gelebilir;
    # veri olan günler bugünden ilerideyse grid onları da kapsasın
    grid_end = max([today, *totals.keys()])

    weeks = []
    week_start = start
    while week_start <= grid_end:
        week = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            minutes = totals.get(day, 0)
            if minutes == 0:
                level = None if day > today else 0
            elif minutes < 15:
                level = 1
            elif minutes < 30:
                level = 2
            elif minutes < 60:
                level = 3
            else:
                level = 4
            day_disciplines = sorted(disciplines.get(day, ()), key=DISCIPLINES.index)
            week.append(
                {"date": day.isoformat(), "level": level, "minutes": minutes, "disciplines": day_disciplines}
            )
        weeks.append(week)
        week_start += timedelta(days=7)
    return weeks
