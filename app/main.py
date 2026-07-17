from starlette.staticfiles import StaticFiles as _StarletteStaticFiles
from starlette.types import Scope

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.deps import AuthRequired, ProRequired, WaitlistGate

if settings.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(dsn=settings.sentry_dsn, environment=settings.env, traces_sample_rate=0)
from app.rate_limit import limiter
from app.routers import admin, auth, billing, blog, guide, kata, landing, practice, profile, programs, push
from app.seed import seed_content

# fonts/ ve js/vendor/ içeriği versiyonlanmış üçüncü taraf kütüphaneler —
# değişmeyecekleri için tarayıcıda uzun süre cache'lenebilir (istek sayısını
# ve sunucu yükünü düşürür, 512MB'lık VPS'te önemli).
_LONG_CACHE_PREFIXES = ("fonts/", "js/vendor/")


class CachedStaticFiles(_StarletteStaticFiles):
    def file_response(self, full_path, stat_result, scope: Scope, status_code: int = 200):
        response = super().file_response(full_path, stat_result, scope, status_code)
        path = scope.get("path", "")
        if any(f"/static/{p}" in path for p in _LONG_CACHE_PREFIXES):
            response.headers["cache-control"] = "public, max-age=31536000, immutable"
        if path == "/static/sw.js":
            # sw.js /static/ altında yaşıyor ama tüm siteyi (scope: "/")
            # kontrol etmesi isteniyor — tarayıcı bunu bu header olmadan
            # reddeder (push bildirimleri hiçbir sayfada calışmazdı).
            response.headers["service-worker-allowed"] = "/"
        return response


app = FastAPI(title="Joryu", docs_url=None, redoc_url=None, openapi_url=None)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.mount("/static", CachedStaticFiles(directory="app/static"), name="static")

app.include_router(landing.router)
app.include_router(admin.router)  # token korumalı; waitlist aşamasında da erişilebilir olmalı
# Bu rotalar her zaman register edilir; WAITLIST_ONLY=true iken her birinin
# kendi waitlist_gate bağımlılığı devreye girer (admin önizleme çerezi hariç).
app.include_router(guide.router)
app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(practice.router)
app.include_router(kata.router)
app.include_router(profile.router)
app.include_router(push.router)
if settings.pro_enabled:
    app.include_router(programs.router)  # kapalıyken programlar tamamen gizli
    app.include_router(billing.router)  # kapalıyken /billing ve webhook da kapanır


@app.exception_handler(AuthRequired)
async def auth_required_handler(request: Request, exc: AuthRequired) -> RedirectResponse:
    return RedirectResponse("/login", status_code=303)


@app.exception_handler(ProRequired)
async def pro_required_handler(request: Request, exc: ProRequired) -> RedirectResponse:
    return RedirectResponse("/billing", status_code=303)


@app.exception_handler(WaitlistGate)
async def waitlist_gate_handler(request: Request, exc: WaitlistGate) -> RedirectResponse:
    return RedirectResponse("/", status_code=303)


@app.on_event("startup")
async def on_startup() -> None:
    await seed_content()  # idempotent upsert; admin önizlemesi için de veriye ihtiyaç var
