from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.deps import AuthRequired, ProRequired

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.env, traces_sample_rate=0)
from app.rate_limit import limiter
from app.routers import admin, auth, billing, blog, guide, kata, landing, practice, profile, programs
from app.seed import seed_content

app = FastAPI(title="Joryu")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(landing.router)
if not settings.waitlist_only:
    app.include_router(guide.router)  # rehber halka açık (giriş istemez) ama lansmanla gelir
    app.include_router(auth.router)
    app.include_router(blog.router)
    app.include_router(practice.router)
    app.include_router(kata.router)
    app.include_router(programs.router)
    app.include_router(billing.router)
    app.include_router(profile.router)
    app.include_router(admin.router)


@app.exception_handler(AuthRequired)
async def auth_required_handler(request: Request, exc: AuthRequired) -> RedirectResponse:
    return RedirectResponse("/login", status_code=303)


@app.exception_handler(ProRequired)
async def pro_required_handler(request: Request, exc: ProRequired) -> RedirectResponse:
    return RedirectResponse("/billing", status_code=303)


@app.on_event("startup")
async def on_startup() -> None:
    if not settings.waitlist_only:
        await seed_content()
