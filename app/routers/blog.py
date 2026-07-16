"""Topluluk blogu: yazma girişli, okuma ve keşfet herkese açık."""

import re
import unicodedata
import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constants import DISCIPLINES
from app.db import get_db
from app.deps import csrf_protect, get_current_user, require_user, waitlist_gate
from app.markdown_utils import markdown_excerpt, render_markdown
from app.models import Post, User
from app.rate_limit import limiter
from app.render import render

router = APIRouter(dependencies=[Depends(waitlist_gate)])

TITLE_MIN, BODY_MIN = 5, 100


def _slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title.lower())
    text = text.replace("ı", "i").replace("ğ", "g").replace("ş", "s").replace("ç", "c").replace("ö", "o").replace("ü", "u")
    text = re.sub(r"[^a-z0-9]+", "-", text.encode("ascii", "ignore").decode()).strip("-")
    return f"{text[:60].rstrip('-') or 'yazi'}-{uuid.uuid4().hex[:6]}"


@router.get("/blog", response_class=HTMLResponse)
@limiter.limit("60/minute")
async def blog_list(
    request: Request,
    user: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    q = (request.query_params.get("q") or "").strip()[:80]
    d = request.query_params.get("d")
    selected = d if d in DISCIPLINES else None

    stmt = select(Post).options(selectinload(Post.author)).order_by(Post.created_at.desc()).limit(30)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(or_(Post.title.ilike(like), Post.body.ilike(like)))
    if selected:
        stmt = stmt.where(Post.discipline == selected)
    result = await db.execute(stmt)
    posts = list(result.scalars().all())
    excerpts = {p.id: markdown_excerpt(p.body) for p in posts}
    return render(
        request, "blog_list.html", user=user,
        posts=posts, excerpts=excerpts, q=q, selected=selected, disciplines=DISCIPLINES,
    )


@router.get("/blog/yeni", response_class=HTMLResponse)
async def blog_new(request: Request, user: User = Depends(require_user)):
    return render(request, "blog_form.html", user=user, post=None, disciplines=DISCIPLINES, error=None)


@router.post("/blog/yeni", dependencies=[Depends(csrf_protect)])
@limiter.limit("5/hour")
async def blog_create(
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    discipline: str = Form(""),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    title, body = title.strip()[:140], body.strip()[:20000]
    if len(title) < TITLE_MIN or len(body) < BODY_MIN:
        return render(request, "blog_form.html", user=user, post=None,
                      disciplines=DISCIPLINES, error="blog_error_short",
                      draft_title=title, draft_body=body)
    post = Post(
        user_id=user.id,
        slug=_slugify(title),
        title=title,
        body=body,
        discipline=discipline if discipline in DISCIPLINES else None,
    )
    db.add(post)
    await db.commit()
    return RedirectResponse(f"/blog/{post.slug}", status_code=303)


@router.get("/blog/{slug}", response_class=HTMLResponse)
async def blog_read(
    slug: str,
    request: Request,
    user: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).options(selectinload(Post.author)).where(Post.slug == slug))
    post = result.scalar_one_or_none()
    if post is None:
        return render(request, "404.html", user=user)
    is_owner = user is not None and user.id == post.user_id
    return render(request, "blog_post.html", user=user, post=post,
                  body_html=render_markdown(post.body),
                  excerpt=markdown_excerpt(post.body, 150), is_owner=is_owner)


@router.get("/blog/{slug}/duzenle", response_class=HTMLResponse)
async def blog_edit(
    slug: str, request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Post).where(Post.slug == slug, Post.user_id == user.id))
    post = result.scalar_one_or_none()
    if post is None:
        return render(request, "404.html", user=user)
    return render(request, "blog_form.html", user=user, post=post, disciplines=DISCIPLINES, error=None)


@router.post("/blog/{slug}/duzenle", dependencies=[Depends(csrf_protect)])
@limiter.limit("30/hour")
async def blog_update(
    slug: str,
    request: Request,
    title: str = Form(...),
    body: str = Form(...),
    discipline: str = Form(""),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Post).where(Post.slug == slug, Post.user_id == user.id))
    post = result.scalar_one_or_none()
    if post is None:
        return render(request, "404.html", user=user)
    title, body = title.strip()[:140], body.strip()[:20000]
    if len(title) < TITLE_MIN or len(body) < BODY_MIN:
        return render(request, "blog_form.html", user=user, post=post,
                      disciplines=DISCIPLINES, error="blog_error_short")
    post.title = title
    post.body = body
    post.discipline = discipline if discipline in DISCIPLINES else None
    post.updated_at = datetime.now(UTC)
    await db.commit()
    return RedirectResponse(f"/blog/{post.slug}", status_code=303)


@router.post("/blog/{slug}/sil", dependencies=[Depends(csrf_protect)])
async def blog_delete(
    slug: str, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Post).where(Post.slug == slug, Post.user_id == user.id))
    post = result.scalar_one_or_none()
    if post is not None:
        await db.delete(post)
        await db.commit()
    return RedirectResponse("/blog", status_code=303)
