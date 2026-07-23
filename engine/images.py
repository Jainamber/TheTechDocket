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

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

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
    "docket":     ((17, 18, 34), (39, 42, 96), (129, 140, 248)),
}
DEFAULT_PALETTE = ((15, 23, 42), (51, 65, 85), (148, 163, 184))


def _font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_DIRS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _dark(c, f):
    return tuple(max(0, min(255, int(x * f))) for x in c)


def _blob(size, center, radius, color):
    """A soft radial glow of `color` on black — screen-composite for light."""
    w, h = size
    lay = Image.new("RGB", (w, h), (0, 0, 0))
    ImageDraw.Draw(lay).ellipse(
        [center[0] - radius, center[1] - radius,
         center[0] + radius, center[1] + radius], fill=color)
    return lay.filter(ImageFilter.GaussianBlur(int(radius * 0.7)))


def _vignette(size):
    w, h = size
    v = Image.new("L", (w, h), 0)
    m = int(min(w, h) * 0.05)
    ImageDraw.Draw(v).rectangle([m, m, w - m, h - m], fill=255)
    return v.filter(ImageFilter.GaussianBlur(int(min(w, h) * 0.16)))


def _cover(w: int, h: int, hub: str, key: str) -> Image.Image:
    """A premium, TEXTLESS per-hub cover: deep gradient + one controlled
    corner glow + fine concentric 'signal' arcs + grain + a small wordmark.
    Deterministic per (hub, key). No headline text — the page already has it,
    so a text-baked card just read as a cheap auto-OG placeholder.
    """
    ss = 2
    W, H = w * ss, h * ss
    top, bottom, accent = PALETTES.get(hub, DEFAULT_PALETTE)
    seed = int(hashlib.md5((hub + "|" + key).encode()).hexdigest()[:8], 16)
    r = [((seed >> (i * 3)) & 1023) / 1023 for i in range(12)]
    right = r[7] > 0.5

    # deep base gradient — stays dark; the glow supplies the light
    base_a = _dark(top, 0.62)
    base_b = _dark(_mix(top, bottom, 0.55), 0.82)
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        d.line([(0, y), (W, y)], fill=_mix(base_a, base_b, y / H))

    # one controlled corner glow + a very dim counter-glow
    gx, gy = W * (0.82 if right else 0.18), H * 0.92
    img = ImageChops.screen(img, _blob(
        (W, H), (int(gx), int(gy)), int(W * 0.34),
        _dark(_mix(accent, top, 0.15), 0.62)))
    img = ImageChops.screen(img, _blob(
        (W, H), (int(W * (0.2 if right else 0.8)), int(H * 0.12)),
        int(W * 0.26), _dark(_mix(accent, (255, 255, 255), 0.3), 0.30)))

    # concentric 'signal' arcs from the glow corner — crisp, thin, fading out
    arc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arc)
    line_col = _mix(accent, (255, 255, 255), 0.25)
    for i in range(8):
        rad = int(W * (0.14 + 0.108 * i))
        ad.ellipse([gx - rad, gy - rad, gx + rad, gy + rad],
                   outline=(*line_col, max(12, 70 - i * 6)),
                   width=max(2, int(ss * 1.2)))
    arc = arc.filter(ImageFilter.GaussianBlur(int(ss * 0.6)))
    img = Image.alpha_composite(img.convert("RGBA"), arc).convert("RGB")

    # framed vignette falloff
    vmask = _vignette((W, H))
    img = Image.composite(img, Image.blend(img, Image.new("RGB", (W, H), (0, 0, 0)), 0.55), vmask)

    # fine grain — kills gradient banding, adds a printed texture
    grain = Image.effect_noise((W, H), 16).convert("RGB")
    img = Image.blend(img, ImageChops.overlay(img, grain), 0.045)

    img = img.resize((w, h), Image.LANCZOS)

    # small, letter-spaced wordmark, bottom-left (share branding only)
    d2 = ImageDraw.Draw(img)
    f = _font(max(10, int(h * 0.030)))
    x, yb = int(w * 0.055), h - int(h * 0.095)
    for ch in "THE TECH DOCKET":
        d2.text((x, yb), ch, font=f, fill=(214, 220, 234))
        x += f.getlength(ch) + max(2, int(h * 0.006))
    return img


