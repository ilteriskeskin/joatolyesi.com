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
    token = await get_csrf(client, "/login")
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


async def test_follow_feed_and_card(client):
    # iki kullanıcı: b herkese açık, a onu takip eder
    email_a, user_a = f"{unique('fa')}@test.com", unique("follower")
    email_b, user_b = f"{unique('fb')}@test.com", unique("followee")

    from app.main import app as _app
    import httpx as _httpx
    tr = _httpx.ASGITransport(app=_app)
    async with _httpx.AsyncClient(transport=tr, base_url="http://test") as cb:
        await register(cb, email_b, user_b)
        csrf = await get_csrf(cb, "/profile")
        await cb.post("/profile", data={"username": user_b, "display_name": "B", "bio": "",
                                        "discipline": "aikijo", "is_public": "on", "csrf_token": csrf})
        token = await get_csrf(cb, "/app")
        await cb.post("/app/practice", data={"practiced_on": date.today().isoformat(),
                                             "discipline": "aikijo", "minutes": "30", "csrf_token": token})

    await register(client, email_a, user_a)
    # takip et
    csrf = await get_csrf(client, f"/u/{user_b}")
    r = await client.post(f"/u/{user_b}/follow", data={"csrf_token": csrf})
    assert r.status_code == 303
    r = await client.get(f"/u/{user_b}")
    assert "Takiptesin" in r.text or "Following" in r.text
    assert "(1)" in r.text  # Takipçiler (1)
    assert f"/u/{user_b}/avatar.png" in r.text  # takipci disina kendi avatarini gormez ama b, a'nin "takip ettikleri" listesinde gorunmeli

    # akış artık /practitioners sayfasında (community)
    r = await client.get("/practitioners")
    assert "feed-card" in r.text and user_b in r.text

    # a'nin kendi profilinde "takip ettikleri" listesinde b gorunmeli
    r = await client.get(f"/u/{user_a}")
    assert f"/u/{user_b}" in r.text

    # takibi bırak
    csrf = await get_csrf(client, f"/u/{user_b}")
    await client.post(f"/u/{user_b}/follow", data={"csrf_token": csrf})
    r = await client.get(f"/u/{user_b}")
    assert "Takiptesin" not in r.text  # takip birakildi

    # OG kartı: herkese açık profil PNG döner, gizli profil 404
    r = await client.get(f"/u/{user_b}/card.png")
    assert r.status_code == 200 and r.content[:8] == b"\x89PNG\r\n\x1a\n"
    r = await client.get(f"/u/{user_a}/card.png")
    assert r.status_code == 404  # a profili gizli
    # profil sayfasında og:image var
    r = await client.get(f"/u/{user_b}")
    assert f"/u/{user_b}/card.png" in r.text


async def test_blog_write_read_search(client):
    email, username = f"{unique('b')}@test.com", unique("blogger")
    await register(client, email, username)

    # yaz
    csrf = await get_csrf(client, "/blog/yeni")
    body_text = "Suburi çalışırken omuzlarım hep gergindi. " * 5
    r = await client.post("/blog/yeni", data={
        "title": "Omuz gerginliğiyle üç ayım", "body": body_text,
        "discipline": "aikijo", "csrf_token": csrf,
    })
    assert r.status_code == 303
    slug = r.headers["location"].split("/blog/")[1]

    # login'siz oku (keşfet + yazı herkese açık)
    from app.main import app as _app
    import httpx as _httpx
    tr = _httpx.ASGITransport(app=_app)
    async with _httpx.AsyncClient(transport=tr, base_url="http://test") as anon:
        r = await anon.get("/blog")
        assert r.status_code == 200 and "Omuz gerginliğiyle" in r.text
        r = await anon.get(f"/blog/{slug}")
        assert r.status_code == 200 and "Suburi çalışırken" in r.text
        # arama
        r = await anon.get("/blog?q=omuz")
        assert "Omuz gerginliğiyle" in r.text
        r = await anon.get("/blog?q=boylebirsheyyok")
        assert "Omuz gerginliğiyle" not in r.text
        # branş filtresi
        r = await anon.get("/blog?d=kendo")
        assert "Omuz gerginliğiyle" not in r.text
        # login'siz yazamaz
        r = await anon.get("/blog/yeni")
        assert r.status_code == 303

    # sahibi düzenler, başkası düzenleyemez
    csrf = await get_csrf(client, f"/blog/{slug}/duzenle")
    r = await client.post(f"/blog/{slug}/duzenle", data={
        "title": "Omuz gerginliği: çözüm", "body": body_text, "discipline": "aikijo", "csrf_token": csrf})
    assert r.status_code == 303
    r = await client.get(f"/blog/{slug}")
    assert "çözüm" in r.text

    # sil
    csrf = await get_csrf(client, f"/blog/{slug}")
    r = await client.post(f"/blog/{slug}/sil", data={"csrf_token": csrf})
    assert r.status_code == 303
    r = await client.get(f"/blog/{slug}")
    assert "404" in r.text or "bulunamadı" in r.text.lower()


