"""Kuşaklar ve rozetler: pratik verisinden anlık hesaplanır, tablo gerektirmez.

Kuşaklar seriye bağlıdır ve klasik kyu ilerleyişini izler: beyazdan siyaha.
Bir eşik bir kez geçilince kaybolmaz — tüm zamanların en uzun serisine bakılır.
Siyah kuşak sonrası dan sistemi (1. dan, 2. dan...) ileride eklenecek.
"""

from dataclasses import dataclass

# (id, gün eşiği) — siyah kuşak 365 gün kesintisiz seri
BELTS = (
    ("white", 7),
    ("yellow", 21),
    ("orange", 45),
    ("green", 90),
    ("blue", 180),
    ("brown", 270),
    ("black", 365),
)

SESSION_THRESHOLDS = (1, 25, 100, 300)


@dataclass(frozen=True)
class Belt:
    id: str
    threshold: int
    earned: bool

    def label(self, t: dict) -> str:
        return t[f"belt_{self.id}"]

    def tip(self, t: dict) -> str:
        fmt = t["belt_tip_earned_fmt"] if self.earned else t["belt_tip_locked_fmt"]
        return fmt.format(n=self.threshold)


@dataclass(frozen=True)
class Badge:
    id: str
    threshold: int
    earned: bool

    def label(self, t: dict) -> str:
        if self.threshold == 1:
            return t["badge_first_session"]
        return t["badge_sessions_fmt"].format(n=self.threshold)

    def tip(self, t: dict) -> str:
        fmt = t["badge_tip_earned_fmt"] if self.earned else t["badge_tip_locked_fmt"]
        return fmt.format(n=self.threshold)


def compute_belts(longest_streak: int) -> list[Belt]:
    return [Belt(id=belt_id, threshold=n, earned=longest_streak >= n) for belt_id, n in BELTS]


def compute_badges(total_sessions: int) -> list[Badge]:
    return [
        Badge(id=f"sessions-{n}", threshold=n, earned=total_sessions >= n)
        for n in SESSION_THRESHOLDS
    ]
