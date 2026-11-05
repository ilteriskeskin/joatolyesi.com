"""B-03 (b): demo hesaplar kamuya açık yerlerde görünmez; blog yazıları "Joryu Ekibi" ile gösterilir."""

import secrets
import uuid
from datetime import date

import httpx
import pytest

from app.constants import DEMO_EMAIL_SUFFIX, is_demo_user



@pytest.fixture()
async def client(migrated_db):
    from app.main import app

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


_SEEDED_TAGS: list[str] = []


@pytest.fixture(autouse=True)
async def _cleanup_seeded(migrated_db):
    """Test DB koşular arası kalıcı: bu dosyanın seed ettiği kullanıcıları (ve FK
    CASCADE ile practice_logs/posts/follows satırlarını) test sonunda sil. Aksi halde
    önceki koşuların 99999 dk'lık "real" kayıtları weekly_leaders'ı doldurur ve
    minutes (int32) birikerek taşar."""
    _SEEDED_TAGS.clear()
    yield
    if not _SEEDED_TAGS:
        return
    from sqlalchemy import delete

    from app.db import async_session
    from app.models import User

    emails = []
    for t in _SEEDED_TAGS:
        emails += [f"demo{t}{DEMO_EMAIL_SUFFIX}", f"real{t}@test.com", f"other{t}@test.com"]
    async with async_session() as db:
        await db.execute(delete(User).where(User.email.in_(emails)))
        await db.commit()


def test_is_demo_user_helper():
    class U:
        def __init__(self, email):
            self.email = email

    assert is_demo_user(U(f"x{DEMO_EMAIL_SUFFIX}"))
    assert is_demo_user(U(f"X{DEMO_EMAIL_SUFFIX.upper()}"))
    assert not is_demo_user(U("real@test.com"))


async def _seed(tag):
    from app.db import async_session
    from app.models import Post, PracticeLog, User

    _SEEDED_TAGS.append(tag)

    def mk(name, email, public=True):
        return User(id=uuid.uuid4(), email=email, password_hash="x", referral_code=secrets.token_hex(5),
                    username=name, display_name=f"Ad {name}", discipline="bokken", is_public=public)

    # Demo: is_public=True (eski prod satırları gibi) -> yine de gizli olmalı
    demo = mk(f"demo{tag}", f"demo{tag}{DEMO_EMAIL_SUFFIX}")
    real = mk(f"real{tag}", f"real{tag}@test.com")
    async with async_session() as db:
        db.add_all([demo, real])
        await db.flush()
        today = date.today()
        db.add_all([
            PracticeLog(user_id=demo.id, practiced_on=today, discipline="bokken", minutes=999999),
            PracticeLog(user_id=real.id, practiced_on=today, discipline="bokken", minutes=99999),
        ])
        db.add_all([
            Post(user_id=demo.id, slug=f"demo-yazi-{tag}", title=f"Demo yazısı {tag}",
                 body="Bokken suburi üzerine bir yazı. " * 10, discipline="bokken"),
            Post(user_id=real.id, slug=f"real-yazi-{tag}", title=f"Gercek yazı {tag}",
                 body="Bokken suburi üzerine bir yazı. " * 10, discipline="bokken"),
        ])
        await db.commit()
    return demo, real


@pytest.mark.asyncio
async def test_demo_hidden_from_public_surfaces(client):
    from app.db import async_session
    from app.stats import weekly_leaders

    tag = uuid.uuid4().hex[:8]
    demo, real = await _seed(tag)

    # /practitioners: liste + arama
    r = await client.get("/practitioners")
    assert f"/u/{demo.username}" not in r.text
    assert f"/u/{real.username}" in r.text  # karşı-test
    r = await client.get(f"/practitioners?q=demo{tag}")
    assert f"/u/{demo.username}" not in r.text and demo.display_name not in r.text
    r = await client.get(f"/practitioners?q=real{tag}")
    assert f"/u/{real.username}" in r.text

    # haftanın enleri: demo daha çok dakikaya sahip olsa da çıkmaz
    async with async_session() as db:
        leaders = await weekly_leaders(db)
    names = {x["person"].username for x in leaders}
    assert demo.username not in names
    assert real.username in names

    # public profil / card / avatar
    r = await client.get(f"/u/{demo.username}")
    assert demo.display_name not in r.text and demo.email not in r.text
    assert (await client.get(f"/u/{demo.username}/card.png")).status_code == 404
    assert (await client.get(f"/u/{demo.username}/avatar.png")).status_code == 404
    assert (await client.get(f"/u/{real.username}/avatar.png")).status_code == 200
    assert real.display_name in (await client.get(f"/u/{real.username}")).text


@pytest.mark.asyncio
async def test_demo_hidden_from_follow_lists_and_follow_post(client):
    from sqlalchemy import select

    from app.db import async_session
    from app.models import Follow

    tag = uuid.uuid4().hex[:8]
    demo, real = await _seed(tag)
    other_email = f"other{tag}@test.com"
    # Gerçek kullanıcı demo'yu takip ediyor + demo gerçeği takip ediyor (eski sahte satırlar)
    async with async_session() as db:
        db.add_all([Follow(follower_id=real.id, followee_id=demo.id),
                    Follow(follower_id=demo.id, followee_id=real.id)])
        await db.commit()
    r = await client.get(f"/u/{real.username}")
    assert r.status_code == 200
    assert demo.username not in r.text and demo.display_name not in r.text
    assert other_email not in r.text

    # Takip POST'u: giriş + CSRF gerekir; giriş yapmış gerçek kullanıcı demo'yu takip edemez
    import re
    page = await client.get("/register")
    token = re.search(r'name="csrf_token" value="([^"]+)"', page.text).group(1)
    uname = f"v{tag}"
    await client.post("/register", data={"email": other_email, "password": "password123",
                                         "username": uname, "discipline": "aikijo", "csrf_token": token})
    page = await client.get("/practitioners")
    token = re.search(r'name="csrf_token" value="([^"]+)"', page.text) or re.search(
        r'name="csrf_token" value="([^"]+)"', (await client.get("/app")).text)
    r = await client.post(f"/u/{demo.username}/follow", data={"csrf_token": token.group(1)})
    assert r.status_code == 303
    async with async_session() as db:
        rows = (await db.execute(select(Follow).where(Follow.followee_id == demo.id))).scalars().all()
    assert all(f.follower_id == real.id for f in rows)  # yeni takip oluşmadı


@pytest.mark.asyncio
async def test_blog_shows_team_author_for_demo_posts(client):
    tag = uuid.uuid4().hex[:8]
    demo, real = await _seed(tag)

    r = await client.get("/blog?lang=tr&q=" + tag)
    assert f"Demo yazısı {tag}" in r.text
    assert "Joryu Ekibi" in r.text
    assert demo.display_name not in r.text and demo.username not in r.text
    # gerçek yazar eskisi gibi
    assert real.display_name in r.text
    assert f"/u/{real.username}/avatar.png" in r.text

    r = await client.get(f"/blog/demo-yazi-{tag}?lang=tr")
    assert r.status_code == 200
    assert "Joryu Ekibi" in r.text
    assert demo.display_name not in r.text and demo.username not in r.text
    assert f"/u/{demo.username}" not in r.text

    r = await client.get(f"/blog/demo-yazi-{tag}?lang=en")
    assert "Joryu Team" in r.text

    r = await client.get(f"/blog/real-yazi-{tag}?lang=tr")
    assert real.display_name in r.text
    assert f'href="/u/{real.username}"' in r.text
    assert "Joryu Ekibi" not in r.text
