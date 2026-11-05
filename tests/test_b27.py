"""B-27: "2 günde 1" serisi, hatırlatmalar (rıza, tek tıkla çıkış, kişisel içerik), günün tekniği."""

import re
import uuid
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

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


def unique(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def utc_today():
    return datetime.now(UTC).date()


async def get_csrf(client, path):
    r = await client.get(path)
    return re.search(r'name="csrf_token" value="([^"]+)"', r.text).group(1)


async def signup(client, **extra):
    email, username = f"{unique('b27')}@test.com", unique("b27")
    client.cookies.clear()  # önceki testin oturumu kalmasın
    token = await get_csrf(client, "/register")
    data = {"email": email, "password": "password123", "username": username,
            "discipline": "aikijo", "csrf_token": token, **extra}
    r = await client.post("/register", data=data)
    assert r.status_code == 303
    return email


async def db_user(email):
    from app.db import async_session
    from app.models import User

    async with async_session() as db:
        return (await db.execute(select(User).where(User.email == email))).scalar_one()


async def add_logs(user_id, offsets):
    from app.db import async_session
    from app.models import PracticeLog

    async with async_session() as db:
        for off in offsets:
            db.add(PracticeLog(user_id=user_id, practiced_on=utc_today() - timedelta(days=off),
                               discipline="aikijo", minutes=20))
        await db.commit()


# --- Kayıt formu rızası ---


async def test_register_form_has_checked_reminder_checkbox(client):
    r = await client.get("/register")
    assert re.search(r'<input type="checkbox" name="reminders" checked>', r.text)
    assert "Günlük hatırlatma e-postası al" in r.text and "İstediğin zaman kapatabilirsin" in r.text
    assert "Get a daily reminder email" in (await client.get("/register?lang=en")).text


async def test_register_reminder_consent_values(client):
    on = await db_user(await signup(client, reminders="on", reminders_shown="1"))
    assert on.reminders_enabled is True
    off = await db_user(await signup(client, reminders_shown="1"))  # kutu kaldırıldı
    assert off.reminders_enabled is False
    legacy = await db_user(await signup(client))  # alan hiç yok (eski istemci): rıza yok
    assert legacy.reminders_enabled is False


# --- Tek tıkla çıkış ---


async def test_unsubscribe_get_confirms_post_disables(client):
    email = await signup(client, reminders="on", reminders_shown="1")
    user = await db_user(email)
    from app.security import create_unsub_token

    token = create_unsub_token(user.id)
    r = await client.get(f"/unsubscribe?t={token}")
    assert r.status_code == 200 and "Evet, kapat" in r.text
    assert (await db_user(email)).reminders_enabled is True  # GET hiçbir şeyi değiştirmez

    r = await client.post("/unsubscribe", data={"token": token})
    assert r.status_code == 200 and "kapatıldı" in r.text
    assert (await db_user(email)).reminders_enabled is False


async def test_unsubscribe_one_click_post_and_invalid_token(client):
    email = await signup(client, reminders="on", reminders_shown="1")
    user = await db_user(email)
    from app.security import create_unsub_token

    # RFC 8058: token URL'de, gövde "List-Unsubscribe=One-Click"
    r = await client.post(f"/unsubscribe?t={create_unsub_token(user.id)}",
                          content=b"List-Unsubscribe=One-Click",
                          headers={"content-type": "application/x-www-form-urlencoded"})
    assert r.status_code == 200
    assert (await db_user(email)).reminders_enabled is False

    other = await db_user(await signup(client, reminders="on", reminders_shown="1"))
    for bad in ("", "garbage", create_unsub_token(other.id)[:-3] + "xyz"):
        assert "geçersiz" in (await client.get(f"/unsubscribe?t={bad}")).text
        await client.post("/unsubscribe", data={"token": bad})
    assert (await db_user(other.email)).reminders_enabled is True


async def test_unsub_token_is_not_a_session_or_reset_token():
    from app.security import create_unsub_token, create_verify_token, read_reset_token, read_session_token, read_unsub_token

    uid = uuid.uuid4()
    assert read_unsub_token(create_unsub_token(uid)) == uid
    assert read_unsub_token(create_verify_token(uid)) is None
    assert read_session_token(create_unsub_token(uid)) is None
    assert read_reset_token(create_unsub_token(uid)) is None


async def test_send_email_passes_headers(monkeypatch):
    from app import mail

    sent = {}

    class FakeResp:
        status_code = 200
        text = ""

    class FakeClient:
        def __init__(self, *a, **k): ...
        async def __aenter__(self): return self
        async def __aexit__(self, *a): return False
        async def post(self, url, headers=None, json=None):
            sent.update(json)
            return FakeResp()

    monkeypatch.setattr(mail.settings, "resend_api_key", "re_test")
    monkeypatch.setattr(mail.httpx, "AsyncClient", FakeClient)
    await mail.send_email("a@b.c", "s", "<p>x</p>", headers={"List-Unsubscribe": "<https://x/u>"})
    assert sent["headers"] == {"List-Unsubscribe": "<https://x/u>"}
    sent.clear()
    await mail.send_email("a@b.c", "s", "<p>x</p>")
    assert "headers" not in sent


# --- Dashboard hatırlatma kartı ---


async def test_reminder_card_enable_and_dismiss(client):
    email = await signup(client)
    r = await client.get("/app")
    assert "reminder-card" in r.text and "Hatırlatma ister misin?" in r.text

    # [Şimdi değil]: çerezle 30 gün gizle, ayar değişmez
    csrf = await get_csrf(client, "/app")
    r = await client.post("/app/reminders/dismiss", data={"csrf_token": csrf})
    assert r.status_code == 303 and "rem_dismiss=1" in r.headers["set-cookie"] and "Max-Age=2592000" in r.headers["set-cookie"]
    assert "reminder-card" not in (await client.get("/app")).text
    assert (await db_user(email)).reminders_enabled is False

    # CSRF'siz POST reddedilir
    assert (await client.post("/app/reminders/enable", data={})).status_code == 403
    client.cookies.delete("rem_dismiss")
    r = await client.post("/app/reminders/enable", data={"csrf_token": csrf})
    assert r.status_code == 303
    assert (await db_user(email)).reminders_enabled is True
    assert "reminder-card" not in (await client.get("/app")).text


async def test_reminder_card_hidden_with_push_subscription_or_reminders_on(client):
    from app.db import async_session
    from app.models import PushSubscription

    await signup(client, reminders="on", reminders_shown="1")
    assert "reminder-card" not in (await client.get("/app")).text

    email = await signup(client)
    assert "reminder-card" in (await client.get("/app")).text
    user = await db_user(email)
    async with async_session() as db:
        db.add(PushSubscription(user_id=user.id, endpoint=f"https://push.example/{uuid.uuid4()}", p256dh="p", auth="a"))
        await db.commit()
    assert "reminder-card" not in (await client.get("/app")).text


async def test_reminder_card_sits_below_first_session_card(client):
    await signup(client)
    html = (await client.get("/app")).text
    assert html.index("first-session-card") < html.index('class="card reminder-card"') < html.index("streak-block")


# --- Seri metinleri ve uyarı ---


async def test_streak_label_hint_and_last_day_warning(client):
    email = await signup(client)
    user = await db_user(email)
    await add_logs(user.id, [2, 4, 6])  # 1,3,5. günler mantığı: son pratik önceki gün
    html = (await client.get("/app")).text
    assert 'streak-number">5' in html  # 6 gün önce..2 gün önce = 5 takvim günü
    assert ">Seri<" in html and "En az iki günde bir çalıştıkça serin sürer." in html
    # bu ay donma hakkı var: "serin biter" demek yanlış olur
    assert "Bugün çalışmazsan bu ayın donma hakkından biri kullanılır." in html
    assert "serin biter" not in html
    en = (await client.get("/app?lang=en")).text
    assert "Your streak keeps going as long as you practice at least every other day." in en
    assert "If you skip today, one of this month&#39;s streak freezes will be used." in en

    await add_logs(user.id, [1])  # dün çalıştı: uyarı kalkar
    assert "streak-warning" not in (await client.get("/app")).text


async def test_last_day_warning_without_freeze_says_streak_ends(client, monkeypatch):
    import app.stats as stats

    monkeypatch.setattr(stats, "FREEZES_PER_MONTH", 0)
    email = await signup(client)
    await add_logs((await db_user(email)).id, [2, 4])
    html = (await client.get("/app")).text
    assert "Bugün son gün: çalışmazsan serin biter." in html and "donma hakkından" not in html
    assert "Last day today: if you skip it, your streak ends." in (await client.get("/app?lang=en")).text


async def test_dashboard_order_with_practice_vs_first_session(client):
    from app.seed import seed_content

    await seed_content()  # taze DB'de katalog yoksa günün tekniği kartı çıkmaz
    email = await signup(client)
    new = (await client.get("/app")).text  # pratiği yok: ilk seans düzeni
    assert new.index("first-session-card") < new.index('class="card reminder-card"') < new.index("streak-block")
    await add_logs((await db_user(email)).id, [2])
    csrf = await get_csrf(client, "/app")
    await client.post("/programs/30-day-jo-suburi/enroll", data={"csrf_token": csrf})
    html = (await client.get("/app")).text
    assert "first-session-card" not in html
    # seri+uyarı -> program banner'ı -> günün tekniği -> hatırlatma kartı
    order = [html.index(x) for x in ("streak-block", "streak-warning", "program-banner", "daily-kata-card", 'class="card reminder-card"')]
    assert order == sorted(order)
    # program kartı (kayıtsız) da seriden sonra, günün tekniğinden önce
    other = await signup(client)
    await add_logs((await db_user(other)).id, [0])
    html = (await client.get("/app")).text
    order = [html.index(x) for x in ("streak-block", 'class="card program-card', "daily-kata-card", 'class="card reminder-card"')]
    assert order == sorted(order)


async def test_no_last_day_warning_when_practiced_today_or_new(client):
    assert "streak-warning" not in (await client.get("/app")).text  # girişsiz yönlenir, yine de uyarı yok
    email = await signup(client)
    assert "streak-warning" not in (await client.get("/app")).text
    await add_logs((await db_user(email)).id, [0, 2])
    assert "streak-warning" not in (await client.get("/app")).text


# --- Günün tekniği ---


def _kata(slug, discipline="aikijo", kind="teknik", video=None):
    return SimpleNamespace(slug=slug, discipline=discipline, kind=kind, video_url=video)


async def test_choose_daily_kata_rules():
    from app.daily import choose_daily_kata

    user = SimpleNamespace(id=uuid.uuid4(), discipline="aikijo")
    d = utc_today()
    katas = [_kata("a"), _kata("b", video="v"), _kata("c", video="v"), _kata("x", "bokken", video="v")]
    picks = {choose_daily_kata(katas, user, d + timedelta(days=i)).slug for i in range(40)}
    assert picks == {"b", "c"}  # videosu olanlar öncelikli, başka branş karışmaz
    assert choose_daily_kata(katas, user, d) is choose_daily_kata(list(reversed(katas)), user, d)  # deterministik
    # kullanıcıya göre farklılaşabilir
    others = {choose_daily_kata(katas, SimpleNamespace(id=uuid.uuid4(), discipline="aikijo"), d).slug for _ in range(30)}
    assert others == {"b", "c"}
    # branşta kata yoksa aikijo
    karate = SimpleNamespace(id=uuid.uuid4(), discipline="karate")
    assert choose_daily_kata(katas, karate, d).slug in {"b", "c"}
    # videosuzda önce teknik
    plain = [_kata("k1", kind="kata"), _kata("t1")]
    assert choose_daily_kata(plain, user, d).slug == "t1"
    assert choose_daily_kata([], user, d) is None


async def test_daily_kata_card_deterministic_with_video_and_quick_log(client):
    from app.seed import seed_content

    await seed_content()
    email = await signup(client)
    html = (await client.get("/app")).text
    assert "daily-kata-card" in html and "Günün tekniği" in html
    slug = re.search(r'hx-post="/kata/([a-z0-9-]+)/log"', html).group(1)
    assert re.search(r'hx-post="/kata/([a-z0-9-]+)/log"', (await client.get("/app")).text).group(1) == slug  # aynı gün aynı teknik
    assert 'href="/kata/' + slug + '"' in html
    assert "video-lazy" in html  # aikijo teknikleri videolu
    assert html.index("first-session-card") < html.index("daily-kata-card") < html.index("streak-block")

    csrf = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)
    r = await client.post(f"/kata/{slug}/log", data={"minutes": "10", "source": "daily_kata", "csrf_token": csrf},
                          headers={"HX-Request": "true"})
    assert r.status_code == 200 and "streak-number" in r.text and "Kaydedildi" in r.text
    assert "daily-kata-card" in r.text and f'hx-post="/kata/{slug}/log"' not in r.text
    assert "joryu:practice-logged" in r.headers["hx-trigger"] and "daily_kata" in r.headers["hx-trigger"]

    from app.db import async_session
    from app.models import PracticeLog

    user = await db_user(email)
    async with async_session() as db:
        log = (await db.execute(select(PracticeLog).where(PracticeLog.user_id == user.id))).scalar_one()
    assert log.kata_slug == slug and log.minutes == 10


