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


# Seri dondurma: takvim ayı başına bu kadar tek günlük boşluk affedilir
# (hastalık/seyahat affı — Duolingo etkisi). Tablo yok: hesap deterministik.
FREEZES_PER_MONTH = 2


def _streak_with_freezes(dates: list, today) -> tuple[int, int]:
    """(seri, bu ay kullanılan donma) döner. Yalnız 1 günlük boşluklar,
    boşluğun düştüğü ayın bütçesinden harcanarak köprülenir."""
    if not dates:
        return 0, 0
    used: dict = {}

    def try_freeze(day) -> bool:
        key = (day.year, day.month)
        if used.get(key, 0) < FREEZES_PER_MONTH:
            used[key] = used.get(key, 0) + 1
            return True
        return False

    # Canlılık: son kayıt dün/bugün (+ UTC önü yarın) ya da dünü dondurabiliyoruz
    if dates[0] < today - timedelta(days=1):
        if dates[0] == today - timedelta(days=2) and try_freeze(today - timedelta(days=1)):
            pass
        else:
            return 0, 0
    streak = 1
    for prev, curr in zip(dates, dates[1:]):
        gap = (prev - curr).days
        if gap == 1:
            streak += 1
        elif gap == 2 and try_freeze(prev - timedelta(days=1)):
            streak += 1
        else:
            break
    this_month = used.get((today.year, today.month), 0)
    return streak, this_month


async def compute_streak(db: AsyncSession, user_id: uuid.UUID) -> int:
    dates = await _practice_dates(db, user_id)
    today = datetime.now(UTC).date()
    streak, _ = _streak_with_freezes(dates, today)
    return streak


async def streak_info(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Dashboard için: seri + bu ay kalan donma hakkı."""
    dates = await _practice_dates(db, user_id)
    today = datetime.now(UTC).date()
    streak, used_this_month = _streak_with_freezes(dates, today)
    return {"streak": streak, "freezes_left": max(0, FREEZES_PER_MONTH - used_this_month)}


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


async def total_practice_days(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Toplam pratik günü (farklı gün sayısı) — kuşaklar buna göre ilerler."""
    result = await db.execute(
        select(func.count(func.distinct(PracticeLog.practiced_on))).where(PracticeLog.user_id == user_id)
    )
    return result.scalar_one()


async def weekly_summary(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Bu hafta / geçen hafta karşılaştırması + haftanın branşı (dashboard kartı)."""
    today = datetime.now(UTC).date()
    week_start = today - timedelta(days=today.weekday())  # pazartesi
    prev_start = week_start - timedelta(days=7)

    result = await db.execute(
        select(PracticeLog.practiced_on, PracticeLog.discipline, func.sum(PracticeLog.minutes))
        .where(PracticeLog.user_id == user_id, PracticeLog.practiced_on >= prev_start)
        .group_by(PracticeLog.practiced_on, PracticeLog.discipline)
    )
    this_days: set = set()
    this_minutes = prev_minutes = 0
    discipline_minutes: dict[str, int] = {}
    for day, discipline, minutes in result.all():
        if day >= week_start:
            this_days.add(day)
            this_minutes += minutes
            discipline_minutes[discipline] = discipline_minutes.get(discipline, 0) + minutes
        else:
            prev_minutes += minutes

    top = max(discipline_minutes, key=discipline_minutes.get) if discipline_minutes else None
    return {
        "week_days": len(this_days),
        "week_minutes": this_minutes,
        "prev_week_minutes": prev_minutes,
        "week_top_discipline": top,
    }


async def practice_day_counts(db: AsyncSession, user_ids: list[uuid.UUID]) -> dict[uuid.UUID, int]:
    """Birden çok kullanıcı için toplam pratik günü — topluluk listesi tek sorguda."""
    if not user_ids:
        return {}
    result = await db.execute(
        select(PracticeLog.user_id, func.count(func.distinct(PracticeLog.practiced_on)))
        .where(PracticeLog.user_id.in_(user_ids))
        .group_by(PracticeLog.user_id)
    )
    return dict(result.all())


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


async def weekly_leaders(db: AsyncSession) -> list[dict]:
    """Haftanın enleri: bu hafta branşında en çok dakika yapan (açık profil)."""
    from app.models import User

    today = datetime.now(UTC).date()
    week_start = today - timedelta(days=today.weekday())
    result = await db.execute(
        select(PracticeLog.discipline, User, func.sum(PracticeLog.minutes).label("m"))
        .join(User, PracticeLog.user_id == User.id)
        .where(PracticeLog.practiced_on >= week_start, User.is_public, User.username.is_not(None))
        .group_by(PracticeLog.discipline, User.id)
        .order_by(func.sum(PracticeLog.minutes).desc())
    )
    leaders: dict[str, dict] = {}
    for discipline, person, minutes in result.all():
        if discipline not in leaders:
            leaders[discipline] = {"discipline": discipline, "person": person, "minutes": minutes}
    return sorted(leaders.values(), key=lambda x: -x["minutes"])