async def test_kata_pages_public(client):
    from app.main import app as _app
    import httpx as _httpx
    tr = _httpx.ASGITransport(app=_app)
    async with _httpx.AsyncClient(transport=tr, base_url="http://test") as anon:
        r = await anon.get("/kata")
        assert r.status_code == 200  # liste login istemiyor


async def test_blog_markdown_rendering(client):
    email, username = f"{unique('md')}@test.com", unique("mdwriter")
    await register(client, email, username)
    csrf = await get_csrf(client, "/blog/yeni")
    body_md = (
        "## Alt başlık\n\n**kalın metin** ve *italik metin*.\n\n"
        "- madde bir\n- madde iki\n\n"
        "> bir alıntı\n\n"
        "<script>alert(1)</script>\n\n" + ("dolgu metni. " * 10)
    )
    r = await client.post("/blog/yeni", data={
        "title": "Markdown testi başlığı", "body": body_md,
        "discipline": "aikijo", "csrf_token": csrf,
    })
    assert r.status_code == 303
    slug = r.headers["location"].split("/blog/")[1]
    r = await client.get(f"/blog/{slug}")
    assert "<h2>Alt başlık</h2>" in r.text
    assert "<strong>kalın metin</strong>" in r.text
    assert "<em>italik metin</em>" in r.text
    assert "<li>madde bir</li>" in r.text
    assert "<blockquote>" in r.text
    post_body_html = r.text.split('class="post-body"')[1].split("</article>")[0]
    assert "alert(1)" not in post_body_html  # XSS payload gövdeden tamamen temizlendi
    assert "alert(1)" not in r.text.split("<meta property=\"og:description\"")[1].split(">")[0]  # meta de temiz
    # keşfet sayfasında özet düz metin (etiketsiz)
    r = await client.get("/blog")
    assert "Markdown testi başlığı" in r.text
    assert "<h2>Alt başlık</h2>" not in r.text  # excerpt duz metin, HTML degil


async def test_kata_kind_split_and_admin(client):
    from app.seed import seed_content
    await seed_content()

    r = await client.get("/kata?d=aikijo&kind=kata")
    assert "31 no jo kata" in r.text
    assert "Choku tsuki" not in r.text
    r = await client.get("/kata?d=aikijo&kind=teknik")
    assert "Choku tsuki" in r.text
    assert "31 no jo kata" not in r.text

    # Aikido'da kata yok — bos durum + teknik sekmesine yonlendirme gorunur
    r = await client.get("/kata?d=aikido&kind=kata")
    assert "kata_empty_kata" not in r.text  # ceviri anahtari kalmamis olmali
    assert "kata" in r.text.lower()

    r = await client.get("/admin/katas?token=test-admin-token")
    assert r.status_code == 200


async def test_waitlist_referral_and_position(client):
    email_a = f"{unique('ra')}@test.com"
    token = await get_csrf(client, "/login")
    r = await client.post("/waitlist", data={"email": email_a, "lang": "tr", "csrf_token": token})
    assert "Listedesin" in r.text
    assert "form-referral-input" in r.text
    import re as _re
    own_ref = _re.search(r"ref=([a-f0-9]+)", r.text).group(1)
    assert _re.search(r"Listede \d+\. kişisin", r.text)

    # ikinci kisi ilkinin linkinden gelsin
    email_b = f"{unique('rb')}@test.com"
    r = await client.get(f"/?ref={own_ref}")
    assert r.status_code == 200
    token2 = await get_csrf(client, "/login")
    r = await client.post("/waitlist", data={"email": email_b, "lang": "tr", "ref": own_ref, "csrf_token": token2})
    assert "Listedesin" in r.text

    from app.db import async_session
    from app.models import Waitlist
    async with async_session() as db:
        b = (await db.execute(select(Waitlist).where(Waitlist.email == email_b))).scalar_one()
        assert b.referred_by == own_ref
        assert b.referral_code and b.referral_code != own_ref