async def test_daily_kata_query_budget(client):
    """Günün tekniği tek ek sorgu: kayıtlı kullanıcının dashboard'unda yalnız bir katas SELECT'i."""
    from sqlalchemy import event
    from app.db import engine
    from app.seed import seed_content

    await seed_content()
    await signup(client)
    statements = []

    def before(conn, cursor, statement, *a):
        statements.append(statement)

    event.listen(engine.sync_engine, "before_cursor_execute", before)
    try:
        await client.get("/app")
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", before)
    kata_selects = [s for s in statements if "FROM katas" in s]
    # ilk seans kartı kendi sorgusunu yapar (mevcut); günün tekniği tam 1 tane ekler
    assert len(kata_selects) == 2


async def test_aikijo_video_urls_seeded(client):
    from app.db import async_session
    from app.models import Kata
    from app.seed import AIKIJO_VIDEOS, seed_content

    await seed_content()
    async with async_session() as db:
        rows = {k.slug: k.video_url for k in (await db.execute(select(Kata).where(Kata.slug.in_(AIKIJO_VIDEOS)))).scalars()}
    assert len(AIKIJO_VIDEOS) == 11 and set(rows) == set(AIKIJO_VIDEOS)
    assert all(rows[s] == f"https://www.youtube.com/embed/{v}" for s, v in AIKIJO_VIDEOS.items())


