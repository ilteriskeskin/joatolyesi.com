"""Kullanıcı avatarı: yükleme gerektirmeyen, sunucuda üretilen mühür/enso
tarzı amblem. Kuşak rengi halka olarak, kullanıcı adının baş harfi
ortada, enso (kırık daire fırça darbesi) her kullanıcı için farklı
açıda döner (deterministik — profil fotoğrafı gibi kalıcı kimlik).

CJK karakter kullanılmaz: prod Docker imajında yalnız DejaVu (Latin)
fontu var, Uzak Doğu glifleri tofu kutucuğu olarak render olurdu.
"""

import hashlib
import io

from PIL import Image, ImageDraw

from app.card import BELT_COLORS, BG, BORDER, RAISED, ACCENT, _font


def render_avatar(*, seed: str, initial: str, belt_id: str, size: int = 256) -> bytes:
    img = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(img)
    cx = cy = size / 2

    # Kullanıcıya özel dönüş açısı — herkesin enso'su biraz farklı durur
    rotation = int(hashlib.sha256(seed.encode()).hexdigest(), 16) % 360

    ring_width = max(4, size // 20)
    belt_rgb = BELT_COLORS.get(belt_id, BELT_COLORS["white"])
    bbox_ring = [ring_width / 2, ring_width / 2, size - ring_width / 2, size - ring_width / 2]
    # Enso: tam kapanmayan fırça darbesi (~300° yay), her kullanıcıda farklı başlangıç açısı
    d.arc(bbox_ring, start=rotation, end=rotation + 300, fill=belt_rgb, width=ring_width)

    inset = ring_width + size * 0.05
    d.ellipse([inset, inset, size - inset, size - inset], fill=RAISED, outline=BORDER, width=max(1, size // 128))

    font = _font(int(size * 0.38), bold=True)
    letter = (initial or "?")[:1].upper()
    bbox = d.textbbox((0, 0), letter, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), letter, font=font, fill=ACCENT)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
