import base64
import hashlib
import hmac
import time
import uuid

import bcrypt
from starlette.concurrency import run_in_threadpool

from app.config import settings

SESSION_COOKIE = "session"
SESSION_MAX_AGE = 60 * 60 * 24 * 30  # 30 gün


# bcrypt CPU-yoğun ve senkron — event loop'u bloklamamak için threadpool'da
async def hash_password(password: str) -> str:
    hashed = await run_in_threadpool(bcrypt.hashpw, password.encode(), bcrypt.gensalt())
    return hashed.decode()


async def verify_password(password: str, password_hash: str) -> bool:
    return await run_in_threadpool(bcrypt.checkpw, password.encode(), password_hash.encode())


def _sign(payload: str) -> str:
    sig = hmac.new(settings.secret_key.encode(), payload.encode(), hashlib.sha256).digest()
    return base64.urlsafe_b64encode(sig).decode().rstrip("=")


def create_session_token(user_id: uuid.UUID) -> str:
    payload = f"{user_id}.{int(time.time()) + SESSION_MAX_AGE}"
    return f"{payload}.{_sign(payload)}"


def read_session_token(token: str) -> uuid.UUID | None:
    parts = token.rsplit(".", 1)
    if len(parts) != 2:
        return None
    payload, sig = parts
    if not hmac.compare_digest(sig, _sign(payload)):
        return None
    try:
        user_id_str, expires_str = payload.split(".")
        if int(expires_str) < time.time():
            return None
        return uuid.UUID(user_id_str)
    except ValueError:
        return None


def verify_ls_signature(raw_body: bytes, signature: str) -> bool:
    if not settings.ls_webhook_secret:
        return False
    expected = hmac.new(settings.ls_webhook_secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)
