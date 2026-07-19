"""Hero / OG image generation (no external APIs).

Generates branded, deterministic gradient cards with the headline text:
  - 1200x675 (16:9)  -> og:image, Discover, twitter:image, schema image[0]
  - 1200x900 (4:3)   -> schema image[1]
  - 1200x1200 (1:1)  -> schema image[2]
Each written as .jpg (quality 88) and .webp alongside.
Also generates the site logo / favicon PNGs once.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]

# hub -> (top colour, bottom colour, accent)
PALETTES = {
    "ai-models":  ((16, 24, 64), (88, 28, 135), (129, 140, 248)),
    "ai-tools":   ((6, 40, 61), (13, 94, 130), (94, 234, 212)),
    "big-tech":   ((30, 27, 75), (67, 20, 100), (196, 181, 253)),
    "hardware":   ((37, 17, 12), (120, 53, 15), (251, 191, 36)),
    "policy":     ((28, 25, 23), (68, 64, 60), (168, 162, 158)),
    "explainers": ((5, 46, 22), (21, 94, 60), (110, 231, 183)),
}
DEFAULT_PALETTE = ((15, 23, 42), (51, 65, 85), (148, 163, 184))


def _font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_DIRS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _card(w: int, h: int, title: str, site: str, hub: str, kicker: str) -> Image.Image:
    top, bottom, accent = PALETTES.get(hub, DEFAULT_PALETTE)
    seed = int(hashlib.md5(title.encode()).hexdigest()[:6], 16)
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=_lerp(top, bottom, y / h))
    # deterministic decorative circles
    for i in range(3):
        r = 120 + (seed >> (i * 4)) % 220
        cx = (seed >> (i * 5)) % w
        cy = (seed >> (i * 3)) % h
        ring = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            outline=(*accent, 46), width=10)
        img = Image.alpha_composite(img.convert("RGBA"), ring).convert("RGB")
    d = ImageDraw.Draw(img)
    # accent bar + kicker
    margin = int(w * 0.06)
    d.rectangle([margin, margin, margin + int(w * 0.09), margin + 12], fill=accent)
    d.text((margin, margin + 30), kicker.upper(), font=_font(int(h * 0.045)),
           fill=(*accent,))
    # headline
    title_font = _font(int(h * 0.105))
    lines = _wrap(d, title, title_font, w - 2 * margin)
    while len(lines) > 4:
        title_font = _font(int(title_font.size * 0.88))
        lines = _wrap(d, title, title_font, w - 2 * margin)
    line_h = int(title_font.size * 1.22)
    total = len(lines) * line_h
    y0 = max(int(h * 0.30), (h - total) // 2)
    for i, line in enumerate(lines):
        d.text((margin, y0 + i * line_h), line, font=title_font, fill=(255, 255, 255))
    # site badge bottom
    badge_font = _font(int(h * 0.05))
    d.text((margin, h - margin - badge_font.size), site, font=badge_font,
           fill=(255, 255, 255))
    tw = d.textlength(site, font=badge_font)
    d.rectangle([margin, h - margin + 6, margin + tw, h - margin + 10], fill=accent)
    return img


def generate_hero(title: str, slug: str, hub: str, site_name: str,
                  outdir: Path) -> list[dict]:
    outdir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for w, h, label in [(1200, 675, "16x9"), (1200, 900, "4x3"), (1200, 1200, "1x1")]:
        img = _card(w, h, title, site_name, hub, kicker=hub.replace("-", " "))
        base = outdir / f"{slug}-{label}"
        img.save(f"{base}.jpg", quality=88, optimize=True, progressive=True)
        img.save(f"{base}.webp", quality=84, method=6)
        outputs.append({"label": label, "w": w, "h": h,
                        "jpg": f"{base.name}.jpg", "webp": f"{base.name}.webp"})
    return outputs


def generate_site_assets(site_name: str, assets_dir: Path) -> None:
    assets_dir.mkdir(parents=True, exist_ok=True)
    accent = (129, 140, 248)
    for size, name in [(112, "logo-112x112.png"), (512, "logo-512.png"),
                       (180, "apple-touch-icon.png"), (48, "favicon-48.png")]:
        img = Image.new("RGB", (size, size), (16, 24, 64))
        d = ImageDraw.Draw(img)
        f = _font(int(size * 0.62))
        letter = site_name[0].upper()
        bb = d.textbbox((0, 0), letter, font=f)
        d.rectangle([0, size - int(size * 0.14), size, size], fill=accent)
        d.text(((size - (bb[2] - bb[0])) / 2 - bb[0],
                (size - (bb[3] - bb[1])) / 2 - bb[1] - size * 0.06),
               letter, font=f, fill=(255, 255, 255))
        img.save(assets_dir / name)
    # simple SVG favicon (crisp at any size)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
           f'<rect width="100" height="100" rx="18" fill="#101840"/>'
           f'<rect y="86" width="100" height="14" fill="#818CF8"/>'
           f'<text x="50" y="66" font-family="DejaVu Sans, Arial, sans-serif" '
           f'font-size="58" font-weight="bold" fill="#fff" '
           f'text-anchor="middle">{site_name[0].upper()}</text></svg>')
    (assets_dir.parent / "favicon.svg").write_text(svg, encoding="utf-8")
