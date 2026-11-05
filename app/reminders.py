"""Hatırlatma maili içeriği (scripts/send_reminders.py) ve abonelikten çıkma
bağlantısı. Kişiselleştirme sırası:
  (a) programa kayıtlı + bugün yeni gün açık -> "Bugün: Gün N — Odak: X"
  (b) "bugün son gün" durumu -> seri uyarısı (a'da da ek satır olarak girer)
  (c) aksi halde günün tekniği + "10 dk yeter"
Sayı yalnız gerçek seri değeridir; uydurma sayı yok."""

import html as _html
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.daily import pick_daily_kata
from app.deps import is_pro
from app.i18n.strings import get_strings
from app.models import Enrollment, ProgramDay, User
from app.security import create_unsub_token
from app.stats import completed_new_day_today


def unsubscribe_url(user: User) -> str:
    return f"{settings.base_url}/unsubscribe?t={create_unsub_token(user.id)}"


def unsubscribe_headers(user: User) -> dict[str, str]:
    """RFC 8058 tek tıkla çıkış: posta istemcisi POST atar."""
    return {
        "List-Unsubscribe": f"<{unsubscribe_url(user)}>",
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    }


async def _open_program_day(db: AsyncSession, user: User) -> tuple[Enrollment, ProgramDay | None, int] | None:
    """Bugün açık yeni program günü: (kayıt, gün, gün no) ya da None."""
    if settings.pro_enabled and not is_pro(user):
        return None
    enrollment = (
        await db.execute(
            select(Enrollment)
            .options(selectinload(Enrollment.program), selectinload(Enrollment.completed_days))
            .where(Enrollment.user_id == user.id)
            .order_by(Enrollment.created_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    if enrollment is None:
        return None
    done = len(enrollment.completed_days)
    if done >= enrollment.program.duration_days or completed_new_day_today(enrollment.completed_days):
        return None
    number = done + 1
    day = (
        await db.execute(
            select(ProgramDay).where(ProgramDay.program_id == enrollment.program_id, ProgramDay.day_number == number)
        )
    ).scalar_one_or_none()
    return enrollment, day, number


async def select_reminder(db: AsyncSession, user: User, today: date, info: dict) -> dict:
    """Mail ve push ortak seçim: kind + gereken alanlar. info: stats.streak_info."""
    lang = user.lang or "tr"
    last_day = bool(info.get("last_day"))
    freeze = bool(info.get("last_day_freeze"))
    opened = await _open_program_day(db, user)
    if opened is not None:
        enrollment, day, number = opened
        t = get_strings(lang)
        if day is not None:
            focus = t["program_review_label"] if number % 7 == 0 else (day.title_en if lang == "en" else day.title_tr)
            return {"kind": "program", "n": number, "focus": focus, "last_day": last_day, "freeze": freeze,
                    "day_path": f"/programs/{enrollment.program.slug}/day/{number}"}
    if last_day:
        return {"kind": "last_day", "last_day": True, "freeze": freeze}
    kata = await pick_daily_kata(db, user, today)
    if kata is not None:
        return {"kind": "technique", "title": kata.title_en if lang == "en" else kata.title_tr,
                "kata_path": f"/kata/{kata.slug}", "last_day": False, "freeze": False}
    return {"kind": "generic", "last_day": False, "freeze": False}


def _last_day_key(sel: dict) -> str:
    return "lastday_freeze" if sel["freeze"] else "lastday"


async def build_reminder(db: AsyncSession, user: User, today: date, info: dict) -> dict:
    """E-posta: kind, subject, html (alt bilgi dahil)."""
    t = get_strings(user.lang or "tr")
    base = settings.base_url
    footer = t["mail_unsub_footer"].format(unsub=unsubscribe_url(user))
    sel = await select_reminder(db, user, today, info)
    key = _last_day_key(sel)
    if sel["kind"] == "program":
        html = t["mail_reminder_program_body"].format(
            n=sel["n"], focus=_html.escape(sel["focus"]), day_link=base + sel["day_path"]
        )
        if sel["last_day"]:
            html += t[f"mail_reminder_{key}_line"]
        subject = t["mail_reminder_program_subject"].format(n=sel["n"])
    elif sel["kind"] == "last_day":
        subject = t[f"mail_reminder_{key}_subject"]
        html = t[f"mail_reminder_{key}_body"].format(streak=info["streak"], link=f"{base}/app")
    elif sel["kind"] == "technique":
        subject = t["mail_reminder_tech_subject"].format(title=sel["title"])  # konu düz metin
        html = t["mail_reminder_tech_body"].format(title=_html.escape(sel["title"]), kata_link=base + sel["kata_path"])
    else:
        subject = t["mail_reminder_subject"]
        html = t["mail_reminder_body"].format(link=f"{base}/app")
    return {"kind": sel["kind"], "subject": subject, "html": html + footer}


async def build_push(db: AsyncSession, user: User, today: date, info: dict) -> dict:
    """Push: aynı seçim, kısa metin; seri sayısı geçmez (seri 0 iken anlamsız)."""
    t = get_strings(user.lang or "tr")
    sel = await select_reminder(db, user, today, info)
    key = _last_day_key(sel)
    url = "/app"
    if sel["kind"] == "program":
        body = t["push_reminder_program_body"].format(n=sel["n"], focus=sel["focus"])
        if sel["last_day"]:
            body += " " + t[f"push_reminder_{key}_body"]
        url = sel["day_path"]
    elif sel["kind"] == "last_day":
        body = t[f"push_reminder_{key}_body"]
    elif sel["kind"] == "technique":
        body = t["push_reminder_tech_body"].format(title=sel["title"])
        url = sel["kata_path"]
    else:
        body = t["push_reminder_body"]
    return {"kind": sel["kind"], "title": t["push_reminder_title"], "body": body, "url": url}
