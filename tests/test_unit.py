"""Saf mantık testleri — DB gerektirmez."""

import time
import uuid

from app.badges import BELTS, compute_badges, compute_belts, current_belt
from app.constants import DISCIPLINES, SELECTABLE_DISCIPLINES
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

    def test_black_at_180(self):
        assert not compute_belts(179)[-1].earned
        assert compute_belts(180)[-1].earned

    def test_belt_thresholds(self):
        assert [n for _, n in BELTS] == [0, 15, 30, 60, 100, 140, 180]

    def test_nobody_loses_a_belt_from_new_thresholds(self):
        # eski eşiklerin hepsi (30/60/120/200/280/365) yeni eşiklerin üstünde: kuşak asla düşmez
        old = {"yellow": 30, "orange": 60, "green": 120, "blue": 200, "brown": 280, "black": 365}
        new = dict(BELTS)
        assert all(new[k] <= v for k, v in old.items())

    def test_current_belt_is_highest_earned(self):
        assert current_belt(0).id == "white"
        assert current_belt(60).id == "green"
        assert current_belt(9999).id == "black"

    def test_thresholds_monotonic(self):
        values = [n for _, n in BELTS]
        assert values == sorted(values) and len(set(values)) == len(values)

    def test_badges(self):
        badges = compute_badges(25)
        assert [b.earned for b in badges] == [True, True, False, False]


class TestDisciplines:
    def test_karate_taekwondo_not_selectable_but_preserved(self):
        assert "karate" not in SELECTABLE_DISCIPLINES
        assert "taekwondo" not in SELECTABLE_DISCIPLINES
        assert "karate" in DISCIPLINES and "taekwondo" in DISCIPLINES  # eski veri hâlâ geçerli


class TestI18n:
    def test_langs_have_same_keys(self):
        assert set(STRINGS["tr"].keys()) == set(STRINGS["en"].keys())

    def test_unknown_lang_falls_back(self):
        assert get_strings("de") == STRINGS["tr"]


