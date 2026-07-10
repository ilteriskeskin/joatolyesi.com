from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db import get_db
from app.deps import csrf_protect, require_pro, require_user
from app.models import Enrollment, EnrollmentDay, Program, ProgramDay, User
from app.render import render

router = APIRouter()


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


@router.get("/programs", response_class=HTMLResponse)
async def program_list(request: Request, user: User = Depends(require_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Program).where(Program.is_published).order_by(Program.title_en))
    return render(request, "program_list.html", user=user, programs=list(result.scalars().all()))


@router.get("/programs/{slug}", response_class=HTMLResponse)
async def program_detail(
    slug: str, request: Request, user: User = Depends(require_pro), db: AsyncSession = Depends(get_db)
):
    program = await _get_program(db, slug)
    if program is None:
        return render(request, "404.html", user=user)
    enrollment = await _get_enrollment(db, user, program)
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
    )


@router.post("/programs/{slug}/enroll", dependencies=[Depends(csrf_protect)])
async def enroll(slug: str, request: Request, user: User = Depends(require_pro), db: AsyncSession = Depends(get_db)):
    program = await _get_program(db, slug)
    if program is None:
        return render(request, "404.html", user=user)
    stmt = (
        pg_insert(Enrollment)
        .values(user_id=user.id, program_id=program.id)
        .on_conflict_do_nothing(index_elements=["user_id", "program_id"])
    )
    await db.execute(stmt)
    await db.commit()
    return RedirectResponse(f"/programs/{slug}/day/1", status_code=303)


@router.get("/programs/{slug}/day/{day_number}", response_class=HTMLResponse)
async def program_day(
    slug: str,
    day_number: int,
    request: Request,
    user: User = Depends(require_pro),
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
    )


@router.post("/programs/{slug}/day/{day_number}/complete", dependencies=[Depends(csrf_protect)])
async def complete_day(
    slug: str,
    day_number: int,
    request: Request,
    user: User = Depends(require_pro),
    db: AsyncSession = Depends(get_db),
):
    program = await _get_program(db, slug)
    if program is None or not 1 <= day_number <= program.duration_days:
        return render(request, "404.html", user=user)
    enrollment = await _get_enrollment(db, user, program)
    if enrollment is None:
        return RedirectResponse(f"/programs/{slug}", status_code=303)

    completed = {d.day_number for d in enrollment.completed_days}
    if day_number <= len(completed) + 1:  # kilitli günü tamamlamaya izin verme
        stmt = (
            pg_insert(EnrollmentDay)
            .values(enrollment_id=enrollment.id, day_number=day_number)
            .on_conflict_do_nothing(index_elements=["enrollment_id", "day_number"])
        )
        await db.execute(stmt)
        await db.commit()
    return RedirectResponse(f"/programs/{slug}", status_code=303)
