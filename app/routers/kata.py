import json
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.routers.programs import KATA_PROGRAM_DAYS
from app.analytics import PRACTICE_SOURCES, practice_logged_params, set_pending_event
from app.constants import SELECTABLE_DISCIPLINES
from app.db import get_db
from app.config import settings
from app.guide_content import GUIDE
from app.deps import ProRequired, csrf_protect, get_current_user, is_pro, require_user, waitlist_gate
from app.models import Kata, PracticeLog, User
from app.rate_limit import limiter
from app.render import render
from app.routers.practice import dashboard_context

router = APIRouter(dependencies=[Depends(waitlist_gate)])


@router.get("/kata", response_class=HTMLResponse)
async def kata_list(request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Sekmeler seçilebilir branşlardan gelir (SELECTABLE_DISCIPLINES).
    available_result = await db.execute(
        select(Kata.discipline).where(Kata.discipline.in_(SELECTABLE_DISCIPLINES)).distinct()
    )
    available = sorted(available_result.scalars().all())

    # Varsayılan görünüm kullanıcının branşı; ?d= ile diğerlerine geçilir
    d = request.query_params.get("d")
    if d == "all":
        selected = None
    elif d in available:
        selected = d
    else:
        selected = user.discipline if user and user.discipline in available else None

    # Kata / teknik sekmesi — branş seçiliyken anlamlı, "tümü" görünümünde karışık kalır
    kind = request.query_params.get("kind")
    if kind not in ("kata", "teknik"):
        kind = "kata"

    stmt = select(Kata).where(Kata.discipline.in_(SELECTABLE_DISCIPLINES)).order_by(Kata.sort_order, Kata.title_en)
    if selected:
        stmt = stmt.where(Kata.discipline == selected, Kata.kind == kind)
    # Listede her zaman tüm katalog görünür (kilitliyse rozetiyle); gerçek
    # erişim kontrolü sadece detay sayfasında (kata_detail) yapılır — Pro
    # kapalıyken zaten herkese açık, açılınca kilitliler orada engellenir.
    result = await db.execute(stmt)
    katas = list(result.scalars().all())

    # Seçili branşta bu türde hiç içerik yoksa (ör. aikido'da kata) diğer türü öner
    other_kind_has_content = False
    if selected and not katas:
        other = "teknik" if kind == "kata" else "kata"
        count = await db.execute(
            select(func.count(Kata.id)).where(Kata.discipline == selected, Kata.kind == other)
        )
        other_kind_has_content = count.scalar_one() > 0

    return render(
        request,
        "kata_list.html",
        user=user,
        katas=katas,
        available=available,
        selected=selected,
        kind=kind,
        other_kind_has_content=other_kind_has_content,
    )


@router.get("/kata/{slug}", response_class=HTMLResponse)
async def kata_detail(
    slug: str, request: Request, user: User | None = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return render(request, "404.html", user=user)
    # Pro kapalıyken ödeme duvarı yok, is_free ayrımı uygulanmaz — herkes
    # her şeyi görür. Pro açılınca kilitli içerik yine gerçek abonelik ister.
    if settings.pro_enabled and not kata.is_free and not is_pro(user):
        if user is None:
            return RedirectResponse("/login", status_code=303)
        raise ProRequired()
    logged = request.query_params.get("logged") == "1"
    repeat_count = 0
    if user is not None:
        repeat_count = (
            await db.execute(
                select(func.count(PracticeLog.id)).where(
                    PracticeLog.user_id == user.id, PracticeLog.kata_slug == slug
                )
            )
        ).scalar_one()
    # İlgili katalar: aynı branş + tür, farklı slug — SEO iç linklemesi ve keşif için
    related_result = await db.execute(
        select(Kata)
        .where(Kata.discipline == kata.discipline, Kata.kind == kata.kind, Kata.slug != kata.slug)
        .order_by(Kata.sort_order, Kata.title_en)
        .limit(6)
    )
    related = list(related_result.scalars().all())
    return render(
        request, "kata_detail.html", user=user, kata=kata, logged=logged,
        repeat_count=repeat_count, related=related,
        guide_available=kata.discipline in GUIDE,
        in_program=KATA_PROGRAM_DAYS.get(kata.slug) if kata.discipline == "aikijo" else None,
    )


@router.post("/kata/{slug}/log", dependencies=[Depends(csrf_protect)])
@limiter.limit("30/minute")
async def kata_quick_log(
    slug: str,
    request: Request,
    minutes: int = Form(20, ge=1, le=600),
    source: str = Form(""),
    user: User = Depends(require_user),
    db: AsyncSession = Depends(get_db),
):
    """Kata sayfasından tek tuşla pratik kaydı: kütüphaneyi pasif arşivden
    aktif antrenman aracına çevirir."""
    result = await db.execute(select(Kata).where(Kata.slug == slug))
    kata = result.scalar_one_or_none()
    if kata is None:
        return render(request, "404.html", user=user)
    if settings.pro_enabled and not kata.is_free and not is_pro(user):
        raise ProRequired()
    db.add(
        PracticeLog(
            user_id=user.id,
            practiced_on=datetime.now(UTC).date(),
            discipline=kata.discipline,
            minutes=minutes,
            notes=kata.title_tr if (user.lang or "tr") == "tr" else kata.title_en,
            kata_slug=kata.slug,
        )
    )
    await db.commit()
    # Dashboard "Günün tekniği" kartı (HTMX): panel yerinde güncellenir, sayfa değişmez
    if source == "daily_kata" and request.headers.get("HX-Request"):
        ctx = await dashboard_context(db, user, request)
        panel = render(request, "_practice_panel.html", user=user, daily_logged=True, **ctx)
        params = practice_logged_params(kata.discipline, minutes, "daily_kata")
        if params:
            panel.headers["HX-Trigger"] = json.dumps({"joryu:practice-logged": params})
        return panel
    # İlk seans kartından gelen kayıt dashboard'a döner (seri hemen görünür);
    # geçersiz source sessizce yok sayılır
    first_session = source == "first_session" and source in PRACTICE_SOURCES
    target = "/app?logged=1" if first_session else f"/kata/{slug}?logged=1"
    response = RedirectResponse(target, status_code=303)
    # GA4 practice_logged: ?logged=1 yenilense de olay yalnız bir kez gider
    params = practice_logged_params(kata.discipline, minutes, "first_session" if first_session else "kata")
    if params:
        set_pending_event(response, "practice_logged", params)
    return response