class TestStreakFreeze:
    """Seri kuralı "2 günde 1": aradaki fark <= 2 sürer, fark == 3 donma ister."""

    T = None

    @staticmethod
    def days(t, *offs):
        from datetime import timedelta
        return [t - timedelta(days=o) for o in offs]

    def test_consecutive_days(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes(self.days(t, 0, 1, 2, 3, 4), t) == (5, 0)

    def test_gap_of_one_empty_day_keeps_chain_without_freeze(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        # 1, 3, 5. günler -> zincir ilk günden son güne 5 takvim günü, donma harcanmaz
        assert _streak_with_freezes(self.days(t, 0, 2, 4), t) == (5, 0)
        assert _streak_with_freezes(self.days(t, 2, 4, 6), t) == (5, 0)

    def test_gap_of_two_empty_days_needs_freeze(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        # fark 3 (2 boş gün): donma köprüler, seri takvim günü olarak 4
        assert _streak_with_freezes(self.days(t, 0, 3), t) == (4, 1)

    def test_gap_of_three_empty_days_breaks(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes(self.days(t, 0, 4), t) == (1, 0)
        assert _streak_with_freezes(self.days(t, 0, 5, 6), t) == (1, 0)

    def test_freeze_budget_two_per_month_then_chain_breaks(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 28)
        # 28, 25, 22, 19: üç tane 2-boş-günlük boşluk, aynı ay -> yalnız 2'si köprülenir
        s, used = _streak_with_freezes(self.days(t, 0, 3, 6, 9), t)
        assert used == 2 and s == 7  # 22..28
        # tüm boşluklar <= 2 fark ise donma gerekmez
        assert _streak_with_freezes(self.days(t, 0, 2, 4, 6, 8, 10), t) == (11, 0)

    def test_freeze_spent_from_month_of_the_gap(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 8, 2)
        # 2 Ağu ve 30 Tem: boş günler 31 Tem, 1 Ağu; boşluğun son günü Ağustos'ta -> bu ayın bütçesi
        assert _streak_with_freezes([date(2026, 8, 2), date(2026, 7, 30)], t) == (4, 1)
        # boşluklar tamamen Temmuz'daysa (31 ve 28 Tem) Ağustos'un hakkı harcanmaz
        d = [date(2026, 8, 2), date(2026, 8, 1), date(2026, 7, 29), date(2026, 7, 26)]
        assert _streak_with_freezes(d, t) == (8, 0)  # 26 Tem..2 Ağu

    def test_liveness_last_practice_within_two_days(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes(self.days(t, 0), t)[0] == 1
        assert _streak_with_freezes(self.days(t, 1), t)[0] == 1
        assert _streak_with_freezes(self.days(t, 2), t) == (1, 0)  # bugün-2: hâlâ canlı, donma yok
        assert _streak_with_freezes(self.days(t, 2, 3), t) == (2, 0)

    def test_liveness_three_days_ago_is_bridged_by_freeze(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes(self.days(t, 3), t) == (1, 1)
        assert _streak_with_freezes(self.days(t, 3, 4), t) == (2, 1)

    def test_liveness_dead_without_freeze_or_after_four_days(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes(self.days(t, 4), t) == (0, 0)
        assert _streak_with_freezes(self.days(t, 10, 11), t) == (0, 0)

    def test_live_freeze_counts_against_the_budget(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        # bugün-3 (canlılık donması) + bir geçmiş boşluk = 2 hak; üçüncü boşluk köprülenemez
        d = [date(2026, 7, 8), date(2026, 7, 5), date(2026, 7, 2)]
        assert _streak_with_freezes(d, t) == (4, 2)  # 5..8 Temmuz

    def test_future_dated_log_counts_as_alive(self):
        from datetime import date, timedelta
        from app.stats import _streak_with_freezes
        t = date(2026, 7, 11)
        assert _streak_with_freezes([t + timedelta(days=1), t], t)[0] == 2

    def test_empty(self):
        from datetime import date
        from app.stats import _streak_with_freezes
        assert _streak_with_freezes([], date(2026, 7, 11)) == (0, 0)

    def test_last_day_flag(self):
        from datetime import date
        from app.stats import _streak_state
        t = date(2026, 7, 11)
        assert _streak_state(self.days(t, 2, 3), t)["last_day"] is True      # son pratik önceki gün
        assert _streak_state(self.days(t, 1), t)["last_day"] is False         # dün çalıştı
        assert _streak_state(self.days(t, 0, 2), t)["last_day"] is False      # bugün çalıştı
        assert _streak_state(self.days(t, 3), t)["last_day"] is False         # donmayla ayakta, uyarı bu durumda yok
        assert _streak_state([], t)["last_day"] is False

    def test_last_day_freeze_flag_follows_budget(self, monkeypatch):
        from datetime import date
        import app.stats as stats
        t = date(2026, 7, 11)
        assert stats._streak_state(self.days(t, 2, 3), t)["last_day_freeze"] is True
        # bu ay iki donma zaten zincirde harcanmışsa bugün çalışılmazsa seri biter
        spent = [date(2026, 7, 8), date(2026, 7, 5), date(2026, 7, 2)]
        # son pratik bugün-2 olsun: 9 Tem, 6 Tem, 3 Tem (iki geçmiş boşluk = 2 donma, ikisi de Temmuz)
        state = stats._streak_state([date(2026, 7, 9), date(2026, 7, 6), date(2026, 7, 3)], t)
        assert state["last_day"] is True and state["last_day_freeze"] is False
        assert stats._streak_state(self.days(t, 1), t)["last_day_freeze"] is False  # son gün değil
        monkeypatch.setattr(stats, "FREEZES_PER_MONTH", 0)
        assert stats._streak_state(self.days(t, 2), t)["last_day_freeze"] is False

    def test_longest_streak_uses_calendar_span(self):
        from datetime import date
        from app.stats import _longest_streak
        t = date(2026, 7, 11)
        assert _longest_streak([]) == 0
        assert _longest_streak(self.days(t, 0)) == 1
        assert _longest_streak(self.days(t, 0, 1, 2)) == 3
        assert _longest_streak(self.days(t, 0, 2, 4)) == 5            # 1,3,5 -> 5
        assert _longest_streak(self.days(t, 0, 3)) == 1               # fark 3: donma sayılmaz
        # eski uzun zincir, yeni kısa zincirden büyük
        assert _longest_streak(self.days(t, 0, 1, 20, 22, 24, 26)) == 7


