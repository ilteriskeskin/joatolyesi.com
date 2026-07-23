import uuid
from datetime import UTC, date, datetime, timedelta

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.constants import SELECTABLE_DISCIPLINES
from app.db import get_db
from app.deps import csrf_protect, require_user, waitlist_gate
from app.models import Enrollment, PracticeLog, User
from app.rate_limit import limiter
from app.badges import BELTS, compute_badges, compute_belts
from app.render import render
from app.stats import (
    FREEZES_PER_MONTH,
    REST_DAYS_PER_WEEK,
    build_heatmap,
    compute_longest_streak,
    practice_stats,
    rest_days_used_this_week,
    streak_info,
    total_practice_days,
    weekly_summary,
)

router = APIRouter(dependencies=[Depends(waitlist_gate)])


async def dashboard_context(db: AsyncSession, user: User) -> dict:
    sinfo = await streak_info(db, user.id)
    longest_streak = await compute_longest_streak(db, user.id)
    practice_days = await total_practice_days(db, user.id)
    stats = await practice_stats(db, user.id)
    belts = compute_belts(practice_days)
    badges = compute_badges(stats["total_sessions"])
    week = await weekly_summary(db, user.id)
    heatmap = await build_heatmap(db, user.id)
    rest_days_left = max(0, REST_DAYS_PER_WEEK - await rest_days_used_this_week(db, user.id))
    recent = await db.execute(
        select(PracticeLog)
        .where(PracticeLog.user_id == user.id)
        .order_by(PracticeLog.practiced_on.desc(), PracticeLog.created_at.desc())
        .limit(10)
    )
    referral_count = (
        await db.execute(select(func.count(User.id)).where(User.referred_by == user.referral_code))
    ).scalar_one()

    enrollment = None
    current_day = None
    if settings.pro_enabled:  # Pro kapalıyken program kaydı olsa bile banner gösterilmez
        enrollment_result = await db.execute(
            select(Enrollment)
            .options(selectinload(Enrollment.program), selectinload(Enrollment.completed_days))
            .where(Enrollment.user_id == user.id)
            .order_by(Enrollment.created_at.desc())
            .limit(1)
        )
        enrollment = enrollment_result.scalar_one_or_none()
        if enrollment:
            current_day = min(len(enrollment.completed_days) + 1, enrollment.program.duration_days)

    return {
        "streak": sinfo["streak"],
        "longest_streak": max(longest_streak, sinfo["streak"]),
        "freezes_left": sinfo["freezes_left"],
        "freezes_total": FREEZES_PER_MONTH,
        "rest_days_left": rest_days_left,
        "rest_days_total": REST_DAYS_PER_WEEK,
        "practice_days": practice_days,
        "belts": belts,
        "badges": badges,
        "week": week,
        "heatmap": heatmap,
        "recent_logs": list(recent.scalars().all()),
        "enrollment": enrollment,
        "current_day": current_day,
        "today": datetime.now(UTC).date().isoformat(),
        "today_max": (datetime.now(UTC).date() + timedelta(days=1)).isoformat(),
        "disciplines": SELECTABLE_DISCIPLINES,
        "referral_link": f"{settings.base_url}/?ref={user.referral_code}",
        "referral_count": referral_count,
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
    if discipline not in SELECTABLE_DISCIPLINES or minutes < 1 or minutes > 600 or practiced_on > max_date:
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
    # Bu kayıt tam bir kuşak eşiğine denk geldiyse kutlama/paylaşım anı göster
    # (sadece bu POST cevabında — sayfayı tekrar açınca bir daha çıkmaz)
    milestone_belt = next((belt_id for belt_id, n in BELTS if n > 0 and n == ctx["practice_days"]), None)
    return render(request, "_practice_panel.html", user=user, milestone=milestone_belt, **ctx)


@router.post("/app/rest-day", response_class=HTMLResponse, dependencies=[Depends(csrf_protect)])
@limiter.limit("30/minute")
async def log_rest_day(
    request: Request,
    practiced_on: date = Form(...),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Planlı dinlenme günü işaretle: haftalık kota içindeyse ve o günde
    zaten kayıt yoksa seriyi bozmayan bir gün ekler."""
    today = datetime.now(UTC).date()
    max_date = today + timedelta(days=1)
    min_date = today - timedelta(days=today.weekday())  # bu haftanın pazartesisi
    already_used = await rest_days_used_this_week(db, user.id)
    existing = await db.execute(
        select(PracticeLog.id).where(PracticeLog.user_id == user.id, PracticeLog.practiced_on == practiced_on)
    )
    can_add = (
        min_date <= practiced_on <= max_date
        and already_used < REST_DAYS_PER_WEEK
        and existing.scalar_one_or_none() is None
    )
    if can_add:
        db.add(
            PracticeLog(
                user_id=user.id,
                practiced_on=practiced_on,
                is_rest_day=True,
            )
        )
        await db.commit()
    ctx = await dashboard_context(db, user)
    return render(request, "_practice_panel.html", user=user, **ctx)
