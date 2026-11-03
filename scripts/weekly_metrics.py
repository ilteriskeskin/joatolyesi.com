"""Haftalık ürün metrikleri (salt okuma) — docs/team/METRICS.md için.

Kuzey yıldızı (haftalık aktif pratisyen) GA4'te ölçülemez; kaynak DB.
Çıktı: METRICS.md haftalık tablosuna yapıştırılabilir bir Markdown satırı
+ altında okunur bir özet. GA sütunları burada doldurulamaz, "—" kalır.

Çalıştırma:
    docker compose exec app python scripts/weekly_metrics.py [--week-start YYYY-MM-DD]

Varsayılan hafta: son tamamlanan Pazartesi-Pazar (UTC; weekly_leaders() ve
send_weekly_digest.py ile aynı tanım). --week-start bir Pazartesi olmalı.

Kısıtlar: yalnız COUNT/DISTINCT agregasyonları, satırlar belleğe çekilmez,
transaction READ ONLY açılır (yazma sorgusu yok). Kişisel veri yazdırılmaz.
Planlı dinlenme günleri (is_rest_day) pratik sayılmaz.
"""

import argparse
import asyncio
from datetime import UTC, date, datetime, time, timedelta

from sqlalchemy import Date, and_, cast, exists, func, not_, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import OWNER_EMAIL
from app.db import async_session
from app.models import PracticeLog, User

# scripts/seed_blog.py'nin oluşturduğu demo hesapların e-posta soneki
DEMO_EMAIL_SUFFIX = "@demo.joatolyesi.com"


def demo_user_clause():
    return func.lower(User.email).like(f"%{DEMO_EMAIL_SUFFIX}")


def owner_user_clause():
    return func.lower(User.email) == OWNER_EMAIL.lower()


def excluded_user_clause():
    """Hariç tutma kuralının tek yeri: demo hesaplar + sahip hesabı."""
    return or_(demo_user_clause(), owner_user_clause())


def _real_practice():
    """Gerçek pratik kaydı: dinlenme günü değil."""
    return PracticeLog.is_rest_day.is_(False)


def _utc_start(day: date) -> datetime:
    return datetime.combine(day, time.min, tzinfo=UTC)


def last_completed_week_start(today: date) -> date:
    return today - timedelta(days=today.weekday()) - timedelta(days=7)


async def compute_weekly_metrics(db: AsyncSession, week_start: date) -> dict:
    """week_start (Pazartesi) → week_start+6 (Pazar) penceresi için metrikler."""
    week_end = week_start + timedelta(days=6)
    start_ts, end_ts = _utc_start(week_start), _utc_start(week_end + timedelta(days=1))
    included = not_(excluded_user_clause())

    async def scalar(stmt) -> int:
        return int((await db.execute(stmt)).scalar_one() or 0)

    active = await scalar(
        select(func.count(func.distinct(PracticeLog.user_id)))
        .join(User, PracticeLog.user_id == User.id)
        .where(included, _real_practice(), PracticeLog.practiced_on.between(week_start, week_end))
    )

    signed_up_this_week = and_(included, User.created_at >= start_ts, User.created_at < end_ts)
    new_signups = await scalar(select(func.count(User.id)).where(signed_up_this_week))

    has_any_log = exists().where(PracticeLog.user_id == User.id, _real_practice())
    converted = await scalar(select(func.count(User.id)).where(signed_up_this_week, has_any_log))
    # 24 saat: kaydın oluşturulma anına bakılır (practiced_on geriye tarihli olabilir)
    has_log_24h = exists().where(
        PracticeLog.user_id == User.id,
        _real_practice(),
        PracticeLog.created_at <= User.created_at + timedelta(hours=24),
    )
    converted_24h = await scalar(select(func.count(User.id)).where(signed_up_this_week, has_log_24h))

    # 7. gün geri dönüş: hafta başından 7-13 gün önce kayıt olan kohort;
    # kayıt gününden sonraki 7.-13. günlerde ≥1 pratik
    signup_day = cast(func.timezone("UTC", User.created_at), Date)
    in_cohort = and_(
        included,
        signup_day.between(week_start - timedelta(days=13), week_start - timedelta(days=7)),
    )
    cohort = await scalar(select(func.count(User.id)).where(in_cohort))
    returned_d7 = await scalar(
        select(func.count(User.id)).where(
            in_cohort,
            exists().where(
                PracticeLog.user_id == User.id,
                _real_practice(),
                PracticeLog.practiced_on.between(signup_day + 7, signup_day + 13),
            ),
        )
    )

    total_users = await scalar(select(func.count(User.id)).where(included, User.created_at < end_ts))
    total_logs = await scalar(
        select(func.count(PracticeLog.id))
        .join(User, PracticeLog.user_id == User.id)
        .where(included, _real_practice(), PracticeLog.practiced_on <= week_end)
    )

    excluded_demo = await scalar(select(func.count(User.id)).where(demo_user_clause()))
    excluded_owner = await scalar(select(func.count(User.id)).where(owner_user_clause()))

    return {
        "week_start": week_start,
        "week_end": week_end,
        "weekly_active_practitioners": active,
        "new_signups": new_signups,
        "signup_to_first_session": converted,
        "signup_to_first_session_24h": converted_24h,
        "d7_cohort": cohort,
        "d7_returned": returned_d7,
        "total_users": total_users,
        "total_practice_logs": total_logs,
        "excluded_demo": excluded_demo,
        "excluded_owner": excluded_owner,
    }


