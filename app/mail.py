"""E-posta gönderimi (Resend). Route içinde await edilmez — BackgroundTasks ile
çağrılır ki yanıt beklemesin. API key yoksa (dev) sadece loglar."""

import logging

import httpx

from app.config import settings

logger = logging.getLogger("joryu.mail")

RESEND_URL = "https://api.resend.com/emails"


async def send_email(to: str, subject: str, html: str, headers: dict[str, str] | None = None) -> None:
    if not settings.resend_api_key:
        logger.info("Mail (dev, gönderilmedi) to=%s subject=%r headers=%s", to, subject, sorted(headers or {}))
        return
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                RESEND_URL,
                headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                json={
                    "from": settings.mail_from,
                    "to": [to],
                    "subject": subject,
                    "html": html,
                    # List-Unsubscribe vb.: Resend "headers" alanını destekler
                    **({"headers": headers} if headers else {}),
                },
            )
            if resp.status_code >= 400:
                logger.error("Mail gönderilemedi to=%s status=%s body=%s", to, resp.status_code, resp.text[:300])
    except httpx.HTTPError:
        logger.exception("Mail gönderimi hata verdi to=%s", to)
