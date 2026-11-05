"""Pratik istatistikleri: seri, toplamlar, GitHub tarzı aktivite ızgarası."""

import uuid
from datetime import UTC, date, datetime, timedelta

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


# Seri kuralı "2 günde 1": iki pratik günü arasında en fazla 1 boş gün varsa
# (aradaki fark <= 2) zincir sürer. Donma hakkı: takvim ayı başına bu kadar
# "2 boş günlük" boşluk (fark == 3) köprülenir — hastalık/seyahat affı.
# Tablo yok: hesap deterministik.
FREEZES_PER_MONTH = 2
MAX_FREE_GAP = 2  # iki pratik günü arası bu kadar gün ya da daha az: zincir sürer


def _streak_state(dates: list, today) -> dict:
    """dates: pratik günleri, yeniden eskiye (distinct). Döner:
    streak = zincirin ilk pratik gününden son pratik gününe takvim günü (dahil),
    used = bu ay harcanan donma, last_day = "bugün son gün" uyarısı durumu.

    Canlılık: son pratik >= bugün-2 ise seri canlı; bugün-3 ise (2 boş gün) bir
    donma hakkıyla köprülenebilir; daha eskiyse seri bitmiştir. Boşluğun
    donması boşluğun son boş gününün ayından harcanır."""
    if not dates:
        return {"streak": 0, "used": 0, "last_day": False, "last_day_freeze": False}
    used: dict = {}

    def try_freeze(day) -> bool:
        key = (day.year, day.month)
        if used.get(key, 0) < FREEZES_PER_MONTH:
            used[key] = used.get(key, 0) + 1
            return True
        return False

    since_last = (today - dates[0]).days
    if since_last > MAX_FREE_GAP + 1:
        return {"streak": 0, "used": 0, "last_day": False, "last_day_freeze": False}
    if since_last == MAX_FREE_GAP + 1 and not try_freeze(today - timedelta(days=1)):
        return {"streak": 0, "used": 0, "last_day": False, "last_day_freeze": False}

    oldest = dates[0]
    for prev, curr in zip(dates, dates[1:]):
        gap = (prev - curr).days
        if gap <= MAX_FREE_GAP or (gap == MAX_FREE_GAP + 1 and try_freeze(prev - timedelta(days=1))):
            oldest = curr
        else:
            break
    return {
        "streak": (dates[0] - oldest).days + 1,
        "used": used.get((today.year, today.month), 0),
        # Son pratik dün değil önceki gün (bugün pratik yok): yarın boşluk 2 gün olur
        "last_day": since_last == MAX_FREE_GAP,
        # Bugün çalışılmazsa yarın fark 3 olur ve bugünün ayından bir donma gerekir:
        # bütçe varsa seri donmayla sürer ("hak harcanır"), yoksa biter
        "last_day_freeze": since_last == MAX_FREE_GAP
        and used.get((today.year, today.month), 0) < FREEZES_PER_MONTH,
    }


def _streak_with_freezes(dates: list, today) -> tuple[int, int]:
    """(seri, bu ay kullanılan donma) döner."""
    state = _streak_state(dates, today)
    return state["streak"], state["used"]


def _longest_streak(dates: list) -> int:
    """Tüm zamanların en uzun zinciri (takvim günü, dahil); donma sayılmaz."""
    if not dates:
        return 0
    longest = 1
    chain_end = dates[0]
    for prev, curr in zip(dates, dates[1:]):
        if (prev - curr).days > MAX_FREE_GAP:
            chain_end = curr
        longest = max(longest, (chain_end - curr).days + 1)
    return longest


async def compute_streak(db: AsyncSession, user_id: uuid.UUID) -> int:
    dates = await _practice_dates(db, user_id)
    today = datetime.now(UTC).date()
    streak, _ = _streak_with_freezes(dates, today)
    return streak