# --- Hatırlatma maili içeriği ---


async def _reminder(email, lang="tr"):
    from app.db import async_session
    from app.models import User
    from app.reminders import build_reminder
    from app.stats import streak_info
    from sqlalchemy.orm import selectinload

    async with async_session() as db:
        user = (await db.execute(select(User).options(selectinload(User.subscription)).where(User.email == email))).scalar_one()
        user.lang = lang
        info = await streak_info(db, user.id)
        return await build_reminder(db, user, utc_today(), info)


async def test_reminder_technique_variant(client):
    email = await signup(client)
    for lang, word in (("tr", "Günün tekniği"), ("en", "Technique of the day")):
        rem = await _reminder(email, lang)
        assert rem["kind"] == "technique" and word in rem["subject"] and word in rem["html"]
        assert "/kata/" in rem["html"] and "/unsubscribe?t=" in rem["html"]
    assert "10 dk yeter" in (await _reminder(email, "tr"))["html"]


async def test_reminder_last_day_variant(client):
    email = await signup(client)
    await add_logs((await db_user(email)).id, [2, 3])
    rem = await _reminder(email, "tr")
    assert rem["kind"] == "last_day"
    assert "Bugün çalışmazsan bu ayın donma hakkından biri kullanılır." in rem["html"]
    assert "serin biter" not in rem["html"] and "Serin şu an 2 gün" in rem["html"]
    assert "one of this month's streak freezes" in (await _reminder(email, "en"))["html"]


