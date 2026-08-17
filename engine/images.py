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
import math
import re
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


# ---------------- topic motifs (cover art v3, 2026-08-01) ----------------
# Owner feedback: the textless gradients read as BLANK at thumbnail size.
# v3 keeps the house rules (deterministic, no external APIs, no stock, no
# generative imagery, no headline text) but adds a drawn, topic-related
# focal MOTIF picked from the title/tags. Boundary-aware matching reuses
# the suggest_tag discipline (docket.py _term_hit rationale).

MOTIF_KEYWORDS = [
    ("waveform", "voice,clone,scam,call,audio,speech,deepfake call,helpline"),
    ("shield",   "privacy,dpdp,data protection,security,breach,secure,gdpr,consent"),
    ("scales",   "law,court,act,ruling,regulation,policy,antitrust,lawsuit,legal,judge,eu ai act,copyright"),
    ("chip",     "chip,chips,gpu,gpus,nvidia,snapdragon,semiconductor,silicon,hardware,mi450,tpu,npu,exynos"),
    ("phone",    "phone,smartphone,mobile,on-device,android,iphone,pixel,galaxy"),
    ("pages",    "context,token,tokens,window,document,memory,prompt,rag"),
    ("cloud",    "cloud,server,data center,datacenter,compute,hosted"),
    ("price",    "price,pricing,cost,cheap,rates,cut,hike,subscription,fee,rupee,billion,funding,deal,stake"),
    ("magnify",  "spot,detect,how to,guide,explained,check,verify,identify,tips"),
    ("chat",     "chatbot,chat,assistant,copilot,tier,free,tiers"),
    ("neural",   "model,models,llm,gpt,gemini,claude,llama,qwen,kimi,training,benchmark,agent,ai model"),
    ("globe",    "google,apple,microsoft,meta,openai,big tech,amazon,global"),
]


def pick_motif(text: str, hub: str) -> str:
    """First motif whose keywords hit `text` (boundary-aware), else the
    hub's default. Deterministic; order in MOTIF_KEYWORDS = priority."""
    t = (text or "").lower()

    def hit(term: str) -> bool:
        for m in re.finditer(re.escape(term), t):
            s, e = m.start(), m.end()
            if (s == 0 or not t[s - 1].isalnum()) and \
               (e == len(t) or not term[-1].isalnum() or not t[e].isalnum()):
                return True
        return False

    for motif, terms in MOTIF_KEYWORDS:
        if any(hit(x.strip()) for x in terms.split(",") if x.strip()):
            return motif
    return {"ai-models": "neural", "ai-tools": "chat", "big-tech": "globe",
            "hardware": "chip", "policy": "scales", "explainers": "magnify",
            "docket": "ticker"}.get(hub, "neural")


