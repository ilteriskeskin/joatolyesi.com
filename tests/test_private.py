"""Özel sayfa erişimi: yalnız OWNER_EMAIL hesabı görür."""

import uuid

import httpx
import pytest

from app.config import settings
from tests.test_flows import register

pytestmark = pytest.mark.asyncio


@pytest.fixture()
async def client(migrated_db):
    from app.main import app

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_private_page_owner_only(client, monkeypatch):
    owner = f"owner-{uuid.uuid4().hex[:8]}@test.com"
    monkeypatch.setattr(settings, "owner_email", owner.upper())  # büyük/küçük harf duyarsız

    r = await client.get("/ozel/90-gun")
    assert r.status_code == 303 and "/login" in r.headers["location"]

    await register(client, f"other-{uuid.uuid4().hex[:8]}@test.com", f"other-{uuid.uuid4().hex[:8]}")
    r = await client.get("/ozel/90-gun")
    assert r.status_code == 404

    client.cookies.clear()
    await register(client, owner, f"owner-{uuid.uuid4().hex[:8]}")
    r = await client.get("/ozel/90-gun")
    assert r.status_code == 200
    assert "90 Günlük" in r.text
    assert r.headers["x-robots-tag"].startswith("noindex")


async def test_private_page_closed_without_owner(client, monkeypatch):
    monkeypatch.setattr(settings, "owner_email", "")
    r = await client.get("/ozel/90-gun")
    assert r.status_code == 404
