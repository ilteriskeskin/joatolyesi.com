import csv
import io
import re

from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import get_db
from app.deps import csrf_protect, get_current_user
from app.i18n.strings import DEFAULT_LANG, SUPPORTED_LANGS, get_strings
from app.models import User, Waitlist
from app.rate_limit import limiter
from app.render import render

router = APIRouter()

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
SOURCE_RE = re.compile(r"^[a-z]{2,10}$")


@router.get("/", response_class=HTMLResponse)
async def index(
    request: Request,
    src: str | None = Query(default=None),
    user: User | None = Depends(get_current_user),
):
    return render(request, "index.html", user=user, source=src if src and SOURCE_RE.match(src) else "")


@router.get("/robots.txt")
async def robots():
    return Response(
        f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {settings.base_url}/sitemap.xml\n",
        media_type="text/plain",
    )


@router.get("/sitemap.xml")
async def sitemap():
    paths = ["/", "/privacy", "/terms"]
    if not settings.waitlist_only:
        from app.guide_content import GUIDE

        paths += ["/guide", "/blog"] + [f"/guide/{d}" for d in GUIDE]
    urls = "".join(f"<url><loc>{settings.base_url}{p}</loc></url>" for p in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, media_type="application/xml")


@router.get("/privacy", response_class=HTMLResponse)
async def privacy(request: Request, user: User | None = Depends(get_current_user)):
    return render(request, "privacy.html", user=user)


@router.get("/terms", response_class=HTMLResponse)
async def terms(request: Request, user: User | None = Depends(get_current_user)):
    return render(request, "terms.html", user=user)


@router.post("/waitlist", response_class=HTMLResponse, dependencies=[Depends(csrf_protect)])
@limiter.limit("5/minute")
async def join_waitlist(request: Request, db: AsyncSession = Depends(get_db)):
    form = await request.form()
    email = str(form.get("email", "")).strip().lower()
    lang = str(form.get("lang", DEFAULT_LANG))
    source = str(form.get("source", "")).strip().lower()

    resolved_lang = lang if lang in SUPPORTED_LANGS else DEFAULT_LANG
    strings = get_strings(resolved_lang)

    if not EMAIL_RE.match(email):
        return HTMLResponse(
            f'<p class="form-message form-message--error">{strings["form_error_invalid"]}</p>',
            status_code=422,
        )

    clean_source = source if SOURCE_RE.match(source) else None

    stmt = (
        pg_insert(Waitlist)
        .values(email=email, lang=resolved_lang, source=clean_source)
        .on_conflict_do_nothing(index_elements=["email"])
    )
    result = await db.execute(stmt)
    await db.commit()

    # Çakışmada insert olmaz (rowcount 0) — kayıt zaten var, kullanıcıya söyle
    if result.rowcount == 0:
        return HTMLResponse(f'<p class="form-message form-message--success">{strings["form_already"]}</p>')

    return HTMLResponse(f'<p class="form-message form-message--success">{strings["form_success"]}</p>')


@router.get("/admin/waitlist")
async def admin_waitlist(token: str = Query(...), db: AsyncSession = Depends(get_db)):
    if token != settings.admin_token:
        return Response(status_code=404)

    result = await db.execute(select(Waitlist).order_by(Waitlist.created_at.desc()))
    rows = result.scalars().all()

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["email", "lang", "source", "created_at"])
    for row in rows:
        writer.writerow([row.email, row.lang, row.source or "", row.created_at.isoformat()])
    buffer.seek(0)

    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=waitlist.csv"},
    )