def _draw_motif(img: Image.Image, motif: str, hub: str, seed: int,
                ss: int) -> Image.Image:
    """Draw one editorial line-art motif on a transparent layer and
    composite. Flat poster style: 2-3 stroke weights, accent + white
    tints, one filled focal element. All geometry scales with height."""
    W, H = img.size
    top, bottom, accent = PALETTES.get(hub, DEFAULT_PALETTE)
    lite = _mix(accent, (255, 255, 255), 0.55)
    soft = _mix(accent, (255, 255, 255), 0.25)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    u = H / 100.0                          # 1 unit = 1% of height
    thin = max(2, int(ss * 1.4))
    mid = max(3, int(ss * 2.4))
    fat = max(4, int(ss * 3.6))
    r = [((seed >> (i * 2)) & 255) / 255 for i in range(16)]
    cx, cy = W * (0.66 + 0.06 * r[0]), H * (0.46 + 0.06 * r[1])

    def ell(x, y, rad, **kw):
        d.ellipse([x - rad, y - rad, x + rad, y + rad], **kw)

    if motif == "chip":
        s = 26 * u
        d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s],
                            radius=int(4 * u), outline=(*lite, 235), width=fat)
        d.rounded_rectangle([cx - s * .45, cy - s * .45, cx + s * .45, cy + s * .45],
                            radius=int(2 * u), fill=(*accent, 90),
                            outline=(*soft, 200), width=mid)
        for i in range(4):
            off = -s * .72 + i * (s * .48)
            for a, b in ((cx + off, cy - s), (cx + off, cy + s)):
                d.line([a, b, a, b + (-9 * u if b < cy else 9 * u)],
                       fill=(*lite, 210), width=mid)
            for a in (cx - s, cx + s):
                d.line([a, cy + off, a + (-9 * u if a < cx else 9 * u), cy + off],
                       fill=(*lite, 210), width=mid)
        d.line([cx - s * 2.2, cy + s * 1.55, cx - s * .45, cy + s * 1.55,
                cx - s * .45, cy + s * .45], fill=(*soft, 150), width=thin)
    elif motif == "neural":
        pts = []
        for i in range(7):
            a = r[i] * 6.28318
            rad = (16 + 18 * r[i + 4]) * u
            pts.append((cx + rad * math.cos(a),
                        cy + rad * math.sin(a) * 0.8))
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                if (i + j) % 2:
                    d.line([pts[i], pts[j]], fill=(*soft, 90), width=thin)
        for i, p in enumerate(pts):
            ell(p[0], p[1], (2.2 + 1.6 * r[i + 6]) * u, fill=(*lite, 235))
        ell(cx, cy, 4.5 * u, fill=(*accent, 255))
        ell(cx, cy, 8 * u, outline=(*lite, 160), width=thin)
    elif motif == "chat":
        bw, bh = 40 * u, 24 * u
        d.rounded_rectangle([cx - bw, cy - bh - 6 * u, cx + bw * .15, cy - 6 * u + bh * .1],
                            radius=int(7 * u), outline=(*lite, 235), width=fat)
        d.polygon([(cx - bw * .55, cy - 6 * u + bh * .08),
                   (cx - bw * .35, cy - 6 * u + bh * .08),
                   (cx - bw * .55, cy + bh * .38)], fill=(*lite, 235))
        d.rounded_rectangle([cx - bw * .05, cy + 2 * u, cx + bw, cy + 2 * u + bh],
                            radius=int(7 * u), fill=(*accent, 80),
                            outline=(*soft, 210), width=mid)
        for i in range(3):
            ell(cx - bw * .55 + i * 9 * u, cy - 6 * u - bh * .42, 1.8 * u,
                fill=(*lite, 230))
    elif motif == "scales":
        d.line([cx, cy - 26 * u, cx, cy + 22 * u], fill=(*lite, 235), width=fat)
        d.line([cx - 26 * u, cy - 18 * u, cx + 26 * u, cy - 18 * u],
               fill=(*lite, 235), width=fat)
        ell(cx, cy - 26 * u, 3 * u, fill=(*accent, 255))
        for sx in (-26 * u, 26 * u):
            d.line([cx + sx, cy - 18 * u, cx + sx - 8 * u, cy + 1 * u],
                   fill=(*soft, 200), width=thin)
            d.line([cx + sx, cy - 18 * u, cx + sx + 8 * u, cy + 1 * u],
                   fill=(*soft, 200), width=thin)
            d.arc([cx + sx - 10 * u, cy - 6 * u, cx + sx + 10 * u, cy + 10 * u],
                  20, 160, fill=(*lite, 235), width=mid)
        d.line([cx - 14 * u, cy + 22 * u, cx + 14 * u, cy + 22 * u],
               fill=(*lite, 235), width=fat)
    elif motif == "shield":
        p = [(cx, cy - 26 * u), (cx + 20 * u, cy - 18 * u),
             (cx + 20 * u, cy + 2 * u), (cx, cy + 26 * u),
             (cx - 20 * u, cy + 2 * u), (cx - 20 * u, cy - 18 * u)]
        d.polygon(p, outline=(*lite, 240), width=fat)
        d.polygon([(x * .999, y) for x, y in p], fill=(*accent, 55))
        ell(cx, cy - 4 * u, 5 * u, outline=(*lite, 235), width=mid)
        d.line([cx, cy + 1 * u, cx, cy + 9 * u], fill=(*lite, 235), width=mid)
    elif motif == "waveform":
        n = 15
        for i in range(n):
            x = cx - 34 * u + i * (68 * u / (n - 1))
            amp = (4 + 20 * abs(math.sin(i * 1.7 + seed % 7))) * u
            col = (*accent, 255) if 5 <= i <= 9 else (*lite, 200)
            d.line([x, cy - amp, x, cy + amp], fill=col, width=fat)
        d.rounded_rectangle([cx - 46 * u, cy - 30 * u, cx - 38 * u, cy + 30 * u],
                            radius=int(3.5 * u), outline=(*soft, 180), width=mid)
    elif motif == "price":
        pts = [(cx - 34 * u, cy - 20 * u), (cx - 16 * u, cy - 4 * u),
               (cx - 4 * u, cy - 14 * u), (cx + 22 * u, cy + 14 * u)]
        d.line(pts, fill=(*lite, 240), width=fat, joint="curve")
        # solid triangular arrowhead at the tip (barbs swept BACK from the
        # travel direction — the open-fork look was a v3.0 draw bug)
        tip = pts[-1]
        ang = math.atan2(tip[1] - pts[-2][1], tip[0] - pts[-2][0])
        ah = 8 * u
        barbs = [(tip[0] - ah * math.cos(ang - 0.42),
                  tip[1] - ah * math.sin(ang - 0.42)),
                 (tip[0] - ah * math.cos(ang + 0.42),
                  tip[1] - ah * math.sin(ang + 0.42))]
        d.polygon([tip, barbs[0], barbs[1]], fill=(*lite, 240))
        for i, p in enumerate(pts[:-1]):
            ell(p[0], p[1], 2.6 * u, fill=(*accent, 255))
        ell(cx - 30 * u, cy + 18 * u, 8 * u, outline=(*soft, 190), width=mid)
        ell(cx - 18 * u, cy + 22 * u, 6 * u, outline=(*soft, 140), width=thin)
    elif motif == "phone":
        d.rounded_rectangle([cx - 15 * u, cy - 27 * u, cx + 15 * u, cy + 27 * u],
                            radius=int(5 * u), outline=(*lite, 240), width=fat)
        d.line([cx - 5 * u, cy - 22 * u, cx + 5 * u, cy - 22 * u],
               fill=(*lite, 200), width=mid)
        s = 8 * u
        d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], radius=int(2 * u),
                            fill=(*accent, 90), outline=(*soft, 220), width=mid)
        for off in (-s * .5, 0, s * .5):
            d.line([cx + off, cy + s, cx + off, cy + s + 4 * u],
                   fill=(*soft, 200), width=thin)
    elif motif == "cloud":
        for dx, dy, rad in ((-12, 2, 12), (0, -6, 15), (13, 2, 11)):
            ell(cx + dx * u, cy - 8 * u + dy * u, rad * u,
                outline=(*lite, 230), width=fat)
        d.line([cx - 24 * u, cy + 6 * u, cx + 24 * u, cy + 6 * u],
               fill=(*lite, 230), width=fat)
        for i, dx in enumerate((-14, 0, 14)):
            y0, y1 = cy + 12 * u, cy + 24 * u
            d.line([cx + dx * u, y0, cx + dx * u, y1],
                   fill=(*accent, 235) if i == 1 else (*soft, 180), width=mid)
            for da in (-1, 1):
                d.line([cx + dx * u, y1, cx + dx * u + da * 3.5 * u, y1 - 4 * u],
                       fill=(*accent, 235) if i == 1 else (*soft, 180), width=mid)
    elif motif == "pages":
        for i, (dx, dy) in enumerate(((9, -8), (4.5, -4), (0, 0))):
            box = [cx - 20 * u + dx * u, cy - 24 * u + dy * u,
                   cx + 14 * u + dx * u, cy + 24 * u + dy * u]
            d.rounded_rectangle(box, radius=int(2.5 * u),
                                fill=(int(top[0] * .7), int(top[1] * .7),
                                      int(top[2] * .7), 235) if i == 2 else None,
                                outline=(*lite, 235 if i == 2 else 120),
                                width=mid if i == 2 else thin)
        for j in range(5):
            wl = (24 - (6 if j == 4 else 0)) * u
            d.line([cx - 15 * u, cy - 15 * u + j * 8 * u,
                    cx - 15 * u + wl, cy - 15 * u + j * 8 * u],
                   fill=(*soft, 210) if j else (*accent, 255),
                   width=fat if not j else mid)
        d.line([cx + 20 * u, cy - 10 * u, cx + 27 * u, cy - 10 * u,
                cx + 27 * u, cy + 10 * u, cx + 20 * u, cy + 10 * u],
               fill=(*accent, 235), width=mid)
    elif motif == "magnify":
        ell(cx - 4 * u, cy - 6 * u, 17 * u, outline=(*lite, 240), width=fat)
        d.line([cx + 8 * u, cy + 6 * u, cx + 22 * u, cy + 20 * u],
               fill=(*lite, 240), width=fat + 2)
        for i in range(3):
            ell(cx - 10 * u + i * 6 * u, cy - 8 * u + (i % 2) * 5 * u, 1.7 * u,
                fill=(*accent, 255))
        d.arc([cx - 15 * u, cy - 17 * u, cx + 7 * u, cy + 5 * u], 200, 300,
              fill=(*soft, 200), width=thin)
    elif motif == "globe":
        R = 24 * u
        ell(cx, cy, R, outline=(*lite, 240), width=fat)
        d.ellipse([cx - R * .45, cy - R, cx + R * .45, cy + R],
                  outline=(*soft, 190), width=thin)
        d.line([cx - R, cy, cx + R, cy], fill=(*soft, 190), width=thin)
        for k in (-.5, .5):
            d.arc([cx - R, cy - R + k * R * (1 if k > 0 else -1) * 0,
                   cx + R, cy + R], 200 if k < 0 else 20,
                  340 if k < 0 else 160, fill=(*soft, 150), width=thin)
        ell(cx + R * .5, cy - R * .4, 3 * u, fill=(*accent, 255))
        ell(cx - R * .55, cy + R * .3, 2.2 * u, fill=(*lite, 235))
    else:  # "ticker" — docket default: reading-order signal blocks
        for i in range(5):
            bw = (10 + 9 * r[i + 3]) * u
            x0 = cx - 36 * u + i * 16 * u
            d.rounded_rectangle([x0, cy - 4 * u - bw / 2, x0 + 11 * u,
                                 cy - 4 * u + bw / 2], radius=int(1.8 * u),
                                fill=(*accent, 235) if i == 0 else None,
                                outline=(*lite, 220), width=mid)
        d.line([cx - 38 * u, cy + 20 * u, cx + 40 * u, cy + 20 * u],
               fill=(*soft, 170), width=thin)

    return Image.alpha_composite(img.convert("RGBA"), lay).convert("RGB")


