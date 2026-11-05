from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analytics import (
    practice_logged_params,
    program_day_complete_params,
    program_enroll_params,
    set_pending_event,
    set_pending_events,
)
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
from app.models import Enrollment, EnrollmentDay, Kata, PracticeLog, Program, ProgramDay, User
from app.render import render
from app.stats import completed_new_day_today
from app.seed import WEEKS

router = APIRouter(dependencies=[Depends(waitlist_gate)])

# Haftalık tema bloğu yalnız bu programda gösterilir (seed.WEEKS tek kaynak)
JO_SUBURI_SLUG = "30-day-jo-suburi"
# Seed'deki odak adı -> aiki-jo teknik slug'ı. Slug doğrudan eşleşmiyorsa buradan;
# burada olmayan ve katalogda da bulunmayan odaklara link verilmez.
FOCUS_SLUG_OVERRIDES = {
    "men uchi gedan gaeshi": "menuchi-gedan-gaeshi",
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


def _week_index(day_number: int) -> int:
    """seed._build_program_days ile aynı: 7'şer günlük haftalar, son hafta 9 gün."""
    return min((day_number - 1) // 7, len(WEEKS) - 1)


def _is_review_day(day_number: int) -> bool:
    return day_number % 7 == 0  # seed: 7, 14, 21, 28


# Program metnindeki süreye göre (normal gün ≈ 5 dk ısınma + 3x20 tekrar ≈ 10-12 dk; tekrar günü 5+10+5 = 20 dk)
DAY_MINUTES = 12
REVIEW_DAY_MINUTES = 20


def _focus_slug(focus: str) -> str:
    focus = focus.strip().lower()
    return FOCUS_SLUG_OVERRIDES.get(focus) or focus.replace(" ", "-")


async def _katas_by_slug(db: AsyncSession, slugs: list[str]) -> dict[str, Kata]:
    result = await db.execute(select(Kata).where(Kata.slug.in_(set(slugs)), Kata.discipline == "aikijo"))
    return {k.slug: k for k in result.scalars().all()}


def _focus_order(first: int, last: int, focuses: list[str]) -> list[str]:
    ordered: list[str] = []
    for day_number in range(first, last + 1):
        if _is_review_day(day_number):
            continue
        focus = focuses[(day_number - 1) % len(focuses)]
        if focus not in ordered:
            ordered.append(focus)
    return ordered


async def _week_blocks(db: AsyncSession) -> list[dict]:
    """Haftalık temalar + odak suburi'ler (katalogda karşılığı varsa kata nesnesiyle)."""
    ranges = [(1, 7), (8, 14), (15, 21), (22, 30)]
    katas = await _katas_by_slug(db, [_focus_slug(f) for _, _, fs in WEEKS for f in fs])
    return [
        {
            "first": first,
            "last": last,
            "theme_en": en,
            "theme_tr": tr,
            # Gösterim sırası: o haftanın günlerinde ilk görünme sırası (WEEKS rotasyonla döner)
            "focuses": [
                {"name": f, "kata": katas.get(_focus_slug(f))}
                for f in _focus_order(first, last, focuses)
            ],
        }
        for (first, last), (en, tr, focuses) in zip(ranges, WEEKS, strict=True)
    ]


async def _focus_kata(db: AsyncSession, day: ProgramDay) -> Kata | None:
    """Gün başlığı "Focus: <teknik>" ise o tekniğin aiki-jo katalog sayfası; yoksa None."""
    prefix = "Focus: "
    if not day.title_en.startswith(prefix):
        return None
    katas = await _katas_by_slug(db, [_focus_slug(day.title_en[len(prefix):])])
    return next(iter(katas.values()), None)


async def _review_katas(db: AsyncSession, day_number: int) -> list[Kata]:
    """Tekrar günü: o haftanın odak katalarının (katalogda olanların) listesi, hafta sırasıyla."""
    focuses = WEEKS[_week_index(day_number)][2]
    katas = await _katas_by_slug(db, [_focus_slug(f) for f in focuses])
    return [katas[_focus_slug(f)] for f in focuses if _focus_slug(f) in katas]


@router.get("/programs", response_class=HTMLResponse)
async def program_list(
    request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    # Ziyaretçiye açık. Nav "Program" linki buraya gelir: tek yayımlı program varsa doğrudan ona gider
    if user is not None and settings.pro_enabled and not is_pro(user):
        raise ProRequired()
    result = await db.execute(select(Program).where(Program.is_published).order_by(Program.title_en))
    programs = list(result.scalars().all())
    if len(programs) == 1:
        qs = f"?{request.url.query}" if request.url.query else ""  # utm/lang düşmesin
        return RedirectResponse(f"/programs/{programs[0].slug}{qs}", status_code=303)
    return render(request, "program_list.html", user=user, programs=programs)


@router.get("/programs/{slug}", response_class=HTMLResponse)
async def program_detail(
    slug: str,
    request: Request,
    done: str | None = Query(default=None),
    user: User | None = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
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
    # Gün tamamlama sonrası ?done=N: "Bugün tamam. Yarın: Gün N+1" mesajı (yalnız gerçekten tamamlanmış gün)
    next_day = None
    done_day = int(done) if done is not None and done.isascii() and done.isdigit() else None  # bozuk değer sessizce yok sayılır
    if done_day is not None and done_day < program.duration_days and enrollment is not None:
        today = datetime.now(UTC).date()
        # Mesaj yalnız o gün bugün tamamlandıysa; eski linkler günler sonra "Yarın" demesin
        if any(d.day_number == done_day and d.completed_at.astimezone(UTC).date() == today
               for d in enrollment.completed_days):
            next_day = program.days[done_day]
    finished = enrollment is not None and len(completed) >= program.duration_days
    opens_tomorrow = enrollment is not None and not finished and completed_new_day_today(enrollment.completed_days)
    is_jo = program.slug == JO_SUBURI_SLUG
    return render(
        request,
        "program_detail.html",
        user=user,
        program=program,
        enrollment=enrollment,
        completed=completed,
        current_day=current_day,
        finished=finished,
        opens_tomorrow=opens_tomorrow,
        weeks=await _week_blocks(db) if is_jo else [],
        day1_kata=await _focus_kata(db, program.days[0]) if is_jo and program.days else None,
        next_day=next_day,
        current_day_obj=program.days[current_day - 1] if current_day else None,
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
    # Takvim kilidi: bugün yeni gün tamamlandıysa sıradaki gün yarın açılır
    opens_tomorrow = day_number == unlocked_until and completed_new_day_today(enrollment.completed_days)
    is_locked = day_number > unlocked_until or opens_tomorrow
    review = _is_review_day(day_number)
    return render(
        request,
        "program_day.html",
        user=user,
        program=program,
        day=day,
        is_completed=day_number in completed,
        is_locked=is_locked,
        opens_tomorrow=opens_tomorrow,
        log_minutes=REVIEW_DAY_MINUTES if review else DAY_MINUTES,
        is_review=review,
        # Kilitli günde video/kata içeriği yok
        focus_kata=None if is_locked or review else await _focus_kata(db, day),
        review_katas=await _review_katas(db, day_number) if review and not is_locked else [],
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
    # kilitli günü tamamlamaya izin verme; bugün zaten yeni gün tamamlandıysa ikinci yeni gün de yok
    is_new = day_number not in completed
    if day_number <= len(completed) + 1 and not (is_new and completed_new_day_today(enrollment.completed_days)):
        stmt = (
            pg_insert(EnrollmentDay)
            .values(enrollment_id=enrollment.id, day_number=day_number)
            .on_conflict_do_nothing(index_elements=["enrollment_id", "day_number"])
        )
        result = await db.execute(stmt)
        events: list[tuple[str, dict]] = []
        if result.rowcount:
            # Program çalışması seriye/dashboard'a sayılsın: günün ilk tamamlanışında bir PracticeLog.
            # Aynı gün başka kayıt olsa da eklenir (dashboard ve kata hızlı kaydı da böyle; seri günleri
            # ayrık tarihle sayar, dakika toplamı gerçek çalışmayı yansıtır). Tekrar tamamlama rowcount=0.
            minutes = REVIEW_DAY_MINUTES if _is_review_day(day_number) else DAY_MINUTES
            focus_kata = None if _is_review_day(day_number) else await _focus_kata(db, program.days[day_number - 1])
            db.add(
                PracticeLog(
                    user_id=user.id,
                    practiced_on=datetime.now(UTC).date(),
                    discipline="aikijo",
                    minutes=minutes,
                    notes=program.title_tr if (user.lang or "tr") == "tr" else program.title_en,
                    kata_slug=focus_kata.slug if focus_kata else None,
                )
            )
            complete_params = program_day_complete_params(slug, day_number)
            if complete_params:
                events.append(("program_day_complete", complete_params))
            practice_params = practice_logged_params("aikijo", minutes, "program")
            if practice_params:
                events.append(("practice_logged", practice_params))
        await db.commit()
        set_pending_events(response, events)
        response.headers["location"] = f"/programs/{slug}?done={day_number}"
    return response


def _kata_program_days() -> dict[str, dict]:
    """Kata slug'ı -> programdaki hafta ve gün numaraları (seed.WEEKS'ten; DB sorgusu yok)."""
    out: dict[str, dict] = {}
    for first, last in [(1, 7), (8, 14), (15, 21), (22, 30)]:
        week = _week_index(first) + 1
        _, _, focuses = WEEKS[week - 1]
        for day_number in range(first, last + 1):
            if _is_review_day(day_number):
                continue
            slug = _focus_slug(focuses[(day_number - 1) % len(focuses)])
            entry = out.setdefault(slug, {"week": week, "days": []})
            entry["days"].append(day_number)
    return out


KATA_PROGRAM_DAYS = _kata_program_days()
