"""B-40: slug'a göre kata içerik şablonu."""

import httpx
import pytest

from app.kata_content import CONTENT, get_kata_content


@pytest.fixture()
async def client(migrated_db):
    from app.main import app
    from app.seed import seed_content

    await seed_content()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


def _seed_slugs():
    import app.seed as seed

    return {
        k["slug"]
        for v in vars(seed).values()
        if isinstance(v, list)
        for k in v
        if isinstance(k, dict) and "slug" in k
    }


def test_ilgili_slugs_exist_in_seed():
    slugs = _seed_slugs()
    for slug, langs in CONTENT.items():
        assert slug in slugs, slug
        for lang, c in langs.items():
            for rel in c["ilgili"]:
                assert rel in slugs, f"{slug}/{lang}: {rel}"


def test_content_lookup():
    assert get_kata_content("tkd-dwit-chagi", "tr")["title"].startswith("Dwit chagi")
    assert get_kata_content("tkd-dwit-chagi", "en")["title"].startswith("Dwit chagi (back kick)")
    assert get_kata_content("karate-choku-tsuki", "tr") is None
    assert "kendo-kodachi-1" not in CONTENT


@pytest.mark.asyncio
async def test_content_page_tr(client):
    r = await client.get("/kata/tkd-dwit-chagi?lang=tr")
    assert r.status_code == 200
    h = r.text
    assert "Dwit chagi (geri tekme) nedir, nasıl yapılır? — Joryu</title>" in h
    assert 'content="Dwit chagi, taekwondoda topukla yapılan geri tekmedir.' in h
    for heading in ("Nedir", "Nasıl yapılır", "Sık hatalar", "İlgili teknikler"):
        assert f"<h2>{heading}</h2>" in h
    assert "<ol><li>Dövüş duruşundan" in h
    assert "video-placeholder" in h or "video-frame" in h


@pytest.mark.asyncio
async def test_related_links_work(client):
    r = await client.get("/kata/karate-zenkutsu-dachi?lang=tr")
    for rel in CONTENT["karate-zenkutsu-dachi"]["tr"]["ilgili"]:
        assert f'href="/kata/{rel}"' in r.text
        assert (await client.get(f"/kata/{rel}")).status_code == 200


@pytest.mark.asyncio
async def test_content_page_en_omits_empty_sections(client):
    h = (await client.get("/kata/karate-kiba-dachi?lang=en")).text
    assert "Kiba dachi (horse stance): what it is and how to do it — Joryu</title>" in h
    assert "<h2>What it is</h2>" in h
    assert "<h2>How to do it</h2>" not in h
    assert "<h2>Related techniques</h2>" in h


@pytest.mark.asyncio
async def test_page_without_content_keeps_old_layout(client):
    r = await client.get("/kata/karate-choku-tsuki?lang=tr")
    assert r.status_code == 200
    assert "kata-nedir" not in r.text
    assert 'class="kata-related"' in r.text
