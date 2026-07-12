"""Web Push gönderimi (VAPID). Route içinde await edilmez — BackgroundTasks
ile çağrılır. Anahtarlar yoksa (dev) sadece loglar, hata fırlatmaz."""

import json
import logging

from starlette.concurrency import run_in_threadpool

from app.config import settings

logger = logging.getLogger("joryu.push")


async def send_push(subscription_info: dict, title: str, body: str, url: str = "/app") -> bool:
    """Tek bir aboneliğe bildirim gönderir. Abonelik artık geçersizse
    (410/404) False döner — çağıran DB'den silebilir."""
    if not settings.vapid_private_key:
        logger.info("Push (dev, gönderilmedi): %s", title)
        return True

    from pywebpush import WebPushException, webpush

    payload = json.dumps({"title": title, "body": body, "url": url})

    def _send() -> bool:
        try:
            webpush(
                subscription_info=subscription_info,
                data=payload,
                vapid_private_key=settings.vapid_private_key,
                vapid_claims={"sub": settings.vapid_claims_email},
            )
            return True
        except WebPushException as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status in (404, 410):
                return False
            logger.error("Push gönderilemedi: %s", exc)
            return True  # geçici hata — aboneliği silme

    return await run_in_threadpool(_send)
