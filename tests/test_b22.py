"""B-22: program e-posta dizisi (enroll sonrası gün 1/3/7, "kaldığın yerden devam")."""

import re
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from tests.test_b27 import add_logs, client, db_user, get_csrf, signup, utc_today  # noqa: F401

pytestmark = pytest.mark.asyncio

SLUG = "30-day-jo-suburi"


async def enrolled(client, **extra):
    from app.seed import seed_content

    await seed_content()  # taze DB'de program yoksa enroll 404 döner
    email = await signup(client, **extra)
    csrf = await get_csrf(client, f"/programs/{SLUG}")
    assert (await client.post(f"/programs/{SLUG}/enroll", data={"csrf_token": csrf})).status_code == 303
    return email


async def set_age(email, days):
    """Enroll'u `days` gün öncesine al."""
    from app.db import async_session
    from app.models import Enrollment

    user = await db_user(email)
    async with async_session() as db:
        e = (await db.execute(select(Enrollment).where(Enrollment.user_id == user.id))).scalar_one()
        e.created_at = datetime.now(UTC) - timedelta(days=days)
        await db.commit()


async def complete_day_today(email):
    from app.db import async_session
    from app.models import Enrollment, EnrollmentDay

    user = await db_user(email)
    async with async_session() as db:
        e = (await db.execute(select(Enrollment).where(Enrollment.user_id == user.id))).scalar_one()
        db.add(EnrollmentDay(enrollment_id=e.id, day_number=1))
        await db.commit()


async def reminder(email, lang="tr"):
    from app.db import async_session
    from app.models import User
    from app.reminders import build_reminder
    from app.stats import streak_info
    from sqlalchemy.orm import selectinload

    async with async_session() as db:
        user = (await db.execute(select(User).options(selectinload(User.subscription)).where(User.email == email))).scalar_one()
        user.lang = lang
        return await build_reminder(db, user, utc_today(), await streak_info(db, user.id))


@pytest.mark.parametrize("age", [1, 3, 7])
async def test_comeback_mail_on_steps(client, age):
    email = await enrolled(client, reminders="on", reminders_shown="1")
    await set_age(email, age)
    rem = await reminder(email)
    assert rem["kind"] == "program_comeback" and rem["step"] == age
    assert re.search(r"Kaldığın yerden devam: <strong>Gün 1</strong> — Odak: \S", rem["html"])
    assert f"/programs/{SLUG}/day/1" in rem["html"] and "/unsubscribe?t=" in rem["html"]
    assert "Gün 1 seni bekliyor" in rem["subject"]
    assert "Pick up where you left off" in (await reminder(email, "en"))["html"]


@pytest.mark.parametrize("age", [0, 2, 4, 8])
async def test_normal_reminder_on_other_days(client, age):
    email = await enrolled(client, reminders="on", reminders_shown="1")
    await set_age(email, age)
    assert (await reminder(email))["kind"] == "program"


async def test_no_comeback_when_day_done_today(client):
    email = await enrolled(client, reminders="on", reminders_shown="1")
    await set_age(email, 3)
    await complete_day_today(email)
    assert (await reminder(email))["kind"] != "program_comeback"


async def test_comeback_idempotent_via_script(client, monkeypatch):
    import scripts.send_reminders as sr

    sent = []

    async def fake_send(to, subject, html, headers=None):
        sent.append((to, subject, headers))

    monkeypatch.setattr(sr, "send_email", fake_send)
    email = await enrolled(client, reminders="on", reminders_shown="1")
    await set_age(email, 3)
    user = await db_user(email)
    await sr._send_email_reminder(user.id, utc_today())
    assert len(sent) == 1 and "List-Unsubscribe" in sent[0][2] and "seni bekliyor" in sent[0][1]
    await sr._send_email_reminder(user.id, utc_today())  # aynı gün ikinci koşu
    assert len(sent) == 2 and "seni bekliyor" not in sent[1][1]  # dizi maili yok, normal hatırlatma


async def test_script_main_skips_reminders_off(client, monkeypatch):
    import scripts.send_reminders as sr

    sent = []

    async def fake_send(to, subject, html, headers=None):
        sent.append(to)

    async def no_sleep(_):
        pass

    monkeypatch.setattr(sr, "send_email", fake_send)
    monkeypatch.setattr(sr.asyncio, "sleep", no_sleep)
    off = await enrolled(client, reminders_shown="1")
    await set_age(off, 3)
    await sr.main()
    assert off not in sent


async def test_push_never_uses_comeback(client):
    from app.db import async_session
    from app.models import User
    from app.reminders import build_push
    from app.stats import streak_info
    from sqlalchemy.orm import selectinload

    email = await enrolled(client, reminders="on", reminders_shown="1")
    await set_age(email, 3)
    async with async_session() as db:
        user = (await db.execute(select(User).options(selectinload(User.subscription)).where(User.email == email))).scalar_one()
        push = await build_push(db, user, utc_today(), await streak_info(db, user.id))
    assert push["kind"] == "program"


async def test_day_page_shows_reminder_card_only_when_off(client):
    off = await enrolled(client, reminders_shown="1")
    html = (await client.get(f"/programs/{SLUG}/day/1")).text
    assert "reminder-card" in html and 'name="next" value="/programs/' in html
    csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)
    r = await client.post("/app/reminders/enable", data={"csrf_token": csrf, "next": f"/programs/{SLUG}/day/1"})
    assert r.status_code == 303 and r.headers["location"] == f"/programs/{SLUG}/day/1"
    assert (await db_user(off)).reminders_enabled is True
    assert "reminder-card" not in (await client.get(f"/programs/{SLUG}/day/1")).text
    r = await client.post("/app/reminders/dismiss", data={"csrf_token": csrf, "next": "//evil.com"})
    assert r.headers["location"] == "/app"
