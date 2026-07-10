"""Uçtan uca akış testleri — çalışan bir test Postgres'i gerektirir (conftest'e bak)."""

import re
import uuid
from datetime import date, timedelta

import httpx
import pytest
from sqlalchemy import select

pytestmark = pytest.mark.asyncio


@pytest.fixture()
async def client(migrated_db):
    from app.main import app

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def get_csrf(client, path):
    r = await client.get(path)
    return re.search(r'name="csrf_token" value="([^"]+)"', r.text).group(1)


async def register(client, email, username, password="password123"):
    token = await get_csrf(client, "/register")
    return await client.post(
        "/register",
        data={"email": email, "password": password, "username": username,
              "discipline": "aikijo", "csrf_token": token},
    )


def unique(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


async def test_register_login_and_csrf(client):
    email, username = f"{unique('u')}@test.com", unique("user")
    r = await register(client, email, username)
    assert r.status_code == 303

    # CSRF'siz POST reddedilir
    r = await client.post("/app/practice", data={"practiced_on": date.today().isoformat(),
                                                 "discipline": "aikijo", "minutes": "20"})
    assert r.status_code == 403

    # Dogru token ile pratik kaydı + streak
    token = await get_csrf(client, "/app")
    r = await client.post("/app/practice", data={"practiced_on": date.today().isoformat(),
                                                 "discipline": "aikijo", "minutes": "20",
                                                 "csrf_token": token})
    assert r.status_code == 200
    r = await client.get("/app")
    assert 'streak-number">1' in r.text


async def test_streak_consecutive_days(client):
    email, username = f"{unique('s')}@test.com", unique("streak")
    await register(client, email, username)
    token = await get_csrf(client, "/app")
    for i in range(5):
        day = (date.today() - timedelta(days=i)).isoformat()
        r = await client.post("/app/practice", data={"practiced_on": day, "discipline": "aikijo",
                                                     "minutes": "20", "csrf_token": token})
        assert r.status_code == 200
    r = await client.get("/app")
    assert 'streak-number">5' in r.text


async def test_password_reset_is_single_use(client):
    from app.db import async_session
    from app.models import User
    from app.security import create_reset_token

    email, username = f"{unique('r')}@test.com", unique("reset")
    await register(client, email, username)

    async with async_session() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        token = create_reset_token(user.id, user.password_hash)

    csrf = await get_csrf(client, f"/reset?token={token}")
    r = await client.post("/reset", data={"token": token, "password": "yeni-sifre-1", "csrf_token": csrf})
    assert r.status_code == 303
    # İkinci kullanım: parola değişti, token öldü
    r = await client.get(f"/reset?token={token}")
    assert "geçersiz" in r.text or "invalid" in r.text


async def test_password_change_drops_other_sessions(client, migrated_db):
    from app.main import app

    email, username = f"{unique('p')}@test.com", unique("pwch")
    await register(client, email, username)
    old_session = client.cookies.get("session")

    csrf = await get_csrf(client, "/profile")
    r = await client.post("/password", data={"current_password": "password123",
                                             "new_password": "yepyeni-sifre", "csrf_token": csrf})
    assert r.status_code == 303

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test",
                                 cookies={"session": old_session}) as old_client:
        r = await old_client.get("/app")
        assert r.status_code == 303  # login'e yönlenir


async def test_email_verification_flow(client):
    from app.db import async_session
    from app.models import User
    from app.security import create_verify_token

    email, username = f"{unique('v')}@test.com", unique("verify")
    await register(client, email, username)

    r = await client.get("/app")
    assert "verify-banner" in r.text  # doğrulanmamış: banner var

    async with async_session() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        token = create_verify_token(user.id)

    r = await client.get(f"/verify?token={token}")
    assert r.status_code == 303
    r = await client.get("/app")
    assert "verify-banner" not in r.text  # doğrulandı: banner gitti


async def test_account_delete_cascades(client):
    from app.db import async_session
    from app.models import PracticeLog, User

    email, username = f"{unique('d')}@test.com", unique("delete")
    await register(client, email, username)
    token = await get_csrf(client, "/app")
    await client.post("/app/practice", data={"practiced_on": date.today().isoformat(),
                                             "discipline": "aikijo", "minutes": "20",
                                             "csrf_token": token})

    async with async_session() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        user_id = user.id

    csrf = await get_csrf(client, "/profile")
    r = await client.post("/account/delete", data={"password": "password123", "csrf_token": csrf})
    assert r.status_code == 303

    async with async_session() as db:
        assert (await db.execute(select(User).where(User.id == user_id))).scalar_one_or_none() is None
        logs = (await db.execute(select(PracticeLog).where(PracticeLog.user_id == user_id))).scalars().all()
        assert logs == []


async def test_waitlist_duplicate_message(client):
    email = f"{unique('w')}@test.com"
    token = await get_csrf(client, "/")
    r1 = await client.post("/waitlist", data={"email": email, "lang": "tr", "csrf_token": token})
    r2 = await client.post("/waitlist", data={"email": email, "lang": "tr", "csrf_token": token})
    assert "Listedesin" in r1.text
    assert "zaten listede" in r2.text


async def test_guide_public_and_complete(client):
    # Rehber giriş istemez
    r = await client.get("/guide")
    assert r.status_code == 200
    # DISCIPLINES'taki her rehberli branş açılıyor ve iki bölümü de var
    from app.guide_content import GUIDE
    for d in GUIDE:
        r = await client.get(f"/guide/{d}")
        assert r.status_code == 200, d
        assert "guide-techlist" in r.text, d
        if GUIDE[d]["kata"]:
            assert "Kata" in r.text, d
    r = await client.get("/guide/olmayan-brans")
    assert "404" in r.text or r.status_code == 200  # 404 sablonu


async def test_kata_quick_log_and_weekly_card(client):
    email, username = f"{unique('k')}@test.com", unique("kata")
    await register(client, email, username)
    r = await client.get("/app")
    assert "week-card" in r.text  # haftalık özet kartı

    # seed'lenmiş ücretsiz bir kata bul
    from app.db import async_session
    from app.models import Kata
    async with async_session() as db:
        kata = (await db.execute(select(Kata).where(Kata.is_free))).scalars().first()
    if kata is None:
        pytest.skip("seed içerik yok")
    token = await get_csrf(client, f"/kata/{kata.slug}")
    r = await client.post(f"/kata/{kata.slug}/log", data={"minutes": "25", "csrf_token": token})
    assert r.status_code == 303
    r = await client.get(f"/kata/{kata.slug}?logged=1")
    assert "form-message--success" in r.text
    r = await client.get("/app")
    assert 'streak-number">1' in r.text
