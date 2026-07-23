import re
import secrets
from datetime import UTC, datetime

from fastapi import APIRouter, BackgroundTasks, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.constants import SELECTABLE_DISCIPLINES
from app.db import get_db
from app.deps import csrf_protect, get_current_user, require_user, waitlist_gate
from app.i18n.strings import get_strings
from app.mail import send_email
from app.models import User
from app.rate_limit import limiter
from app.render import render, resolve_lang
from app.security import (
    SESSION_COOKIE,
    SESSION_MAX_AGE,
    create_reset_token,
    create_session_token,
    create_verify_token,
    hash_password,
    password_fingerprint,
    read_reset_token,
    read_verify_token,
    verify_password,
)

router = APIRouter(dependencies=[Depends(waitlist_gate)])

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$")
REF_RE = re.compile(r"^[a-f0-9]{6,12}$")


def _session_response(user: User) -> RedirectResponse:
    response = RedirectResponse("/app", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        create_session_token(user.id, user.password_hash),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=settings.env == "production",
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(
    request: Request, ref: str | None = Query(default=None), user: User | None = Depends(get_current_user)
):
    if user:
        return RedirectResponse("/app", status_code=303)
    return render(
        request, "register.html", error=None, disciplines=SELECTABLE_DISCIPLINES,
        ref=ref if ref and REF_RE.match(ref) else "",
    )


def _send_verification(background: BackgroundTasks, user: User) -> None:
    strings = get_strings(user.lang or "tr")
    link = f"{settings.base_url}/verify?token={create_verify_token(user.id)}"
    background.add_task(
        send_email,
        user.email,
        strings["mail_verify_subject"],
        strings["mail_verify_body"].format(link=link),
    )


@router.post("/register", dependencies=[Depends(csrf_protect)])
@limiter.limit("10/minute")
async def register(
    request: Request,
    background: BackgroundTasks,
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    discipline: str = Form("aikijo"),
    ref: str = Form(""),
    db: AsyncSession = Depends(get_db),
):
    email = email.strip().lower()
    username = username.strip().lower()
    ref_clean = ref if ref and REF_RE.match(ref) else ""
    if not EMAIL_RE.match(email):
        return render(request, "register.html", error="form_error_invalid", disciplines=SELECTABLE_DISCIPLINES, ref=ref_clean)
    if not USERNAME_RE.match(username):
        return render(request, "register.html", error="profile_error_username_invalid", disciplines=SELECTABLE_DISCIPLINES, ref=ref_clean)
    if len(password) < 8:
        return render(request, "register.html", error="auth_error_password_short", disciplines=SELECTABLE_DISCIPLINES, ref=ref_clean)
    if discipline not in SELECTABLE_DISCIPLINES:
        discipline = "aikijo"

    existing = await db.execute(select(User.id).where(User.email == email))
    if existing.scalar_one_or_none() is not None:
        return render(request, "register.html", error="auth_error_exists", disciplines=SELECTABLE_DISCIPLINES, ref=ref_clean)
    taken = await db.execute(select(User.id).where(User.username == username))
    if taken.scalar_one_or_none() is not None:
        return render(request, "register.html", error="profile_error_username_taken", disciplines=SELECTABLE_DISCIPLINES, ref=ref_clean)

    referred_by = None
    if ref_clean:
        referrer = await db.execute(select(User.referral_code).where(User.referral_code == ref_clean))
        referred_by = ref_clean if referrer.scalar_one_or_none() else None

    user = User(
        email=email,
        password_hash=await hash_password(password),
        lang=resolve_lang(request),
        username=username,
        discipline=discipline,
        referral_code=secrets.token_hex(5),
        referred_by=referred_by,
    )
    db.add(user)
    await db.commit()
    _send_verification(background, user)
    return _session_response(user)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse("/app", status_code=303)
    return render(request, "login.html", error=None)


@router.post("/login", dependencies=[Depends(csrf_protect)])
@limiter.limit("10/minute")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    email = email.strip().lower()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if user is None or not await verify_password(password, user.password_hash):
        return render(request, "login.html", error="auth_error_invalid")
    return _session_response(user)


@router.post("/logout", dependencies=[Depends(csrf_protect)])
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


# --- Şifremi unuttum / sıfırlama ---


@router.get("/forgot", response_class=HTMLResponse)
async def forgot_page(request: Request):
    return render(request, "forgot.html", sent=False)


@router.post("/forgot", dependencies=[Depends(csrf_protect)])
@limiter.limit("5/minute")
async def forgot(
    request: Request,
    background: BackgroundTasks,
    email: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    email = email.strip().lower()
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    # Hesap var/yok bilgisi sızdırılmaz: her durumda aynı ekran
    if user is not None:
        strings = get_strings(user.lang or resolve_lang(request))
        token = create_reset_token(user.id, user.password_hash)
        link = f"{settings.base_url}/reset?token={token}"
        background.add_task(
            send_email,
            user.email,
            strings["mail_reset_subject"],
            strings["mail_reset_body"].format(link=link),
        )
    return render(request, "forgot.html", sent=True)


@router.get("/reset", response_class=HTMLResponse)
async def reset_page(request: Request, token: str = Query(""), db: AsyncSession = Depends(get_db)):
    user = await _user_from_reset_token(db, token)
    return render(request, "reset.html", token=token, invalid=user is None, error=None)


@router.post("/reset", dependencies=[Depends(csrf_protect)])
@limiter.limit("5/minute")
async def reset(
    request: Request,
    token: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    user = await _user_from_reset_token(db, token)
    if user is None:
        return render(request, "reset.html", token=token, invalid=True, error=None)
    if len(password) < 8:
        return render(request, "reset.html", token=token, invalid=False, error="auth_error_password_short")
    user.password_hash = await hash_password(password)
    await db.commit()
    # Yeni parolayla otomatik giriş — eski oturumlar parmak izi değiştiği için düştü
    return _session_response(user)


async def _user_from_reset_token(db: AsyncSession, token: str) -> User | None:
    parsed = read_reset_token(token)
    if parsed is None:
        return None
    user_id, fingerprint = parsed
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    # Parmak izi eski hash'e bağlı: parola değiştiyse token tek kullanımlıktı
    if user is None or fingerprint != password_fingerprint(user.password_hash):
        return None
    return user


# --- E-posta doğrulama (yumuşak: giriş engellenmez) ---


@router.get("/verify")
async def verify_email(token: str = Query(""), db: AsyncSession = Depends(get_db)):
    user_id = read_verify_token(token)
    if user_id is not None:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if user is not None and user.email_verified_at is None:
            user.email_verified_at = datetime.now(UTC)
            await db.commit()
    # Geçersiz token'da da app'e döner; banner durumu gerçeği yansıtır
    return RedirectResponse("/app", status_code=303)


@router.post("/verify/resend", dependencies=[Depends(csrf_protect)])
@limiter.limit("3/minute")
async def resend_verification(
    request: Request,
    background: BackgroundTasks,
    user: User = Depends(require_user),
):
    if user.email_verified_at is None:
        _send_verification(background, user)
    return RedirectResponse(request.headers.get("referer") or "/app", status_code=303)


# --- Parola değiştirme (girişliyken) ---


@router.post("/password", dependencies=[Depends(csrf_protect)])
@limiter.limit("10/minute")
async def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    if not await verify_password(current_password, user.password_hash):
        return render(request, "profile_edit.html", user=user, disciplines=SELECTABLE_DISCIPLINES,
                      error="pw_wrong_current", saved=False)
    if len(new_password) < 8:
        return render(request, "profile_edit.html", user=user, disciplines=SELECTABLE_DISCIPLINES,
                      error="auth_error_password_short", saved=False)
    user.password_hash = await hash_password(new_password)
    await db.commit()
    # Diğer cihazlardaki oturumlar düşer; bu cihaza yeni cookie verilir
    return _session_response(user)


# --- Hesap silme ---


@router.post("/account/delete", dependencies=[Depends(csrf_protect)])
@limiter.limit("5/minute")
async def delete_account(
    request: Request,
    password: str = Form(...),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    if not await verify_password(password, user.password_hash):
        return render(request, "profile_edit.html", user=user, disciplines=SELECTABLE_DISCIPLINES,
                      error="pw_wrong_current", saved=False)
    await db.delete(user)  # practice_logs, enrollments, subscription cascade ile silinir
    await db.commit()
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response
