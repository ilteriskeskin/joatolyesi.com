DISCIPLINES = (
    "aikijo",
    "bokken",
    "aikido",
    "jodo",
    "kenjutsu",
    "kendo",
    "iaido",
    "karate",
    "taekwondo",
    "other",
)

# Ürün artık silahlı solo pratiğe odaklanıyor (karate/taekwondo kapsam dışı).
# Yeni seçim gerektiren her yerde (kayıt, profil, pratik kaydı, filtreler)
# bu liste kullanılır. Eski karate/taekwondo verisi (kullanıcı/seans/kata)
# DISCIPLINES üzerinden hâlâ okunabilir — silinmedi, sadece yeni seçimden
# çıkarıldı.
SELECTABLE_DISCIPLINES = tuple(d for d in DISCIPLINES if d not in ("karate", "taekwondo"))

# Sahibin gerçek hesabı: geçmişi scripts/backfill_practice.py ile doldurulduğu
# için scripts/weekly_metrics.py ana metriklerden hariç tutar. Tek kaynak burası.
OWNER_EMAIL = "aliilteriskeskin@gmail.com"

# seed_blog.py'nin oluşturduğu demo hesapların e-posta soneki. Repo genelinde
# tek tanım burası; demo hesaplar kamuya açık hiçbir yerde görünmez.
DEMO_EMAIL_SUFFIX = "@demo.joatolyesi.com"


def demo_user_clause():
    """SQL: kullanıcı demo hesap mı (e-posta sonekine göre)."""
    from sqlalchemy import func

    from app.models import User  # geç import: models -> constants döngüsünü önler

    return func.lower(User.email).like(f"%{DEMO_EMAIL_SUFFIX}")


def public_user_clause():
    """SQL: kamuya açık gösterilebilir kullanıcı (açık profil, kullanıcı adı var, demo değil)."""
    from sqlalchemy import and_

    from app.models import User

    return and_(User.is_public, User.username.is_not(None), ~demo_user_clause())


def is_demo_user(user) -> bool:
    """Python/Jinja tarafı: aynı kural, yüklenmiş kullanıcı nesnesi için."""
    email = getattr(user, "email", None) or ""
    return email.lower().endswith(DEMO_EMAIL_SUFFIX)
