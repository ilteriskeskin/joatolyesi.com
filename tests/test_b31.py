"""B-31: Günün ipucu — deterministik seçim, doğrulanmamış madde yok, dashboard kartı."""

import re
import uuid
from datetime import date

import httpx
import pytest


def test_pick_daily_tip_is_deterministic():
    from app.tips_content import TIPS, pick_daily_tip

    d = date(2026, 11, 12)
    assert pick_daily_tip(d) is pick_daily_tip(d) is TIPS[d.toordinal() % len(TIPS)]
    seen = {pick_daily_tip(date.fromordinal(d.toordinal() + i))["tr"] for i in range(len(TIPS))}
    assert len(seen) == len(TIPS)  # ardışık günler döner, döngü tüm listeyi kapsar


def test_unverified_dokkodo_first_item_removed():
    from app.tips_content import TIPS

    assert len(TIPS) == 20
    blob = " ".join(t["tr"] + t["en"] for t in TIPS)
    assert "olduğu gibi kabul et" not in blob
    assert "Accept everything" not in blob
    assert "control yourself" not in blob


@pytest.mark.asyncio
async def test_dashboard_renders_tip_card(migrated_db):
    from app.main import app
    from app.tips_content import pick_daily_tip
    from datetime import UTC, datetime

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/register")
        token = re.search(r'name="csrf_token" value="([^"]+)"', r.text).group(1)
        u = uuid.uuid4().hex[:8]
        r = await c.post("/register", data={"email": f"b31-{u}@test.com", "password": "password123",
                                            "username": f"b31{u}", "discipline": "aikijo", "csrf_token": token})
        assert r.status_code == 303
        tip = pick_daily_tip(datetime.now(UTC).date())
        html = (await c.get("/app?lang=en")).text
        assert "tip-of-day" in html
        assert tip["source"] in html
        assert tip["en"].replace("'", "&#39;") in html or tip["en"] in html
