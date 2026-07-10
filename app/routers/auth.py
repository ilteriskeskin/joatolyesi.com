import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.constants import DISCIPLINES
from app.db import get_db
from app.deps import get_current_user
from app.models import User
from app.rate_limit import limiter
from app.render import render, resolve_lang
from app.security import SESSION_COOKIE, SESSION_MAX_AGE, create_session_token, hash_password, verify_password

router = APIRouter()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$")


def _session_response(user: User) -> RedirectResponse:
    response = RedirectResponse("/app", status_code=303)
    response.set_cookie(
        SESSION_COOKIE,
        create_session_token(user.id),
        max_age=SESSION_MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=settings.env == "production",
    )
    return response


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse("/app", status_code=303)
    return render(request, "register.html", error=None, disciplines=DISCIPLINES)


@router.post("/register")
@limiter.limit("10/minute")
async def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    username: str = Form(...),
    discipline: str = Form("aikijo"),
    db: AsyncSession = Depends(get_db),
):
    email = email.strip().lower()
    username = username.strip().lower()
    if not EMAIL_RE.match(email):
        return render(request, "register.html", error="form_error_invalid", disciplines=DISCIPLINES)
    if not USERNAME_RE.match(username):
        return render(request, "register.html", error="profile_error_username_invalid", disciplines=DISCIPLINES)
    if len(password) < 8:
        return render(request, "register.html", error="auth_error_password_short", disciplines=DISCIPLINES)
    if discipline not in DISCIPLINES:
        discipline = "aikijo"

    existing = await db.execute(select(User.id).where(User.email == email))
    if existing.scalar_one_or_none() is not None:
        return render(request, "register.html", error="auth_error_exists", disciplines=DISCIPLINES)
    taken = await db.execute(select(User.id).where(User.username == username))
    if taken.scalar_one_or_none() is not None:
        return render(request, "register.html", error="profile_error_username_taken", disciplines=DISCIPLINES)

    user = User(
        email=email,
        password_hash=await hash_password(password),
        lang=resolve_lang(request),
        username=username,
        discipline=discipline,
    )
    db.add(user)
    await db.commit()
    return _session_response(user)


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user: User | None = Depends(get_current_user)):
    if user:
        return RedirectResponse("/app", status_code=303)
    return render(request, "login.html", error=None)


@router.post("/login")
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


@router.post("/logout")
async def logout():
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response