def generate_hero(title: str, slug: str, hub: str, site_name: str,
                  outdir: Path) -> list[dict]:
    outdir.mkdir(parents=True, exist_ok=True)
    outputs = []
    for w, h, label in [(1200, 675, "16x9"), (1200, 900, "4x3"), (1200, 1200, "1x1")]:
        img = _cover(w, h, hub, slug)
        base = outdir / f"{slug}-{label}"
        img.save(f"{base}.jpg", quality=88, optimize=True, progressive=True)
        img.save(f"{base}.webp", quality=84, method=6)
        outputs.append({"label": label, "w": w, "h": h,
                        "jpg": f"{base.name}.jpg", "webp": f"{base.name}.webp"})
    return outputs


def generate_docket_card(date_str: str, date_human: str, site_name: str,
                         outdir: Path) -> dict:
    """OG card for a Today's Docket page (1200x675 + webp), textless cover."""
    outdir.mkdir(parents=True, exist_ok=True)
    img = _cover(1200, 675, "docket", date_str)
    base = outdir / f"docket-{date_str}-16x9"
    img.save(f"{base}.jpg", quality=88, optimize=True, progressive=True)
    img.save(f"{base}.webp", quality=84, method=6)
    return {"jpg": f"{base.name}.jpg", "webp": f"{base.name}.webp"}