def ratio(part: int, whole: int) -> str:
    """Payda 0 ise oran uydurulmaz: "n=0"."""
    if whole == 0:
        return "n=0"
    return f"{part}/{whole} (%{round(100 * part / whole)})"


def markdown_row(m: dict) -> str:
    # Sütun sırası METRICS.md tablosuyla birebir aynı:
    # Hafta | GA aktif kull. (28g) | Yeni kull. | Ort. etkileşim | Google organik oturum |
    # Instagram oturum | Yeni kayıt | Haftalık aktif pratisyen | Not
    note = (
        f"İlk seans {ratio(m['signup_to_first_session'], m['new_signups'])}, "
        f"24s içinde {ratio(m['signup_to_first_session_24h'], m['new_signups'])}; "
        f"D7 {ratio(m['d7_returned'], m['d7_cohort'])}. "
        f"Demo ({m['excluded_demo']}) + sahip hesabı hariç."
    )
    cells = [
        m["week_start"].isoformat(), "—", "—", "—", "—", "—",
        str(m["new_signups"]), str(m["weekly_active_practitioners"]), note,
    ]
    return "| " + " | ".join(cells) + " |"


def summary_block(m: dict) -> str:
    owner_note = (
        "sahip hesabı dahil edilmedi"
        if m["excluded_owner"]
        else "sahip hesabı DB'de bulunamadı"
    )
    lines = [
        f"Hafta: {m['week_start']} → {m['week_end']} (Pazartesi-Pazar, UTC)",
        f"- Haftalık aktif pratisyen: {m['weekly_active_practitioners']}",
        f"- Yeni kayıt: {m['new_signups']}",
        f"- Kayıttan ilk seansa: {ratio(m['signup_to_first_session'], m['new_signups'])}",
        f"- Kayıttan ilk 24 saatte seans: {ratio(m['signup_to_first_session_24h'], m['new_signups'])}",
        f"- 7. gün geri dönüş (kohort: hafta başından 7-13 gün önce kayıt): "
        f"{ratio(m['d7_returned'], m['d7_cohort'])}",
        f"- Toplam kullanıcı (hafta sonu itibarıyla): {m['total_users']}",
        f"- Toplam pratik kaydı (dinlenme günü hariç, hafta sonu itibarıyla): {m['total_practice_logs']}",
        f"- Hariç tutulan: {m['excluded_demo']} demo hesap + {m['excluded_owner']} sahip hesabı "
        f"({owner_note})",
        "- GA sütunları script tarafından doldurulamaz (—); GA4'ten elle eklenir.",
    ]
    return "\n".join(lines)


def parse_week_start(value: str | None, today: date) -> date:
    if value is None:
        return last_completed_week_start(today)
    week_start = date.fromisoformat(value)
    if week_start.weekday() != 0:
        raise SystemExit(f"--week-start bir Pazartesi olmalı: {value} ({week_start.strftime('%A')})")
    return week_start


async def main() -> None:
    parser = argparse.ArgumentParser(description="Haftalık ürün metrikleri (salt okuma)")
    parser.add_argument("--week-start", help="Haftanın Pazartesi'si, YYYY-MM-DD (varsayılan: son tamamlanan hafta)")
    args = parser.parse_args()
    week_start = parse_week_start(args.week_start, datetime.now(UTC).date())

    async with async_session() as db:
        # Savunma: bu oturumda yazma sorgusu çalışamaz
        await db.execute(text("SET TRANSACTION READ ONLY"))
        metrics = await compute_weekly_metrics(db, week_start)
        await db.rollback()

    print(markdown_row(metrics))
    print()
    print(summary_block(metrics))


if __name__ == "__main__":
    asyncio.run(main())
