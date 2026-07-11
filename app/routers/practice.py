import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.constants import DISCIPLINES
from app.db import get_db
from app.deps import csrf_protect, require_user
from app.models import Enrollment, Follow, PracticeLog, User
from app.rate_limit import limiter
from app.badges import compute_badges, compute_belts
from app.render import render
from app.stats import build_heatmap, compute_streak, practice_stats, total_practice_days, weekly_summary

router = APIRouter()


async def dashboard_context(db: AsyncSession, user: User) -> dict:
    streak = await compute_streak(db, user.id)
    practice_days = await total_practice_days(db, user.id)
    stats = await practice_stats(db, user.id)
    belts = compute_belts(practice_days)
    badges = compute_badges(stats["total_sessions"])
    week = await weekly_summary(db, user.id)
    heatmap = await build_heatmap(db, user.id)
    recent = await db.execute(
        select(PracticeLog)
        .where(PracticeLog.user_id == user.id)
        .order_by(PracticeLog.practiced_on.desc(), PracticeLog.created_at.desc())
        .limit(10)
    )
    enrollment_result = await db.execute(
        select(Enrollment)
        .options(selectinload(Enrollment.program), selectinload(Enrollment.completed_days))
        .where(Enrollment.user_id == user.id)
        .order_by(Enrollment.created_at.desc())
        .limit(1)
    )
    enrollment = enrollment_result.scalar_one_or_none()
    current_day = None
    if enrollment:
        current_day = min(len(enrollment.completed_days) + 1, enrollment.program.duration_days)
    # Takip edilenlerin son pratikleri (yalnız herkese açık profiller)
    feed_result = await db.execute(
        select(PracticeLog, User)
        .join(User, PracticeLog.user_id == User.id)
        .join(Follow, Follow.followee_id == User.id)
        .where(Follow.follower_id == user.id, User.is_public)
        .order_by(PracticeLog.practiced_on.desc(), PracticeLog.created_at.desc())
        .limit(15)
    )
    feed = feed_result.all()

    return {
        "feed": feed,
        "streak": streak,
        "belts": belts,
        "badges": badges,
        "week": week,
        "heatmap": heatmap,
        "recent_logs": list(recent.scalars().all()),
        "enrollment": enrollment,
        "current_day": current_day,
        "today": datetime.now(UTC).date().isoformat(),
        "today_max": (datetime.now(UTC).date() + timedelta(days=1)).isoformat(),
        "disciplines": DISCIPLINES,
    }


@router.get("/app", response_class=HTMLResponse)
async def dashboard(request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)):
    ctx = await dashboard_context(db, user)
    return render(request, "dashboard.html", user=user, **ctx)


@router.post("/app/practice", response_class=HTMLResponse, dependencies=[Depends(csrf_protect)])
@limiter.limit("30/minute")
async def log_practice(
    request: Request,
    practiced_on: date = Form(...),
    discipline: str = Form(...),
    minutes: int = Form(...),
    notes: str = Form(""),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    # UTC+14'e kadar dilimlerde kullanıcının "bugün"ü sunucu UTC'sinden bir gün
    # ileride olabilir; o yüzden bir gün tolerans tanınır
    max_date = datetime.now(UTC).date() + timedelta(days=1)
    if discipline not in DISCIPLINES or minutes < 1 or minutes > 600 or practiced_on > max_date:
        ctx = await dashboard_context(db, user)
        return render(request, "_practice_panel.html", user=user, **ctx)

    db.add(
        PracticeLog(
            user_id=user.id,
            practiced_on=practiced_on,
            discipline=discipline,
            minutes=minutes,
            notes=notes.strip()[:2000] or None,
        )
    )
    await db.commit()
    ctx = await dashboard_context(db, user)
    return render(request, "_practice_panel.html", user=user, **ctx)
