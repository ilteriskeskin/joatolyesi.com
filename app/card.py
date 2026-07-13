"""Paylaşılabilir profil kartı (OG görseli): 1200x630 PNG.

Pillow ile sunucuda çizilir; harici servis yok. Instagram bio/story ve
link önizlemelerinde (WhatsApp, Twitter, Slack...) profil kartı olarak
görünür — "dövüş sanatçısının GitHub profili" vitrini.
"""

import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 12, 13)
RAISED = (20, 21, 23)
INK = (232, 228, 220)
DIM = (166, 161, 154)
ACCENT = (184, 146, 90)
BORDER = (38, 40, 43)

BELT_COLORS = {
    "white": (237, 233, 223),
    "yellow": (220, 182, 63),
    "orange": (205, 124, 54),
    "green": (92, 138, 85),
    "blue": (71, 103, 156),
    "brown": (111, 74, 42),
    "black": (25, 26, 28),
}

# Isı haritası kademeleri (build_heatmap ile aynı mantık)
LEVEL_ALPHA = {None: 0, 0: 26, 1: 70, 2: 120, 3: 180, 4: 255}

_FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVu{kind}.ttf",  # debian/slim (Dockerfile kurar)
    "/System/Library/Fonts/Supplemental/Arial{mac_kind}.ttf",  # macOS (lokal gelistirme)
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for tmpl in _FONT_CANDIDATES:
        path = tmpl.format(kind="Sans-Bold" if bold else "Sans", mac_kind=" Bold" if bold else "")
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _draw_belt(d: ImageDraw.ImageDraw, x: float, y: float, width: float, belt_rgb: tuple) -> None:
    """Gerçek bir kuşak çizer (bant + düğüm + sarkan uçlar) — sitedeki
    _belt_svg.html ile aynı 72x44 oranlarını kullanır, düz banttan
    çok daha tanınabilir."""
    scale = width / 72

    def rx(v: float) -> float:
        return x + v * scale

    def ry(v: float) -> float:
        return y + v * scale

    knot_rgb = tuple(max(0, int(c * 0.82)) for c in belt_rgb)

    d.rounded_rectangle([rx(2), ry(14), rx(70), ry(26)], radius=max(2, scale * 2), fill=belt_rgb, outline=BORDER, width=1)
    d.polygon([(rx(31), ry(25)), (rx(25), ry(41)), (rx(31), ry(41)), (rx(35), ry(27))], fill=belt_rgb)
    d.polygon([(rx(41), ry(25)), (rx(47), ry(41)), (rx(41), ry(41)), (rx(37), ry(27))], fill=belt_rgb)
    d.rounded_rectangle([rx(29), ry(11), rx(43), ry(29)], radius=max(2, scale * 3), fill=knot_rgb, outline=BORDER, width=1)


def render_profile_card(
    *,
    name: str,
    username: str,
    user_id: str,
    discipline_label: str,
    streak: int,
    streak_label: str,
    total_days: int,
    days_label: str,
    belt_id: str,
    belt_label: str,
    heatmap: list[list[dict]],
) -> bytes:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Çerçeve + marka
    d.rounded_rectangle([24, 24, W - 24, H - 24], radius=18, outline=BORDER, width=2)
    d.text((W - 60, 60), "joatolyesi.com", font=_font(26), fill=DIM, anchor="ra")

    # Avatar amblemi (enso + kuşak rengi + baş harf) isim solunda
    from app.avatar import render_avatar

    avatar_size = 140
    avatar_png = render_avatar(seed=user_id, initial=name, belt_id=belt_id, size=avatar_size)
    avatar_img = Image.open(io.BytesIO(avatar_png)).convert("RGB")
    img.paste(avatar_img, (60, 52))

    # İsim + kullanıcı adı + branş (avatarın sağında)
    text_x = 60 + avatar_size + 28
    d.text((text_x, 60), name[:24], font=_font(52, bold=True), fill=INK)
    d.text((text_x, 128), f"@{username}", font=_font(26), fill=DIM)
    d.text((text_x, 168), discipline_label, font=_font(26), fill=ACCENT)

    # Seri ve toplam gün blokları
    d.text((60, 350), str(streak), font=_font(110, bold=True), fill=ACCENT)
    streak_w = d.textlength(str(streak), font=_font(110, bold=True))
    d.text((60 + streak_w + 20, 420), streak_label, font=_font(28), fill=DIM)
    d.text((60 + streak_w + 20, 456), f"{total_days} {days_label}", font=_font(28), fill=DIM)

    # Kuşak — gerçek kuşak şekli (bant + düğüm + sarkan uçlar)
    belt_rgb = BELT_COLORS.get(belt_id, BELT_COLORS["white"])
    belt_width = 130
    belt_x, belt_y = 60, 526
    _draw_belt(d, belt_x, belt_y, belt_width, belt_rgb)
    belt_h = belt_width * 44 / 72
    d.text((belt_x + belt_width + 26, belt_y + belt_h / 2 - 16), belt_label, font=_font(30, bold=True), fill=INK)

    # Isı haritası (sağ blok): sütun=hafta, satır=gün
    cell, gap = 26, 6
    grid_x = W - 60 - len(heatmap) * (cell + gap)
    grid_y = 200
    for wi, week in enumerate(heatmap):
        for di, day in enumerate(week):
            alpha = LEVEL_ALPHA.get(day["level"], 0)
            if alpha == 0:
                continue
            color = tuple(int(BG[i] + (ACCENT[i] - BG[i]) * alpha / 255) for i in range(3))
            x = grid_x + wi * (cell + gap)
            y = grid_y + di * (cell + gap)
            d.rounded_rectangle([x, y, x + cell, y + cell], radius=5, fill=color)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
