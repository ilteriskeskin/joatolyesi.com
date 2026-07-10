"""Waitlist lansman daveti: davet edilmemiş herkese "açıldık" maili gönderir.

Sunucuda:  docker compose exec app python scripts/send_invites.py
Önce kaç kişiye gideceğini gösterir; --yes olmadan GÖNDERMEZ (dry-run).
invited_at ile çift gönderim engellenir; yarıda kesilirse kaldığı yerden devam eder.
"""

import asyncio
import sys
from datetime import UTC, datetime

from sqlalchemy import select

from app.config import settings
from app.db import async_session
from app.mail import send_email
from app.models import Waitlist

SUBJECT = {
    "tr": "Joryu açıldı — yerin hazır",
    "en": "Joryu is live — your spot is ready",
}
BODY = {
    "tr": (
        "<p>Bekleme listesine katılmıştın: Joryu artık açık.</p>"
        "<p>Pratik kaydı, seri takibi, kuşak sistemi ve kata kütüphanesi seni bekliyor. "
        'Herkes beyaz kuşakla başlar — <a href="{link}">hesabını aç ve ilk seansını kaydet</a>.</p>'
        "<p>İyi çalışmalar.<br>İlteriş — @joryu.art</p>"
    ),
    "en": (
        "<p>You joined the waitlist: Joryu is now live.</p>"
        "<p>Practice logging, streaks, the belt system and the kata library are waiting. "
        'Everyone starts with the white belt — <a href="{link}">create your account and log your first session</a>.</p>'
        "<p>Train well.<br>İlteriş — @joryu.art</p>"
    ),
}


async def main(dry_run: bool) -> None:
    async with async_session() as db:
        result = await db.execute(select(Waitlist).where(Waitlist.invited_at.is_(None)))
        pending = list(result.scalars().all())
        print(f"Davet bekleyen: {len(pending)} kişi (dry-run={dry_run})")
        if dry_run:
            for w in pending[:10]:
                print(" ", w.email, w.lang)
            if len(pending) > 10:
                print(f"  ... ve {len(pending) - 10} kişi daha")
            print("Göndermek için: python scripts/send_invites.py --yes")
            return

        link = f"{settings.base_url}/register"
        sent = 0
        for w in pending:
            lang = w.lang if w.lang in SUBJECT else "tr"
            await send_email(w.email, SUBJECT[lang], BODY[lang].format(link=link))
            w.invited_at = datetime.now(UTC)
            await db.commit()  # her mailden sonra: kesinti olursa kaldığı yerden devam
            sent += 1
            print(f"[{sent}/{len(pending)}] {w.email}")
            await asyncio.sleep(0.6)  # Resend rate limitine saygı (2 req/s)
        print(f"Bitti: {sent} davet gönderildi.")


if __name__ == "__main__":
    asyncio.run(main(dry_run="--yes" not in sys.argv))
