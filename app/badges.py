"""Rozetler: pratik verisinden anlık hesaplanır, ayrı tablo gerektirmez.

Bir rozet bir kez eşiği geçince kaybolmaz: seri rozetleri mevcut seriye
değil, tüm zamanların en uzun serisine bakar.
"""

from dataclasses import dataclass

STREAK_THRESHOLDS = (7, 30, 90, 180, 365)
SESSION_THRESHOLDS = (1, 25, 100, 300)


@dataclass(frozen=True)
class Badge:
    id: str
    kind: str  # "streak" | "sessions"
    threshold: int
    earned: bool

    def label(self, t: dict) -> str:
        if self.kind == "sessions" and self.threshold == 1:
            return t["badge_first_session"]
        fmt = t["badge_streak_fmt"] if self.kind == "streak" else t["badge_sessions_fmt"]
        return fmt.format(n=self.threshold)


def compute_badges(longest_streak: int, total_sessions: int) -> list[Badge]:
    badges = [
        Badge(id=f"sessions-{n}", kind="sessions", threshold=n, earned=total_sessions >= n)
        for n in SESSION_THRESHOLDS
    ]
    badges += [
        Badge(id=f"streak-{n}", kind="streak", threshold=n, earned=longest_streak >= n)
        for n in STREAK_THRESHOLDS
    ]
    return badges
