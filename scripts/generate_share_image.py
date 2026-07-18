"""Paylaşım (sosyal medya) görseli üretir: 1200x630 PNG.

Uygulamanın kendi görsel diliyle (siyah zemin, enso, jo çizgisi, altın
vurgu) — Instagram/Twitter/LinkedIn'e atılacak tanıtım görseli. Profil
kartından (app/card.py) farklı olarak kişiye özel değil, ürünü tanıtan
genel bir görsel.

Çalıştırma:  python scripts/generate_share_image.py
Çıktı:       share_image.png (proje kökünde)
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 12, 13)
INK = (232, 228, 220)
DIM = (166, 161, 154)
ACCENT = (184, 146, 90)
RED = (178, 58, 46)
BORDER = (38, 40, 43)

_SERIF_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
]
_SERIF_REGULAR_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/System/Library/Fonts/Supplemental/Georgia.ttf",
]
_SANS_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]
_SANS_BOLD_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
]


def _load(candidates: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def _draw_enso(d: ImageDraw.ImageDraw, cx: float, cy: float, r: float, width: int) -> None:
    """Kırık daire (enso) — landing hero / ikon ile aynı motif."""
    start, end = -60 + 20, -60 + 340  # ~340 derecelik ark, brush-stroke hissi
    d.arc([cx - r, cy - r, cx + r, cy + r], start=start, end=end, fill=ACCENT, width=width)
    # Uçları yuvarlatmak için küçük daireler (round cap simülasyonu)
    for angle in (start, end):
        rad = math.radians(angle)
        x, y = cx + r * math.cos(rad), cy + r * math.sin(rad)
        d.ellipse([x - width / 2, y - width / 2, x + width / 2, y + width / 2], fill=ACCENT)
    # Jo çizgisi: enso'nun içinden geçen çapraz çizgi
    lw = width - 6
    x1, y1 = cx - r * 0.62, cy + r * 0.72
    x2, y2 = cx + r * 0.68, cy - r * 0.62
    d.line([x1, y1, x2, y2], fill=INK, width=lw)
    for x, y in ((x1, y1), (x2, y2)):
        d.ellipse([x - lw / 2, y - lw / 2, x + lw / 2, y + lw / 2], fill=INK)


def _wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int, draw: ImageDraw.ImageDraw) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def render() -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Hafif dokulu köşe vinyeti (üst-sol koyu, alt-sağ enso'nun etrafı biraz aydınlık)
    d.rectangle([0, 0, W, H], fill=BG)

    headline_font = _load(_SERIF_CANDIDATES, 54)
    sub_font = _load(_SANS_CANDIDATES, 25)
    bullet_font = _load(_SANS_CANDIDATES, 23)
    bullet_bold_font = _load(_SANS_BOLD_CANDIDATES, 25)
    brand_font = _load(_SERIF_CANDIDATES, 32)
    brand_sub_font = _load(_SANS_CANDIDATES, 19)

    left_margin = 70
    content_width = 620

    # Başlık
    headline = "Dojo kapalıyken de çalış."
    lines = _wrap(headline, headline_font, content_width, d)
    y = 56
    for line in lines:
        d.text((left_margin, y), line, font=headline_font, fill=INK)
        y += 62

    # Alt başlık
    sub = "Aikido, iaido, jodo, kenjutsu, kendo, karate ve taekwondo için\nsolo pratik takip uygulaması."
    y += 10
    for line in sub.split("\n"):
        d.text((left_margin, y), line, font=sub_font, fill=DIM)
        y += 32

    # Madde noktaları
    bullets = [
        ("Seri ve kuşak sistemi", "Her gün kaydet, 365 günde siyah kuşak ol."),
        ("Kata & teknik kütüphanesi", "Branşına özel, videolu ve yazılı referans."),
        ("Herkese açık profil", "Isı haritası, seri, paylaşılabilir kart."),
    ]
    y += 22
    for title, desc in bullets:
        d.ellipse([left_margin, y + 7, left_margin + 10, y + 17], fill=RED)
        d.text((left_margin + 26, y), title, font=bullet_bold_font, fill=INK)
        d.text((left_margin + 26, y + 30), desc, font=bullet_font, fill=DIM)
        y += 66

    # Marka
    brand_y = H - 66
    d.text((left_margin, brand_y), "joryu", font=brand_font, fill=ACCENT)
    brand_w = d.textlength("joryu", font=brand_font)
    d.text((left_margin + brand_w + 14, brand_y + 7), "Jo Atölyesi · joatolyesi.com",
           font=brand_sub_font, fill=DIM)

    # Sağ taraf: dev enso + jo çizgisi
    cx, cy, r = 930, 320, 210
    _draw_enso(d, cx, cy, r, width=15)

    # İnce çerçeve
    d.rectangle([0, 0, W - 1, H - 1], outline=BORDER, width=2)

    return img


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "share_image.png"
    render().save(out)
    print(f"kaydedildi: {out}")