async def test_reminder_last_day_variant_without_freeze(client, monkeypatch):
    import app.stats as stats

    monkeypatch.setattr(stats, "FREEZES_PER_MONTH", 0)
    email = await signup(client)
    await add_logs((await db_user(email)).id, [2, 3])
    rem = await _reminder(email, "tr")
    assert rem["kind"] == "last_day" and "Bugün son gün" in rem["html"] and "serin biter" in rem["html"]
    assert "donma" not in rem["html"]
    assert "Last day today" in (await _reminder(email, "en"))["html"]


async def test_reminder_program_variant(client):
    email = await signup(client)
    csrf = await get_csrf(client, "/programs/30-day-jo-suburi")
    r = await client.post("/programs/30-day-jo-suburi/enroll", data={"csrf_token": csrf})
    assert r.status_code == 303
    rem = await _reminder(email, "tr")
    assert rem["kind"] == "program"
    assert re.search(r"Bugün: <strong>Gün 1</strong> — Odak: \S", rem["html"])
    assert "/programs/30-day-jo-suburi/day/1" in rem["html"]
    en = await _reminder(email, "en")
    assert "Today: <strong>Day 1</strong> — Focus:" in en["html"]
    # bugün son gün + program: uyarı satırı eklenir
    await add_logs((await db_user(email)).id, [2])
    assert "donma hakkından biri kullanılır" in (await _reminder(email, "tr"))["html"]


