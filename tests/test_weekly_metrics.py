"""scripts/weekly_metrics.py testleri (B-02).

DB'li test çalışan bir test Postgres'i gerektirir (conftest'e bak). Test
verisi 2020'deki sabit bir haftaya yazılır ve sonda silinir; diğer testlerin
"bugün"e yazdığı kayıtlarla karışmaz. Bu, test fikstürüdür — seed değildir.
"""

import re
import secrets
import uuid
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest
from sqlalchemy import delete, select

from scripts.weekly_metrics import (
    DEMO_EMAIL_SUFFIX,
    compute_weekly_metrics,
    last_completed_week_start,
    markdown_row,
    parse_week_start,
    ratio,
)

WEEK = date(2020, 1, 6)  # Pazartesi


def at(day: date, hour: int = 10) -> datetime:
    return datetime(day.year, day.month, day.day, hour, tzinfo=UTC)


# --- Saf mantık ---


def test_ratio_does_not_invent_rate_for_empty_cohort():
    assert ratio(0, 0) == "n=0"
    assert ratio(1, 4) == "1/4 (%25)"


def test_week_start_defaults_to_last_completed_week():
    assert last_completed_week_start(date(2026, 11, 3)) == date(2026, 10, 26)  # Salı → önceki Pzt
    assert last_completed_week_start(date(2026, 11, 2)) == date(2026, 10, 26)  # Pzt → önceki Pzt
    assert parse_week_start("2026-10-26", date(2026, 11, 3)) == date(2026, 10, 26)
    with pytest.raises(SystemExit):
        parse_week_start("2026-10-27", date(2026, 11, 3))


def test_markdown_row_matches_metrics_table_columns():
    metrics_md = (Path(__file__).parent.parent / "docs/team/METRICS.md").read_text(encoding="utf-8")
    header = next(line for line in metrics_md.splitlines() if line.startswith("| Hafta |"))
    columns = [c.strip() for c in header.strip("|").split("|")]
    m = {
        "week_start": WEEK, "week_end": WEEK + timedelta(days=6),
        "weekly_active_practitioners": 7, "new_signups": 3,
        "signup_to_first_session": 2, "signup_to_first_session_24h": 1,
        "d7_cohort": 0, "d7_returned": 0, "total_users": 10, "total_practice_logs": 50,
        "excluded_demo": 7, "excluded_owner": 1,
    }
    row = markdown_row(m)
    cells = [c.strip() for c in row.strip("|").split("|")]
    assert len(cells) == len(columns) == 9
    by_col = dict(zip(columns, cells))
    assert by_col["Hafta"] == "2020-01-06"
    assert by_col["Yeni kayıt"] == "3"
    assert by_col["Haftalık aktif pratisyen"] == "7"
    for ga_col in columns[1:6]:
        assert by_col[ga_col] == "—"
    assert "D7 n=0" in by_col["Not"]


def test_script_has_no_write_queries():
    src = (Path(__file__).parent.parent / "scripts/weekly_metrics.py").read_text(encoding="utf-8")
    assert not re.search(r"\b(insert|update|delete|db\.add|commit)\s*\(", src, re.I)
    assert "SET TRANSACTION READ ONLY" in src


# --- DB ---


async def test_weekly_metrics_excludes_demo_and_owner(migrated_db):
    from app.constants import OWNER_EMAIL
    from app.db import async_session
    from app.models import PracticeLog, User

    tag = uuid.uuid4().hex[:8]
    created: list[uuid.UUID] = []

    def user(email: str, created_at: datetime) -> User:
        u = User(id=uuid.uuid4(), email=email, password_hash="x", referral_code=secrets.token_hex(5),
                 created_at=created_at)
        created.append(u.id)
        return u

    def log(u: User, day: date, logged_at: datetime | None = None, rest: bool = False) -> PracticeLog:
        return PracticeLog(user_id=u.id, practiced_on=day, discipline=None if rest else "aikijo",
                           minutes=None if rest else 20, is_rest_day=rest,
                           created_at=logged_at or at(day, 20))

    a = user(f"a-{tag}@test.com", at(WEEK + timedelta(days=1)))    # kayıt + 24s içinde seans
    b = user(f"b-{tag}@test.com", at(WEEK + timedelta(days=2)))    # kayıt + 4 gün sonra seans
    c = user(f"c-{tag}@test.com", at(WEEK + timedelta(days=3)))    # yalnız dinlenme günü
    demo = user(f"demo-{tag}{DEMO_EMAIL_SUFFIX}", at(WEEK + timedelta(days=1)))
    e = user(f"e-{tag}@test.com", at(WEEK - timedelta(days=12)))   # kohort, 8. gün döndü
    f = user(f"f-{tag}@test.com", at(WEEK - timedelta(days=13)))   # kohort, dönmedi
    g = user(f"g-{tag}@test.com", at(WEEK - timedelta(days=14)))   # kohort dışı

    async with async_session() as db:
        owner_exists = (await db.execute(select(User.id).where(User.email == OWNER_EMAIL))).first()
    if owner_exists is not None:
        pytest.skip("Test DB'de sahip hesabı zaten var; izolasyon için test atlandı")
    owner = user(OWNER_EMAIL, at(WEEK + timedelta(days=1)))

    async with async_session() as db:
        db.add_all([a, b, c, demo, e, f, g, owner])
        await db.flush()
        db.add_all([
            log(a, WEEK + timedelta(days=1), at(WEEK + timedelta(days=1), 12)),
            log(b, WEEK + timedelta(days=6)),
            log(c, WEEK + timedelta(days=4), rest=True),
            log(demo, WEEK + timedelta(days=2)),
            log(demo, WEEK + timedelta(days=3)),
            log(e, WEEK - timedelta(days=4)),        # kayıttan 8 gün sonra
            log(e, WEEK),                            # bu hafta da aktif
            log(f, WEEK - timedelta(days=12)),       # kayıttan 1 gün sonra (7-13 aralığı dışı)
            log(g, WEEK - timedelta(days=7)),        # kohort dışı
            log(owner, WEEK + timedelta(days=2)),
        ])
        await db.commit()

    try:
        async with async_session() as db:
            m = await compute_weekly_metrics(db, WEEK)
        assert m["weekly_active_practitioners"] == 3   # a, b, e — demo/sahip/dinlenme sayılmaz
        assert m["new_signups"] == 3                   # a, b, c — demo/sahip sayılmaz
        assert m["signup_to_first_session"] == 2       # a, b
        assert m["signup_to_first_session_24h"] == 1   # a
        assert m["d7_cohort"] == 2                     # e, f
        assert m["d7_returned"] == 1                   # e
        assert m["excluded_demo"] >= 1
        assert m["excluded_owner"] == 1
        row = markdown_row(m)
        assert "@" not in row and tag not in row       # kişisel veri yok
    finally:
        async with async_session() as db:
            await db.execute(delete(User).where(User.id.in_(created)))
            await db.commit()
