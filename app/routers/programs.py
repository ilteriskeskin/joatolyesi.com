from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analytics import program_day_complete_params, program_enroll_params, set_pending_event
from app.config import settings
from app.db import get_db
from app.deps import (
    ProRequired,
    csrf_protect,
    get_current_user,
    is_pro,
    require_program_access,
    require_user,
    waitlist_gate,
)
from app.models import Enrollment, EnrollmentDay, Kata, Program, ProgramDay, User
from app.render import render
from app.seed import WEEKS

router = APIRouter(dependencies=[Depends(waitlist_gate)])

# Haftalık tema bloğu yalnız bu programda gösterilir (seed.WEEKS tek kaynak)
JO_SUBURI_SLUG = "30-day-jo-suburi"
# Seed'deki odak adı -> aiki-jo teknik/kata slug'ı. Slug doğrudan eşleşmiyorsa buradan;
# burada olmayan ve katalogda da bulunmayan odaklara (ör. "free flow combinations") link verilmez.
FOCUS_SLUG_OVERRIDES = {
    "31-count kata (sections)": "sanjuichi-no-jo",
    "full kata runs": "sanjuichi-no-jo",
}


async def _get_program(db: AsyncSession, slug: str) -> Program | None:
    result = await db.execute(
        select(Program).options(selectinload(Program.days)).where(Program.slug == slug, Program.is_published)
    )
    return result.scalar_one_or_none()


async def _get_enrollment(db: AsyncSession, user: User, program: Program) -> Enrollment | None:
    result = await db.execute(
        select(Enrollment)
        .options(selectinload(Enrollment.completed_days))
        .where(Enrollment.user_id == user.id, Enrollment.program_id == program.id)
    )
    return result.scalar_one_or_none()


def _week_blocks() -> list[dict]:
    """Haftalık temalar: gün aralıkları seed._build_program_days ile aynı (7+7+7+9)."""
    ranges = [(1, 7), (8, 14), (15, 21), (22, 30)]
    return [
        {"first": first, "last": last, "theme_en": en, "theme_tr": tr, "focuses": focuses}
        for (first, last), (en, tr, focuses) in zip(ranges, WEEKS, strict=True)
    ]


async def _focus_kata(db: AsyncSession, day: ProgramDay) -> Kata | None:
    """Gün başlığı "Focus: <teknik>" ise o tekniğin aiki-jo katalog sayfası; yoksa None."""
    prefix = "Focus: "
    if not day.title_en.startswith(prefix):
        return None
    focus = day.title_en[len(prefix):].strip().lower()
    slug = FOCUS_SLUG_OVERRIDES.get(focus) or focus.replace(" ", "-")
    result = await db.execute(select(Kata).where(Kata.slug == slug, Kata.discipline == "aikijo"))
    return result.scalar_one_or_none()


@router.get("/programs", response_class=HTMLResponse)
async def program_list(request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Program).where(Program.is_published).order_by(Program.title_en))
    return render(request, "program_list.html", user=user, programs=list(result.scalars().all()))


@router.get("/programs/{slug}", response_class=HTMLResponse)
async def program_detail(
    slug: str, request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    # Ziyaretçiye açık (Instagram açılış sayfası); Pro açıkken girişli Pro olmayan kullanıcı eskisi gibi /billing'e gider
    if user is not None and settings.pro_enabled and not is_pro(user):
        raise ProRequired()
    program = await _get_program(db, slug)
    if program is None:
        return render(request, "404.html", user=user)
    enrollment = await _get_enrollment(db, user, program) if user else None
    completed = {d.day_number for d in enrollment.completed_days} if enrollment else set()
    current_day = min(len(completed) + 1, program.duration_days) if enrollment else None
    return render(
        request,
        "program_detail.html",
        user=user,
        program=program,
        enrollment=enrollment,
        completed=completed,
        current_day=current_day,
        finished=enrollment is not None and len(completed) >= program.duration_days,
        weeks=_week_blocks() if program.slug == JO_SUBURI_SLUG else [],
    )


@router.post("/programs/{slug}/enroll", dependencies=[Depends(csrf_protect)])
async def enroll(slug: str, request: Request, user: User = Depends(require_program_access), db: AsyncSession = Depends(get_db)):
    program = await _get_program(db, slug)
    if program is None:
        return render(request, "404.html", user=user)
    stmt = (
        pg_insert(Enrollment)
        .values(user_id=user.id, program_id=program.id)
        .on_conflict_do_nothing(index_elements=["user_id", "program_id"])
    )
    result = await db.execute(stmt)
    await db.commit()
    response = RedirectResponse(f"/programs/{slug}/day/1", status_code=303)
    params = program_enroll_params(slug)
    if result.rowcount and params:  # yalnız yeni kayıtta; tekrar POST olayı çoğaltmaz
        set_pending_event(response, "program_enroll", params)
    return response


@router.get("/programs/{slug}/day/{day_number}", response_class=HTMLResponse)
async def program_day(
    slug: str,
    day_number: int,
    request: Request,
    user: User = Depends(require_program_access),
    db: AsyncSession = Depends(get_db),
):
    program = await _get_program(db, slug)
    if program is None or not 1 <= day_number <= program.duration_days:
        return render(request, "404.html", user=user)
    enrollment = await _get_enrollment(db, user, program)
    if enrollment is None:
        return RedirectResponse(f"/programs/{slug}", status_code=303)

    completed = {d.day_number for d in enrollment.completed_days}
    unlocked_until = len(completed) + 1  # günler sırayla açılır
    day: ProgramDay = program.days[day_number - 1]
    return render(
        request,
        "program_day.html",
        user=user,
        program=program,
        day=day,
        is_completed=day_number in completed,
        is_locked=day_number > unlocked_until,
        focus_kata=await _focus_kata(db, day) if day_number <= unlocked_until else None,
    )


@router.post("/programs/{slug}/day/{day_number}/complete", dependencies=[Depends(csrf_protect)])
async def complete_day(
    slug: str,
    day_number: int,
    request: Request,
    user: User = Depends(require_program_access),
    db: AsyncSession = Depends(get_db),
):
    program = await _get_program(db, slug)
    if program is None or not 1 <= day_number <= program.duration_days:
        return render(request, "404.html", user=user)
    enrollment = await _get_enrollment(db, user, program)
    if enrollment is None:
        return RedirectResponse(f"/programs/{slug}", status_code=303)

    response = RedirectResponse(f"/programs/{slug}", status_code=303)
    completed = {d.day_number for d in enrollment.completed_days}
    if day_number <= len(completed) + 1:  # kilitli günü tamamlamaya izin verme
        stmt = (
            pg_insert(EnrollmentDay)
            .values(enrollment_id=enrollment.id, day_number=day_number)
            .on_conflict_do_nothing(index_elements=["enrollment_id", "day_number"])
        )
        result = await db.execute(stmt)
        await db.commit()
        params = program_day_complete_params(slug, day_number)
        if result.rowcount and params:
            set_pending_event(response, "program_day_complete", params)
    return response
