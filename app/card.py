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


def render_profile_card(
    *,
    name: str,
    username: str,
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
    d.text((60, 52), "joryu", font=_font(40, bold=True), fill=ACCENT)
    d.text((W - 60, 60), "joatolyesi.com", font=_font(26), fill=DIM, anchor="ra")

    # İsim + kullanıcı adı + branş
    d.text((60, 140), name[:28], font=_font(64, bold=True), fill=INK)
    d.text((60, 222), f"@{username}", font=_font(30), fill=DIM)
    d.text((60, 268), discipline_label, font=_font(30), fill=ACCENT)

    # Seri ve toplam gün blokları
    d.text((60, 360), str(streak), font=_font(120, bold=True), fill=ACCENT)
    streak_w = d.textlength(str(streak), font=_font(120, bold=True))
    d.text((60 + streak_w + 20, 440), streak_label, font=_font(30), fill=DIM)
    d.text((60, 508), f"{total_days} {days_label}", font=_font(30), fill=DIM)

    # Kuşak bandı (alt kenar)
    belt_rgb = BELT_COLORS.get(belt_id, BELT_COLORS["white"])
    d.rounded_rectangle([60, 556, 560, 580], radius=6, fill=belt_rgb, outline=BORDER, width=1)
    d.text((580, 556), belt_label, font=_font(26, bold=True), fill=INK)

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
