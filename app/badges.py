"""Kuşaklar ve rozetler: pratik verisinden anlık hesaplanır, tablo gerektirmez.

Kuşaklar toplam pratik gününe (farklı gün sayısı) bağlıdır ve klasik kyu
ilerleyişini izler: herkes beyaz kuşakla başlar, 365 pratik gününü dolduran
siyah kuşak olur. Toplam gün azalmayacağı için kazanılan kuşak kaybolmaz.
Siyah kuşak sonrası dan sistemi (1. dan, 2. dan...) ileride eklenecek.
"""

from dataclasses import dataclass

# (id, toplam pratik günü eşiği) — beyaz herkese, siyah 365 günde
BELTS = (
    ("white", 0),
    ("yellow", 30),
    ("orange", 60),
    ("green", 120),
    ("blue", 200),
    ("brown", 280),
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
        if self.threshold == 0:
            return t["belt_tip_start"]
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


def compute_belts(total_practice_days: int) -> list[Belt]:
    return [Belt(id=belt_id, threshold=n, earned=total_practice_days >= n) for belt_id, n in BELTS]


def compute_badges(total_sessions: int) -> list[Badge]:
    return [
        Badge(id=f"sessions-{n}", threshold=n, earned=total_sessions >= n)
        for n in SESSION_THRESHOLDS
    ]
