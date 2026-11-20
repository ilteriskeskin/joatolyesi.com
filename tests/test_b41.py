"""B-41a: program dizini, bokken 30 gün programı, tek aktif program, seed düzeltmeleri."""

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from tests.test_b27 import client, db_user, get_csrf, signup  # noqa: F401


JO = "30-day-jo-suburi"
BOKKEN = "30-day-bokken-suburi"


async def seeded():
    from app.seed import seed_content

    await seed_content()


async def enroll(client, slug):
    csrf = await get_csrf(client, f"/programs/{slug}")
    return await client.post(f"/programs/{slug}/enroll", data={"csrf_token": csrf})


async def active_slug(email):
    from app.db import async_session
    from app.models import Enrollment

    user = await db_user(email)
    async with async_session() as db:
        rows = (
            await db.execute(
                select(Enrollment)
                .options(selectinload(Enrollment.program))
                .where(Enrollment.user_id == user.id)
                .order_by(Enrollment.activated_at.desc())
            )
        ).scalars().all()
        return [e.program.slug for e in rows] if rows else []


async def test_seed_is_idempotent_and_bokken_program_complete(client):
    from app.db import async_session
    from app.models import Program, ProgramDay

    await seeded()
    await seeded()
    async with async_session() as db:
        progs = (await db.execute(select(Program).where(Program.slug.in_([JO, BOKKEN])))).scalars().all()
        assert sorted(p.slug for p in progs) == sorted([JO, BOKKEN])  # çift satır yok
        bokken = next(p for p in progs if p.slug == BOKKEN)
        days = (
            await db.execute(select(ProgramDay).where(ProgramDay.program_id == bokken.id).order_by(ProgramDay.day_number))
        ).scalars().all()
    assert [d.day_number for d in days] == list(range(1, 31))
    assert "Bir ay boyunca her gün yapılandırılmış bokken suburi" in bokken.description_tr
    assert days[0].title_tr == "Odak: Duruş (migi hanmi) + ichi no suburi, yavaş"
    assert days[6].title_tr == "Tekrar günü (hafta 1)" and "Bugün tekrar günü" in days[6].content_tr
    assert days[28].content_tr.startswith("Hafta teması: Birleştirme: tüm seri.")
    # B-33: tavsiye dili, kumitachi yok
    assert "en az 10 tekrar önerilir" in days[1].content_tr and "önce ona danış" in days[1].content_tr
    assert "kumitachi" not in " ".join(d.content_tr.lower() + d.content_en.lower() for d in days)


async def test_seed_bokken_suburi_texts_corrected(client):
    from app.db import async_session
    from app.models import Kata

    await seeded()
    async with async_session() as db:
        k = {s.slug: s for s in (await db.execute(select(Kata).where(Kata.slug.like("aiki-ken-suburi-%")))).scalars()}
    assert "waki gamae" in k["aiki-ken-suburi-3"].description_tr and "gedan'a geri adımla" in k["aiki-ken-suburi-3"].description_tr
    assert k["aiki-ken-suburi-5"].description_tr == "İlerlerken sağa ve sola dönüşümlü, başın yanına yönelen çapraz kesişler."
    assert k["aiki-ken-suburi-6"].description_tr == "Her kesişin ardından tsuki; sağ ve sol tarafta dönüşümlü tekrarlanır."
    assert k["aiki-ken-suburi-7"].description_tr.startswith("Sağ duruşta kesiş, ardından öne adımla sol duruşta tsuki")
    for s in ("3", "5", "6", "7"):
        assert "savuşturma" not in k[f"aiki-ken-suburi-{s}"].description_tr.lower()


def test_seed_bokken_suburi_tr_matches_verified_doc():
    """Seed TR metinleri onaylı belgenin 4. bölümüyle birebir aynı (B-41a-2)."""
    import re
    from pathlib import Path

    from app.seed import BOKKEN

    doc = (Path(__file__).resolve().parent.parent
           / "docs/team/content/verified/2026-11-15-30-gun-bokken-programi.md").read_text(encoding="utf-8")
    section = doc.split("## 4. Suburi hareket açıklamaları", 1)[1].split("\n## ", 1)[0]
    approved = dict(re.findall(r"^(\d)\. \*\*[^*]+\.\*\* (.+)$", section, flags=re.M))
    assert sorted(approved) == list("1234567")
    slugs = {"1": "bokken-shomen-suburi", **{str(n): f"aiki-ken-suburi-{n}" for n in range(2, 8)}}
    seed = {k["slug"]: k for k in BOKKEN}
    for n, text in approved.items():
        assert seed[slugs[n]]["description_tr"] == text, f"suburi {n}"


def test_seed_bokken_suburi_en_matches_verified_doc():
    """Seed EN metinleri onaylı EN belgesiyle birebir; suburi 7 başlığı §4 ile uyumlu (B-41a-2)."""
    import re
    from pathlib import Path

    from app.seed import BOKKEN

    root = Path(__file__).resolve().parent.parent / "docs/team/content/verified"
    doc = (root / "2026-11-18-bokken-suburi-en.md").read_text(encoding="utf-8")
    approved = dict(re.findall(r"^\| `([^`]+)` \| (.+?) \| [^|]+ \|$", doc, flags=re.M))
    assert sorted(approved) == sorted(["bokken-shomen-suburi", *[f"aiki-ken-suburi-{n}" for n in range(2, 8)]])
    seed = {k["slug"]: k for k in BOKKEN}
    for slug, text in approved.items():
        assert seed[slug]["description_en"] == text, slug

    assert seed["aiki-ken-suburi-7"]["title_en"] == "Aiki-ken suburi 7 — Shichi (nana) no suburi"
    assert seed["aiki-ken-suburi-7"]["title_tr"] == seed["aiki-ken-suburi-7"]["title_en"]