async def _push(email, lang="tr"):
    from app.db import async_session
    from app.models import User
    from app.reminders import build_push
    from app.stats import streak_info
    from sqlalchemy.orm import selectinload

    async with async_session() as db:
        user = (await db.execute(select(User).options(selectinload(User.subscription)).where(User.email == email))).scalar_one()
        user.lang = lang
        return await build_push(db, user, utc_today(), await streak_info(db, user.id))


async def test_push_variants_never_mention_streak_count(client, monkeypatch):
    import app.stats as stats

    email = await signup(client)
    p = await _push(email, "tr")  # seri 0: seri cümlesi yok, günün tekniği
    assert p["kind"] == "technique" and p["body"].startswith("Günün tekniği:") and p["url"].startswith("/kata/")
    assert "seri" not in p["body"].lower() and "0 gün" not in p["body"]
    assert (await _push(email, "en"))["body"].startswith("Technique of the day:")

    # program günü
    csrf = await get_csrf(client, "/programs/30-day-jo-suburi")
    await client.post("/programs/30-day-jo-suburi/enroll", data={"csrf_token": csrf})
    p = await _push(email, "tr")
    assert p["kind"] == "program" and p["body"].startswith("Bugün: Gün 1 — Odak:") and p["url"].endswith("/day/1")
    assert (await _push(email, "en"))["body"].startswith("Today: Day 1 — Focus:")


async def test_push_last_day_both_branches(client, monkeypatch):
    import app.stats as stats

    email = await signup(client)
    await add_logs((await db_user(email)).id, [2, 3])
    p = await _push(email, "tr")
    assert p["kind"] == "last_day" and p["body"] == "Bugün çalışmazsan bu ayın donma hakkından biri kullanılır."
    assert (await _push(email, "en"))["body"] == "If you skip today, one of this month's streak freezes will be used."
    monkeypatch.setattr(stats, "FREEZES_PER_MONTH", 0)
    assert (await _push(email, "tr"))["body"] == "Bugün son gün: çalışmazsan serin biter."
    assert (await _push(email, "en"))["body"] == "Last day today: if you skip it, your streak ends."


# --- QA turu 1 düzeltmeleri ---