def _cover(w: int, h: int, hub: str, key: str,
           motif: str | None = None) -> Image.Image:
    """A premium per-hub cover: deep gradient + one controlled corner glow
    + a drawn, topic-related MOTIF (cover art v3) + faint 'signal' arcs +
    grain + a small wordmark. Deterministic per (hub, key). Still no
    headline text — the motif carries the meaning, the page carries the
    words.
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

    # faint 'signal' arcs from the glow corner — background texture only in
    # v3 (the motif is the focal element now, arcs must not compete)
    arc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arc)
    line_col = _mix(accent, (255, 255, 255), 0.25)
    for i in range(5):
        rad = int(W * (0.16 + 0.13 * i))
        ad.ellipse([gx - rad, gy - rad, gx + rad, gy + rad],
                   outline=(*line_col, max(8, 34 - i * 6)),
                   width=max(2, int(ss * 1.2)))
    arc = arc.filter(ImageFilter.GaussianBlur(int(ss * 0.6)))
    img = Image.alpha_composite(img.convert("RGBA"), arc).convert("RGB")

    # topic motif (v3) — drawn before vignette/grain so it sits in the light
    img = _draw_motif(img, motif or pick_motif(key, hub), hub, seed, ss)

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
    motif = pick_motif(f"{title} {slug.replace('-', ' ')}", hub)
    for w, h, label in [(1200, 675, "16x9"), (1200, 900, "4x3"), (1200, 1200, "1x1")]:
        img = _cover(w, h, hub, slug, motif=motif)
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
    img = _cover(1200, 675, "docket", date_str, motif="ticker")
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
    img = _cover(slide_w, slide_h, "docket", date_str + "-cover", motif="ticker")
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
        img = _cover(slide_w, slide_h, hub, f"{date_str}-{n}",
                     motif=pick_motif(str(e.get("headline") or ""), hub))
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
    img = _cover(slide_w, slide_h, "docket", date_str + "-cta", motif="ticker")
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