async def test_program_index_lists_both_and_links_from_dashboard(client):
    await seeded()
    r = await client.get("/programs")  # ziyaretçi
    assert r.status_code == 200
    assert f"/programs/{JO}" in r.text and f"/programs/{BOKKEN}" in r.text
    assert "30 Günlük Bokken Suburi Programı" in r.text
    await signup(client)
    r = await client.get("/programs")
    assert "Aynı anda tek program aktif olur" in r.text
    assert f'action="/programs/{BOKKEN}/enroll"' in r.text
    # rehberden bokken programına bağlantı
    assert f"/programs/{BOKKEN}" in (await client.get("/guide/bokken")).text
    # dashboard: aktif program bandında dizin bağlantısı
    await enroll(client, JO)
    assert 'href="/programs"' in (await client.get("/app")).text
    assert "Tüm programlar / programı değiştir" in (await client.get("/app")).text


async def test_start_bokken_and_complete_day(client):
    from app.db import async_session
    from app.models import PracticeLog

    await seeded()
    email = await signup(client)
    r = await enroll(client, BOKKEN)
    assert r.status_code == 303 and r.headers["location"] == f"/programs/{BOKKEN}/day/1"
    day = await client.get(f"/programs/{BOKKEN}/day/1")
    assert day.status_code == 200 and "migi hanmi" in day.text
    detail = await client.get(f"/programs/{BOKKEN}")
    assert "Gün 1/30" in detail.text and "Joryu tavsiyesi" not in detail.text  # kayıtlıda tavsiye kutusu yok
    csrf = await get_csrf(client, f"/programs/{BOKKEN}/day/1")
    r = await client.post(f"/programs/{BOKKEN}/day/1/complete", data={"csrf_token": csrf})
    assert r.status_code == 303
    user = await db_user(email)
    async with async_session() as db:
        logs = (await db.execute(select(PracticeLog).where(PracticeLog.user_id == user.id))).scalars().all()
    assert len(logs) == 1 and logs[0].discipline == "bokken" and logs[0].kata_slug is None
    # öneri metni: sayaç/kilit yok, "hocana danış" günde var
    assert "hocandan öğrenmediysen" in day.text and "en az 10 tekrar önerilir" in day.text


async def test_advice_shown_to_unenrolled_without_counter(client):
    await seeded()
    await signup(client)
    r = await client.get(f"/programs/{BOKKEN}")
    assert "Joryu tavsiyesi" in r.text and "en az 10 tekrar" in r.text
    assert "Bunlar tavsiyedir; sayaç ya da kilit yok." in r.text


async def test_switch_programs_single_active_progress_kept(client):
    from app.db import async_session
    from app.models import EnrollmentDay, Enrollment

    await seeded()
    email = await signup(client)
    await enroll(client, JO)
    csrf = await get_csrf(client, f"/programs/{JO}/day/1")
    await client.post(f"/programs/{JO}/day/1/complete", data={"csrf_token": csrf})
    assert (await active_slug(email))[0] == JO
    assert "30 Günlük Jo Suburi Programı" in (await client.get("/app")).text

    # bokken'e geç: dashboard bandı bokken, jo kaydı ve ilerlemesi duruyor
    r = await enroll(client, BOKKEN)
    assert r.status_code == 303
    assert await active_slug(email) == [BOKKEN, JO]
    app_html = (await client.get("/app")).text
    assert "program-banner" in app_html and f"/programs/{BOKKEN}/day/1" in app_html
    assert f"/programs/{JO}/day/" not in app_html  # tek aktif program
    user = await db_user(email)
    async with async_session() as db:
        enrollments = (
            await db.execute(
                select(Enrollment).options(selectinload(Enrollment.program)).where(Enrollment.user_id == user.id)
            )
        ).scalars().all()
        assert len(enrollments) == 2
        jo_e = next(e for e in enrollments if e.program.slug == JO)
        days = (await db.execute(select(EnrollmentDay).where(EnrollmentDay.enrollment_id == jo_e.id))).scalars().all()
        assert [d.day_number for d in days] == [1]  # eski ilerleme silinmedi

    # dizinde durumlar
    idx = (await client.get("/programs")).text
    assert "Aktif program" in idx and "Başladın: 1/30 gün tamam" in idx
    assert f"/programs/{JO}" in idx
    # jo detayında "aktif değil" notu; geri geçince jo aktif, ilerleme 1 gün
    assert "şu an aktif programın değil" in (await client.get(f"/programs/{JO}")).text
    r = await enroll(client, JO)
    assert r.status_code == 303 and r.headers["location"] == f"/programs/{JO}"
    assert await active_slug(email) == [JO, BOKKEN]
    assert "şu an aktif programın değil" not in (await client.get(f"/programs/{JO}")).text
    assert "Gün 2/30" in (await client.get(f"/programs/{JO}")).text
    # tekrar POST yeni kayıt açmaz
    await enroll(client, JO)
    async with async_session() as db:
        n = len((await db.execute(select(Enrollment).where(Enrollment.user_id == user.id))).scalars().all())
    assert n == 2


async def test_enroll_requires_login_and_unknown_program_404(client):
    await seeded()
    csrf = await get_csrf(client, "/login")
    r = await client.post(f"/programs/{BOKKEN}/enroll", data={"csrf_token": csrf})
    assert r.status_code == 303 and r.headers["location"] == "/login"
    await signup(client)
    csrf = await get_csrf(client, "/programs")
    r = await client.post("/programs/yok-boyle-program/enroll", data={"csrf_token": csrf})
    assert r.status_code == 404 or "404" in r.text