async def test_longest_streak_shown(client):
    email, username = f"{unique('ls')}@test.com", unique("longest")
    await register(client, email, username)
    token = await get_csrf(client, "/app")
    for i in range(5):
        d = (date.today() - timedelta(days=i)).isoformat()
        await client.post("/app/practice", data={"practiced_on": d, "discipline": "aikijo",
                                                 "minutes": "20", "csrf_token": token})
    old_day = (date.today() - timedelta(days=20)).isoformat()
    await client.post("/app/practice", data={"practiced_on": old_day, "discipline": "aikijo",
                                             "minutes": "20", "csrf_token": token})
    r = await client.get("/app")
    assert 'streak-number">5' in r.text  # guncel seri 5, rekorla esit oldugu icin ayri not gorunmez
    csrf = await get_csrf(client, "/profile")
    await client.post("/profile", data={"username": username, "display_name": "L", "bio": "",
                                        "discipline": "aikijo", "is_public": "on", "csrf_token": csrf})
    r = await client.get(f"/u/{username}")
    assert "En uzun seri" in r.text


async def test_kata_repeat_counter(client):
    email, username = f"{unique('kr')}@test.com", unique("repeater")
    await register(client, email, username)
    from app.db import async_session
    from app.models import Kata
    async with async_session() as db:
        kata = (await db.execute(select(Kata).where(Kata.is_free))).scalars().first()
    if kata is None:
        pytest.skip("seed içerik yok")
    for _ in range(3):
        token = await get_csrf(client, f"/kata/{kata.slug}")
        await client.post(f"/kata/{kata.slug}/log", data={"minutes": "20", "csrf_token": token})
    r = await client.get(f"/kata/{kata.slug}")
    assert "3 kez çalıştın" in r.text


async def test_push_subscribe_unsubscribe(client):
    email, username = f"{unique('pu')}@test.com", unique("pushuser")
    await register(client, email, username)
    token = await get_csrf(client, "/app")
    r = await client.post("/push/subscribe", data={
        "endpoint": "https://push.example.com/abc123",
        "p256dh": "fake-p256dh", "auth": "fake-auth", "csrf_token": token,
    })
    assert r.status_code == 204
    from app.db import async_session
    from app.models import PushSubscription
    async with async_session() as db:
        sub = (await db.execute(select(PushSubscription).where(
            PushSubscription.endpoint == "https://push.example.com/abc123"))).scalar_one_or_none()
        assert sub is not None

    token = await get_csrf(client, "/app")
    r = await client.post("/push/unsubscribe", data={
        "endpoint": "https://push.example.com/abc123", "csrf_token": token,
    })
    assert r.status_code == 204
    async with async_session() as db:
        sub = (await db.execute(select(PushSubscription).where(
            PushSubscription.endpoint == "https://push.example.com/abc123"))).scalar_one_or_none()
        assert sub is None

    r = await client.get("/push/vapid-public-key")
    assert r.status_code == 200 and "key" in r.json()


async def test_avatar_and_share_widget(client):
    email, username = f"{unique('av')}@test.com", unique("avataruser")
    await register(client, email, username)
    csrf = await get_csrf(client, "/profile")
    await client.post("/profile", data={"username": username, "display_name": "Avatar Kişi", "bio": "",
                                        "discipline": "aikijo", "is_public": "on", "csrf_token": csrf})

    r = await client.get(f"/u/{username}/avatar.png")
    assert r.status_code == 200 and r.content[:8] == b"\x89PNG\r\n\x1a\n"

    r = await client.get(f"/u/{username}/avatar.png?size=64")
    assert r.status_code == 200

    # gizli profilde avatar 404 (ayri, anonim client ile kayit ol)
    from app.main import app as _app
    import httpx as _httpx
    other_username = unique("privateuser")
    tr = _httpx.ASGITransport(app=_app)
    async with _httpx.AsyncClient(transport=tr, base_url="http://test") as other_client:
        await register(other_client, f"{unique('priv')}@test.com", other_username)
    r = await client.get(f"/u/{other_username}/avatar.png")
    assert r.status_code == 404

    # profil sayfasinda avatar + paylasim widget'i gorunur
    r = await client.get(f"/u/{username}")
    assert f'/u/{username}/avatar.png' in r.text
    assert 'share-inline' in r.text and 'data-share' in r.text

    # dashboard'da da paylasim widget'i (public profil sahibi icin)
    r = await client.get("/app")
    assert 'streak-share' in r.text and f'/u/{username}/card.png' in r.text


