import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import DISCIPLINES
from app.db import get_db
from app.deps import csrf_protect, get_current_user, require_user
from app.models import User
from app.rate_limit import limiter
from app.render import render
from app.badges import compute_badges, compute_belts, current_belt
from app.stats import build_heatmap, compute_streak, practice_day_counts, practice_stats, total_practice_days

router = APIRouter()

USERNAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,28}[a-z0-9]$")


@router.get("/profile", response_class=HTMLResponse)
async def profile_edit(request: Request, user: User = Depends(require_user)):
    return render(request, "profile_edit.html", user=user, disciplines=DISCIPLINES, error=None, saved=False)


@router.post("/profile", response_class=HTMLResponse, dependencies=[Depends(csrf_protect)])
async def profile_save(
    request: Request,
    username: str = Form(...),
    display_name: str = Form(""),
    bio: str = Form(""),
    discipline: str = Form("jo"),
    is_public: str = Form(""),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    username = username.strip().lower()
    if not USERNAME_RE.match(username):
        return render(
            request, "profile_edit.html", user=user, disciplines=DISCIPLINES,
            error="profile_error_username_invalid", saved=False,
        )
    if username != user.username:
        taken = await db.execute(select(User.id).where(User.username == username, User.id != user.id))
        if taken.scalar_one_or_none() is not None:
            return render(
                request, "profile_edit.html", user=user, disciplines=DISCIPLINES,
                error="profile_error_username_taken", saved=False,
            )

    user.username = username
    user.display_name = display_name.strip()[:80] or None
    user.bio = bio.strip()[:500] or None
    user.discipline = discipline if discipline in DISCIPLINES else user.discipline
    user.is_public = is_public == "on"
    await db.commit()
    return render(request, "profile_edit.html", user=user, disciplines=DISCIPLINES, error=None, saved=True)


@router.get("/practitioners", response_class=HTMLResponse)
@limiter.limit("30/minute")
async def practitioners(
    request: Request,
    user: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    q = (request.query_params.get("q") or "").strip()[:80]
    stmt = select(User).where(User.is_public, User.username.is_not(None))
    if q:
        like = f"%{q.lower()}%"
        stmt = stmt.where(or_(User.username.ilike(like), User.display_name.ilike(like)))
    stmt = stmt.order_by(User.created_at.desc()).limit(50)
    result = await db.execute(stmt)
    people = list(result.scalars().all())
    day_counts = await practice_day_counts(db, [p.id for p in people])
    belts = {p.id: current_belt(day_counts.get(p.id, 0)) for p in people}
    return render(request, "practitioners.html", user=user, people=people, belts=belts, q=q)


@router.get("/u/{username}", response_class=HTMLResponse)
async def public_profile(
    username: str,
    request: Request,
    viewer: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(User).where(User.username == username.lower()))
    person = result.scalar_one_or_none()
    is_owner = viewer is not None and person is not None and viewer.id == person.id
    if person is None or (not person.is_public and not is_owner):
        return render(request, "404.html", user=viewer)

    streak = await compute_streak(db, person.id)
    practice_days = await total_practice_days(db, person.id)
    stats = await practice_stats(db, person.id)
    belts = [b for b in compute_belts(practice_days) if b.earned]
    badges = [b for b in compute_badges(stats["total_sessions"]) if b.earned]
    heatmap = await build_heatmap(db, person.id)
    return render(
        request,
        "profile_public.html",
        user=viewer,
        person=person,
        is_owner=is_owner,
        streak=streak,
        belts=belts,
        badges=badges,
        heatmap=heatmap,
        **stats,
    )