async def test_register_error_keeps_reminder_choice_and_links_privacy(client):
    page = (await client.get("/register")).text
    assert 'href="/privacy"' in page and "Ayrıntılar:" in page and "Gizlilik ve KVKK" in page
    client.cookies.clear()
    token = await get_csrf(client, "/register")
    base = {"email": "not-an-email", "password": "password123", "username": unique("e"),
            "discipline": "aikijo", "csrf_token": token, "reminders_shown": "1"}
    off = (await client.post("/register", data=base)).text  # kullanıcı kutuyu kaldırmıştı
    assert "form-message--error" in off
    assert not re.search(r'name="reminders"\s+checked', off)
    on = (await client.post("/register", data={**base, "reminders": "on"})).text
    assert re.search(r'name="reminders"\s+checked', on)


async def test_seed_video_only_fills_null_and_keeps_other_fields_upserting(client):
    from app.db import async_session
    from app.models import Kata
    from app.seed import AIKIJO_VIDEOS, seed_content

    await seed_content()
    custom = "https://www.youtube.com/embed/ADMINCUSTOM1"
    async with async_session() as db:
        a = (await db.execute(select(Kata).where(Kata.slug == "choku-tsuki"))).scalar_one()
        b = (await db.execute(select(Kata).where(Kata.slug == "kaeshi-tsuki"))).scalar_one()
        a.video_url = custom          # admin'den girilmiş
        b.video_url = None            # boş
        b.description_tr = "elle bozuldu"
        await db.commit()
    await seed_content()
    async with async_session() as db:
        a = (await db.execute(select(Kata).where(Kata.slug == "choku-tsuki"))).scalar_one()
        b = (await db.execute(select(Kata).where(Kata.slug == "kaeshi-tsuki"))).scalar_one()
        assert a.video_url == custom                                   # admin değeri ezilmedi
        assert b.video_url == f"https://www.youtube.com/embed/{AIKIJO_VIDEOS['kaeshi-tsuki']}"
        assert b.description_tr != "elle bozuldu"                      # diğer alanlar upsert'te yenilenir
        a.video_url = f"https://www.youtube.com/embed/{AIKIJO_VIDEOS['choku-tsuki']}"
        await db.commit()


async def test_reminder_html_escapes_title_and_focus(monkeypatch):
    import app.reminders as rem

    async def no_program(db, user):
        return None

    evil = SimpleNamespace(slug="x", title_tr="<script>alert(1)</script>", title_en="<b>t</b>")

    async def fake_pick(db, user, today):
        return evil

    monkeypatch.setattr(rem, "_open_program_day", no_program)
    monkeypatch.setattr(rem, "pick_daily_kata", fake_pick)
    user = SimpleNamespace(id=uuid.uuid4(), lang="tr")
    out = await rem.build_reminder(None, user, utc_today(), {"streak": 0, "last_day": False, "last_day_freeze": False})
    assert "<script>" not in out["html"] and "&lt;script&gt;" in out["html"]

    day = SimpleNamespace(title_tr="<i>odak</i>", title_en="<i>focus</i>")
    enrollment = SimpleNamespace(program=SimpleNamespace(slug="p"))

    async def program(db, user):
        return enrollment, day, 2

    monkeypatch.setattr(rem, "_open_program_day", program)
    out = await rem.build_reminder(None, user, utc_today(), {"streak": 0, "last_day": False, "last_day_freeze": False})
    assert "<i>odak</i>" not in out["html"] and "&lt;i&gt;odak&lt;/i&gt;" in out["html"]


def _load_script(name):
    import importlib.util
    from pathlib import Path

    path = Path(__file__).resolve().parent.parent / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"scripts_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fast_sleep(mod, monkeypatch):
    import asyncio

    real = asyncio.sleep

    async def quick(delay, *a):
        await real(0)

    monkeypatch.setattr(mod.asyncio, "sleep", quick)