async def streak_info(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Dashboard/hatırlatma için: seri + bu ay kalan donma hakkı + "bugün son gün"."""
    dates = await _practice_dates(db, user_id)
    today = datetime.now(UTC).date()
    state = _streak_state(dates, today)
    return {
        "streak": state["streak"],
        "freezes_left": max(0, FREEZES_PER_MONTH - state["used"]),
        "last_day": state["last_day"],
        "last_day_freeze": state["last_day_freeze"],
    }


async def compute_longest_streak(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Tüm zamanların en uzun serisi — rozetler buna bakar, bozulan seri
    kazanılmış rozeti geri almaz."""
    return _longest_streak(await _practice_dates(db, user_id))


async def total_practice_days(db: AsyncSession, user_id: uuid.UUID) -> int:
    """Toplam pratik günü (farklı gün sayısı) — kuşaklar buna göre ilerler.
    Planlı dinlenme günleri sayılmaz: seviye ilerlemesi gerçek pratik ister."""
    result = await db.execute(
        select(func.count(func.distinct(PracticeLog.practiced_on))).where(
            PracticeLog.user_id == user_id, PracticeLog.is_rest_day.is_(False)
        )
    )
    return result.scalar_one()


# Planlı dinlenme günü: haftada bu kadar hak, seriyi bozmaz. Pazartesi başlangıçlı hafta.
REST_DAYS_PER_WEEK = 1


def _week_start(today: date) -> date:
    return today - timedelta(days=today.weekday())


async def rest_days_used_this_week(db: AsyncSession, user_id: uuid.UUID) -> int:
    today = datetime.now(UTC).date()
    result = await db.execute(
        select(func.count(PracticeLog.id)).where(
            PracticeLog.user_id == user_id,
            PracticeLog.is_rest_day.is_(True),
            PracticeLog.practiced_on >= _week_start(today),
        )
    )
    return result.scalar_one()


async def weekly_summary(db: AsyncSession, user_id: uuid.UUID) -> dict:
    """Bu hafta / geçen hafta karşılaştırması + haftanın branşı (dashboard kartı).
    Planlı dinlenme günleri pratik istatistiğine dahil edilmez."""
    today = datetime.now(UTC).date()
    week_start = today - timedelta(days=today.weekday())  # pazartesi
    prev_start = week_start - timedelta(days=7)

    result = await db.execute(
        select(PracticeLog.practiced_on, PracticeLog.discipline, func.sum(PracticeLog.minutes))
        .where(
            PracticeLog.user_id == user_id,
            PracticeLog.practiced_on >= prev_start,
            PracticeLog.is_rest_day.is_(False),
        )
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
        .where(PracticeLog.user_id.in_(user_ids), PracticeLog.is_rest_day.is_(False))
        .group_by(PracticeLog.user_id)
    )
    return dict(result.all())


async def practice_stats(db: AsyncSession, user_id: uuid.UUID) -> dict:
    result = await db.execute(
        select(func.count(PracticeLog.id), func.coalesce(func.sum(PracticeLog.minutes), 0)).where(
            PracticeLog.user_id == user_id, PracticeLog.is_rest_day.is_(False)
        )
    )
    sessions, minutes = result.one()
    return {"total_sessions": sessions, "total_minutes": minutes}


async def build_heatmap(db: AsyncSession, user_id: uuid.UUID) -> list[list[dict]]:
    """Sütun = hafta, satır = gün (Pzt–Paz). Her hücre: tarih, yoğunluk
    kademesi, toplam dakika ve o gün çalışılan branşlar (tooltip için).
    Planlı dinlenme günleri ayrı bir desenle ("rest" kademesi) işaretlenir."""
    today = datetime.now(UTC).date()
    start = today - timedelta(days=HEATMAP_WEEKS * 7 - 1)
    start -= timedelta(days=start.weekday())  # haftanın pazartesisine hizala

    result = await db.execute(
        select(PracticeLog.practiced_on, PracticeLog.discipline, func.sum(PracticeLog.minutes))
        .where(
            PracticeLog.user_id == user_id,
            PracticeLog.practiced_on >= start,
            PracticeLog.is_rest_day.is_(False),
        )
        .group_by(PracticeLog.practiced_on, PracticeLog.discipline)
    )
    totals: dict = {}
    disciplines: dict = {}
    for day, discipline, minutes in result.all():
        totals[day] = totals.get(day, 0) + minutes
        disciplines.setdefault(day, set()).add(discipline)

    rest_result = await db.execute(
        select(PracticeLog.practiced_on).where(
            PracticeLog.user_id == user_id,
            PracticeLog.practiced_on >= start,
            PracticeLog.is_rest_day.is_(True),
        )
    )
    rest_days = set(rest_result.scalars().all())

    # UTC'nin önündeki dilimlerden "yarın" tarihli kayıt gelebilir;
    # veri olan günler bugünden ilerideyse grid onları da kapsasın
    grid_end = max([today, *totals.keys(), *rest_days])

    weeks = []
    week_start = start
    while week_start <= grid_end:
        week = []
        for i in range(7):
            day = week_start + timedelta(days=i)
            minutes = totals.get(day, 0)
            if day in rest_days:
                level = "rest"
            elif minutes == 0:
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
    from app.constants import public_user_clause
    from app.models import User

    today = datetime.now(UTC).date()
    week_start = today - timedelta(days=today.weekday())
    result = await db.execute(
        select(PracticeLog.discipline, User, func.sum(PracticeLog.minutes).label("m"))
        .join(User, PracticeLog.user_id == User.id)
        .where(
            PracticeLog.practiced_on >= week_start,
            PracticeLog.is_rest_day.is_(False),
            public_user_clause(),
        )
        .group_by(PracticeLog.discipline, User.id)
        .order_by(func.sum(PracticeLog.minutes).desc())
    )
    leaders: dict[str, dict] = {}
    for discipline, person, minutes in result.all():
        if discipline not in leaders:
            leaders[discipline] = {"discipline": discipline, "person": person, "minutes": minutes}
    return sorted(leaders.values(), key=lambda x: -x["minutes"])


def completed_new_day_today(completed_days) -> bool:
    """Program takvim kilidi: bugün (PracticeLog ile aynı UTC "bugün") yeni bir gün
    tamamlandıysa sıradaki gün yarın açılır. Aynı takvim gününde en çok 1 yeni gün."""
    today = datetime.now(UTC).date()
    return any(d.completed_at is not None and d.completed_at.astimezone(UTC).date() == today for d in completed_days)