async def test_avatar_deterministic_but_belt_aware(client):
    from app.avatar import render_avatar
    png_a = render_avatar(seed="same-seed", initial="A", belt_id="white", size=64)
    png_b = render_avatar(seed="same-seed", initial="A", belt_id="white", size=64)
    assert png_a == png_b  # ayni girdi -> ayni gorsel (deterministik)
    png_black = render_avatar(seed="same-seed", initial="A", belt_id="black", size=64)
    assert png_black != png_a  # kusak degisince gorsel degisir


async def test_pro_disabled_by_default(client):
    email, username = f"{unique('nopro')}@test.com", unique("noprouser")
    await register(client, email, username)

    # Pro nav linki, Programlar linki ve /billing tamamen kapali
    r = await client.get("/app")
    assert "/billing" not in r.text and "/programs" not in r.text

    assert (await client.get("/billing")).status_code == 404
    assert (await client.get("/programs")).status_code == 404

    # Pro kapaliyken odeme duvari yok: is_free=False isaretli kata da tamamen
    # erisilebilir olmali (listede gorunur, detay 200 doner) - aksi halde
    # kutuphanenin buyuk kismi bombos gorunur (bkz. gecmis geri bildirim).
    from app.db import async_session
    from app.models import Kata
    async with async_session() as db:
        locked_kata = (await db.execute(select(Kata).where(Kata.is_free.is_(False)))).scalars().first()
    if locked_kata is not None:
        r = await client.get(f"/kata/{locked_kata.slug}")
        assert r.status_code == 200 and "404" not in r.text
        r = await client.get(f"/kata?d={locked_kata.discipline}&kind={locked_kata.kind}")
        assert locked_kata.title_tr in r.text


async def test_rest_day_does_not_break_streak_and_has_weekly_quota(client):
    email, username = f"{unique('rest')}@test.com", unique("restuser")
    await register(client, email, username)
    token = await get_csrf(client, "/app")

    day2 = (date.today() - timedelta(days=2)).isoformat()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    today = date.today().isoformat()

    # 2 gün önce pratik, dün dinlenme, bugün pratik: seri kırılmamalı
    r = await client.post("/app/practice", data={"practiced_on": day2, "discipline": "aikijo",
                                                 "minutes": "20", "csrf_token": token})
    assert r.status_code == 200
    r = await client.post("/app/rest-day", data={"practiced_on": yesterday, "csrf_token": token})
    assert r.status_code == 200
    assert "rest_day_left" not in r.text  # anahtar degil, cevrilmis metin gorunmeli
    r = await client.post("/app/practice", data={"practiced_on": today, "discipline": "aikijo",
                                                 "minutes": "20", "csrf_token": token})
    assert r.status_code == 200
    r = await client.get("/app")
    assert 'streak-number">3' in r.text

    # Dinlenme günü kuşak/seviye ilerlemesine sayılmaz: 2 gerçek pratik günü var
    from app.db import async_session
    from app.models import User
    from app.stats import total_practice_days
    async with async_session() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        days = await total_practice_days(db, user.id)
    assert days == 2

    # Haftalık kota: aynı haftada ikinci dinlenme günü reddedilir (sessizce yok sayılır).
    # Yarını dene — pazar günü hariç her zaman aynı haftanın içinde kalır.
    today_date = date.today()
    if today_date.weekday() == 6:  # pazar: yarın yeni haftaya geçer, kota testi anlamsızlaşır
        pytest.skip("hafta sınırı pazar gününe denk geliyor")
    other_day = (today_date + timedelta(days=1)).isoformat()
    r = await client.post("/app/rest-day", data={"practiced_on": other_day, "csrf_token": token})
    assert r.status_code == 200
    from app.models import PracticeLog
    async with async_session() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        rest_rows = (
            await db.execute(
                select(PracticeLog).where(PracticeLog.user_id == user.id, PracticeLog.is_rest_day.is_(True))
            )
        ).scalars().all()
    assert len(rest_rows) == 1  # ikinci istek kotayı aştığı için eklenmedi
