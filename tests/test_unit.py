"""Saf mantık testleri — DB gerektirmez."""

import time
import uuid

from app.badges import BELTS, compute_badges, compute_belts, current_belt
from app.i18n.strings import STRINGS, get_strings
from app.security import (
    create_reset_token,
    create_session_token,
    create_verify_token,
    password_fingerprint,
    read_reset_token,
    read_session_token,
    read_verify_token,
    verify_ls_signature,
)

UID = uuid.uuid4()
HASH = "$2b$12$abcdefghijklmnopqrstuv"


class TestTokens:
    def test_session_roundtrip(self):
        token = create_session_token(UID, HASH)
        parsed = read_session_token(token)
        assert parsed == (UID, password_fingerprint(HASH))

    def test_session_tampered(self):
        token = create_session_token(UID, HASH)
        assert read_session_token(token[:-2] + "xx") is None
        assert read_session_token("garbage") is None

    def test_reset_bound_to_old_password(self):
        token = create_reset_token(UID, HASH)
        uid, fp = read_reset_token(token)
        assert uid == UID
        # Parola değişti -> parmak izi artık eşleşmez (tek kullanımlık)
        assert fp != password_fingerprint("yeni-hash")

    def test_verify_roundtrip_and_prefix_isolation(self):
        token = create_verify_token(UID)
        assert read_verify_token(token) == UID
        # Token türleri birbirinin yerine geçemez
        assert read_reset_token(token) is None
        assert read_session_token(create_reset_token(UID, HASH)) is None

    def test_expiry(self, monkeypatch):
        token = create_session_token(UID, HASH)
        real_time = time.time
        monkeypatch.setattr(time, "time", lambda: real_time() + 10**9)
        assert read_session_token(token) is None


class TestWebhookSignature:
    def test_rejects_bad_signature(self, monkeypatch):
        from app import security

        monkeypatch.setattr(security.settings, "ls_webhook_secret", "s3cret")
        import hashlib
        import hmac as hmac_mod

        body = b'{"ok":1}'
        good = hmac_mod.new(b"s3cret", body, hashlib.sha256).hexdigest()
        assert verify_ls_signature(body, good)
        assert not verify_ls_signature(body, "deadbeef")
        monkeypatch.setattr(security.settings, "ls_webhook_secret", "")
        assert not verify_ls_signature(body, good)  # secret yoksa asla geçmez


class TestBelts:
    def test_everyone_starts_white(self):
        belts = compute_belts(0)
        assert belts[0].id == "white" and belts[0].earned
        assert sum(b.earned for b in belts) == 1

    def test_black_at_365(self):
        assert not compute_belts(364)[-1].earned
        assert compute_belts(365)[-1].earned

    def test_current_belt_is_highest_earned(self):
        assert current_belt(0).id == "white"
        assert current_belt(120).id == "green"
        assert current_belt(9999).id == "black"

    def test_thresholds_monotonic(self):
        values = [n for _, n in BELTS]
        assert values == sorted(values) and len(set(values)) == len(values)

    def test_badges(self):
        badges = compute_badges(25)
        assert [b.earned for b in badges] == [True, True, False, False]


class TestI18n:
    def test_langs_have_same_keys(self):
        assert set(STRINGS["tr"].keys()) == set(STRINGS["en"].keys())

    def test_unknown_lang_falls_back(self):
        assert get_strings("de") == STRINGS["tr"]
