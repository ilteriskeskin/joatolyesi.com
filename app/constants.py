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