async def test_send_reminders_survives_user_errors_with_pro_enabled(client, monkeypatch):
    """Bir kullanıcının hatası döngüyü kesmez; pro_enabled=True iken subscription lazy-load
    hatası (MissingGreenlet) yok; ölü push aboneliği silmesi commit'lenir."""
    from app.config import settings
    from app.db import async_session
    from app.models import PushSubscription

    mod = _load_script("send_reminders")
    _fast_sleep(mod, monkeypatch)
    monkeypatch.setattr(settings, "pro_enabled", True)

    good = await signup(client, reminders="on", reminders_shown="1")
    bad = await signup(client, reminders="on", reminders_shown="1")
    pusher = await signup(client)
    pusher_user = await db_user(pusher)
    dead = f"https://push.example/dead-{uuid.uuid4()}"
    boom = f"https://push.example/boom-{uuid.uuid4()}"
    async with async_session() as db:
        db.add_all([PushSubscription(user_id=pusher_user.id, endpoint=dead, p256dh="p", auth="a"),
                    PushSubscription(user_id=pusher_user.id, endpoint=boom, p256dh="p", auth="a")])
        await db.commit()

    sent, pushed = [], []

    async def fake_email(to, subject, html, headers=None):
        sent.append((to, headers))

    real_build = mod.build_reminder

    async def flaky_build(db, user, today, info):
        if user.email == bad:
            raise RuntimeError("kaboom")
        return await real_build(db, user, today, info)

    async def fake_push(sub_info, title, body, url="/app"):
        pushed.append((sub_info["endpoint"], body))
        if sub_info["endpoint"] == dead:
            return False
        if sub_info["endpoint"] == boom:
            raise RuntimeError("push patladı")
        return True

    monkeypatch.setattr(mod, "send_email", fake_email)
    monkeypatch.setattr(mod, "build_reminder", flaky_build)
    monkeypatch.setattr(mod, "send_push", fake_push)
    await mod.main()

    sent_to = {to: h for to, h in sent}
    assert good in sent_to and bad not in sent_to  # hatalı kullanıcı atlandı, döngü sürdü
    assert "List-Unsubscribe" in sent_to[good]
    assert any(e == dead for e, _ in pushed)
    async with async_session() as db:
        left = (await db.execute(select(PushSubscription.endpoint).where(PushSubscription.user_id == pusher_user.id))).scalars().all()
    assert dead not in left and boom in left  # ölü abonelik silindi ve commit'lendi


async def test_weekly_leader_mail_follows_reminders_flag_with_unsubscribe(client, monkeypatch):
    import time

    from app.db import async_session
    from app.models import PracticeLog, User

    mod = _load_script("send_weekly_digest")
    _fast_sleep(mod, monkeypatch)
    sent = []

    async def fake_email(to, subject, html, headers=None):
        sent.append((to, subject, html, headers))

    async def fake_push(*a, **k):
        return True

    monkeypatch.setattr(mod, "send_email", fake_email)
    monkeypatch.setattr(mod, "send_push", fake_push)

    email = await signup(client, reminders="on", reminders_shown="1")
    user = await db_user(email)
    monday = utc_today() - timedelta(days=utc_today().weekday())
    big = int(time.time())  # her koşuda öncekinden büyük: kesin haftanın birincisi
    async with async_session() as db:
        db.add_all([PracticeLog(user_id=user.id, practiced_on=monday - timedelta(days=3), discipline="aikijo", minutes=big),
                    PracticeLog(user_id=user.id, practiced_on=monday - timedelta(days=4), discipline="aikijo", minutes=5)])
        await db.commit()

    await mod.main()
    mine = [m for m in sent if m[0] == email and "birincisin" in m[1]]
    assert len(mine) == 1
    assert "/unsubscribe?t=" in mine[0][2] and "List-Unsubscribe" in mine[0][3]

    async with async_session() as db:
        u = (await db.execute(select(User).where(User.id == user.id))).scalar_one()
        u.reminders_enabled = False
        await db.commit()
    sent.clear()
    await mod.main()
    assert not [m for m in sent if m[0] == email]  # rıza kapalı: ne özet ne birincilik maili