def _wrap_text(draw: ImageDraw.ImageDraw, text: str,
               font: ImageFont.FreeTypeFont, max_w: int) -> list[str]:
    lines, cur = [], ""
    for w in (text or "").split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def generate_carousel(date_str: str, date_human: str, entries: list[dict],
                      site_url: str, outdir: Path, slide_w: int = 1080,
                      slide_h: int = 1350, max_slides: int = 20) -> list[str]:
    """Instagram-ready 4:5 carousel from a day's docket (proposal
    2026-07-23 Phase B) — the text-baked sibling of the textless covers
    (the DESIGN-COVER-2026-07-21 optional follow-up, now with a job).

    Slide 1 = cover promise (the lead headline, RED-style specific promise),
    one slide per entry (headline + stat + why), last slide = CTA. Every
    slide carries the site host; house gradient art only — no generative
    imagery (gate D19 / proposal S07 contract). Output is data/social/
    (gitignored): deliverables for the owner to post manually, never
    auto-published anywhere.
    """
    outdir.mkdir(parents=True, exist_ok=True)
    host = site_url.replace("https://", "").replace("http://", "").strip("/")
    body = entries[: max(1, max_slides - 2)]
    total = len(body) + 2
    made: list[str] = []
    margin = int(slide_w * 0.074)
    text_w = slide_w - 2 * margin

    def _host_tag(d: ImageDraw.ImageDraw) -> None:
        f = _font(int(slide_h * 0.019))
        tw = d.textlength(host, font=f)
        d.text((slide_w - tw - margin, slide_h - int(slide_h * 0.052)),
               host, font=f, fill=(214, 220, 234))

    def _counter(d: ImageDraw.ImageDraw, n: int) -> None:
        f = _font(int(slide_h * 0.019))
        d.text((margin, slide_h - int(slide_h * 0.052)), f"{n} / {total}",
               font=f, fill=(150, 158, 180))

    def _save(img: Image.Image, n: int) -> None:
        p = outdir / f"slide-{n:02d}.jpg"
        img.save(p, quality=88, optimize=True, progressive=True)
        made.append(p.name)

    # slide 1 — cover promise: the lead headline IS the promise
    img = _cover(slide_w, slide_h, "docket", date_str + "-cover")
    d = ImageDraw.Draw(img)
    accent = PALETTES["docket"][2]
    fk = _font(int(slide_h * 0.023))
    d.text((margin, int(slide_h * 0.115)), "TODAY'S DOCKET", font=fk, fill=accent)
    d.text((margin, int(slide_h * 0.115) + int(slide_h * 0.034)),
           date_human.upper(), font=fk, fill=(190, 196, 214))
    lead = next((e for e in body if e.get("lead")), body[0] if body else None)
    y = int(slide_h * 0.29)
    if lead:
        fh = _font(int(slide_h * 0.05))
        for ln in _wrap_text(d, str(lead.get("headline") or ""), fh, text_w)[:6]:
            d.text((margin, y), ln, font=fh, fill=(238, 240, 248))
            y += int(slide_h * 0.06)
    fs = _font(int(slide_h * 0.024))
    d.text((margin, y + int(slide_h * 0.024)),
           f"+ {max(0, len(body) - 1)} more signals · a 60-second read",
           font=fs, fill=(170, 178, 200))
    d.text((margin, y + int(slide_h * 0.024) + int(slide_h * 0.036)),
           "swipe →", font=fs, fill=accent)
    _host_tag(d)
    _counter(d, 1)
    _save(img, 1)

    # entry slides — one claim + one number, why-it-matters, source
    for n, e in enumerate(body, start=2):
        hub = str(e.get("hub") or "docket")
        img = _cover(slide_w, slide_h, hub, f"{date_str}-{n}")
        d = ImageDraw.Draw(img)
        pal = PALETTES.get(hub, DEFAULT_PALETTE)
        acc = _mix(pal[2], (255, 255, 255), 0.25)
        fk = _font(int(slide_h * 0.021))
        d.text((margin, int(slide_h * 0.082)),
               str(e.get("hub_name") or hub).upper(), font=fk, fill=acc)
        y = int(slide_h * 0.13)
        fh = _font(int(slide_h * 0.042))
        for ln in _wrap_text(d, str(e.get("headline") or ""), fh, text_w)[:5]:
            d.text((margin, y), ln, font=fh, fill=(240, 242, 250))
            y += int(slide_h * 0.052)
        y += int(slide_h * 0.018)
        stat = str(e.get("stat_line") or "").strip()
        if stat:
            fstat = _font(int(slide_h * 0.056))
            for ln in _wrap_text(d, stat, fstat, text_w)[:2]:
                d.text((margin, y), ln, font=fstat, fill=pal[2])
                y += int(slide_h * 0.068)
            y += int(slide_h * 0.012)
        why = str(e.get("why") or "").strip()
        if why:
            flab = _font(int(slide_h * 0.018))
            d.text((margin, y), "WHY IT MATTERS", font=flab, fill=acc)
            y += int(slide_h * 0.032)
            fw = _font(int(slide_h * 0.027))
            for ln in _wrap_text(d, why, fw, text_w)[:5]:
                d.text((margin, y), ln, font=fw, fill=(210, 216, 232))
                y += int(slide_h * 0.038)
        src = str(e.get("source") or "").strip()
        if src:
            fsrc = _font(int(slide_h * 0.019))
            d.text((margin, min(y + int(slide_h * 0.022),
                                slide_h - int(slide_h * 0.11))),
                   f"Source: {src}", font=fsrc, fill=(150, 158, 180))
        _host_tag(d)
        _counter(d, n)
        _save(img, n)

    # CTA slide
    img = _cover(slide_w, slide_h, "docket", date_str + "-cta")
    d = ImageDraw.Draw(img)
    fh = _font(int(slide_h * 0.05))
    d.text((margin, int(slide_h * 0.34)), "That's today's docket.",
           font=fh, fill=(238, 240, 248))
    fs = _font(int(slide_h * 0.026))
    d.text((margin, int(slide_h * 0.425)),
           "One long read + the day's signals, every", font=fs,
           fill=(200, 206, 224))
    d.text((margin, int(slide_h * 0.425) + int(slide_h * 0.036)),
           "morning. Every claim linked to its source.", font=fs,
           fill=(200, 206, 224))
    fbig = _font(int(slide_h * 0.034))
    d.text((margin, int(slide_h * 0.55)), f"{host}/docket/",
           font=fbig, fill=PALETTES["docket"][2])
    _host_tag(d)
    _counter(d, total)
    _save(img, total)

    # caption.txt — hook, contents line, link line, hashtags
    lead_h = (str(lead.get("headline")) if lead
              else f"Today's Docket, {date_human}")
    others = [str(e.get("headline") or "") for e in body
              if not e.get("lead")][:4]
    cap = [lead_h, ""]
    if others:
        cap += ["Also today: " + " · ".join(o for o in others if o), ""]
    cap += [f"Full docket with every source linked → {host}/docket/", "",
            "#TechNews #AI #India #TheTechDocket #TechDaily"]
    (outdir / "caption.txt").write_text("\n".join(cap), encoding="utf-8")
    return made


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
