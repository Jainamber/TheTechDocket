"""Minimal SVG path parser + Pillow-only rasteriser for the vendored Tabler
icon paths in `engine/icons.py`. No cairo / svg render libraries — this
flattens the subset of the SVG path grammar Tabler's outline icons use
(M m L l H h V v C c S s Q q T t A a Z z) into polylines in the icon's
24x24 unit grid, then draws them with Pillow at a supersampled resolution
and downscales for anti-aliasing.
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

_COMMANDS = set("MmLlHhVvCcSsQqTtAaZz")


class _Scanner:
    """Cursor over an SVG path `d` string. Numbers follow the SVG grammar
    (optional sign, digits, optional decimal point + digits, optional
    exponent); commas and whitespace are both valid separators and may be
    omitted entirely between a negative number and its predecessor (e.g.
    "1-2") or between a decimal number and what follows (e.g. "1.5.5" is
    two numbers, "1.5" and ".5"). Arc flags are single '0'/'1' characters
    that may be glued to the following number (e.g. "0 01.5" is flag=0,
    flag=0, number=1.5)."""

    def __init__(self, s: str):
        self.s = s
        self.i = 0
        self.n = len(s)

    def _skip_sep(self) -> None:
        s, n = self.s, self.n
        i = self.i
        while i < n and (s[i].isspace() or s[i] == ","):
            i += 1
        self.i = i

    def eof(self) -> bool:
        self._skip_sep()
        return self.i >= self.n

    def more_command_ahead(self) -> bool:
        self._skip_sep()
        return self.i < self.n and self.s[self.i].isalpha()

    def read_command(self) -> str:
        self._skip_sep()
        c = self.s[self.i]
        if c not in _COMMANDS:
            raise ValueError(f"Unsupported path command {c!r} at {self.i} in {self.s!r}")
        self.i += 1
        return c

    def read_number(self) -> float:
        self._skip_sep()
        s, n = self.s, self.n
        start = i = self.i
        if i < n and s[i] in "+-":
            i += 1
        had_digits = False
        while i < n and s[i].isdigit():
            i += 1
            had_digits = True
        if i < n and s[i] == ".":
            i += 1
            while i < n and s[i].isdigit():
                i += 1
                had_digits = True
        if not had_digits:
            raise ValueError(f"Expected number at {start} in {self.s!r}")
        if i < n and s[i] in "eE":
            j = i + 1
            if j < n and s[j] in "+-":
                j += 1
            if j < n and s[j].isdigit():
                i = j
                while i < n and s[i].isdigit():
                    i += 1
        val = float(s[start:i])
        self.i = i
        return val

    def read_flag(self) -> float:
        self._skip_sep()
        s = self.s
        if self.i >= self.n or s[self.i] not in "01":
            raise ValueError(f"Expected arc flag (0/1) at {self.i} in {self.s!r}")
        val = float(s[self.i])
        self.i += 1
        return val


Point = tuple[float, float]


def _flatten_cubic(p0: Point, p1: Point, p2: Point, p3: Point, n: int = 16) -> list[Point]:
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        a, b, c, dd = mt ** 3, 3 * mt ** 2 * t, 3 * mt * t ** 2, t ** 3
        x = a * p0[0] + b * p1[0] + c * p2[0] + dd * p3[0]
        y = a * p0[1] + b * p1[1] + c * p2[1] + dd * p3[1]
        pts.append((x, y))
    return pts


def _flatten_quad(p0: Point, p1: Point, p2: Point, n: int = 16) -> list[Point]:
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        a, b, c = mt ** 2, 2 * mt * t, t ** 2
        x = a * p0[0] + b * p1[0] + c * p2[0]
        y = a * p0[1] + b * p1[1] + c * p2[1]
        pts.append((x, y))
    return pts


def _angle(ux: float, uy: float, vx: float, vy: float) -> float:
    len_u = math.hypot(ux, uy)
    len_v = math.hypot(vx, vy)
    denom = len_u * len_v
    if denom == 0:
        return 0.0
    cos_val = max(-1.0, min(1.0, (ux * vx + uy * vy) / denom))
    ang = math.acos(cos_val)
    if (ux * vy - uy * vx) < 0:
        ang = -ang
    return ang


def _flatten_arc(p0: Point, rx: float, ry: float, x_axis_rotation_deg: float,
                  large_arc_flag: float, sweep_flag: float, p1: Point,
                  min_seg: int = 6, deg_step: float = 5.0) -> list[Point]:
    """SVG spec F.6.5 endpoint-to-center arc parameterisation, F.6.6 radius
    correction, sampled every ~`deg_step` degrees (at least `min_seg`
    segments)."""
    x1, y1 = p0
    x2, y2 = p1
    if x1 == x2 and y1 == y2:
        return [p0]
    if rx == 0 or ry == 0:
        return [p0, p1]

    rx, ry = abs(rx), abs(ry)
    phi = math.radians(x_axis_rotation_deg % 360)
    cos_phi, sin_phi = math.cos(phi), math.sin(phi)

    dx2, dy2 = (x1 - x2) / 2.0, (y1 - y2) / 2.0
    x1p = cos_phi * dx2 + sin_phi * dy2
    y1p = -sin_phi * dx2 + cos_phi * dy2

    # F.6.6: scale up rx/ry if the requested radii are too small to span
    # the chord at all.
    lam = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
    if lam > 1:
        s = math.sqrt(lam)
        rx *= s
        ry *= s

    rx_sq, ry_sq = rx * rx, ry * ry
    x1p_sq, y1p_sq = x1p * x1p, y1p * y1p

    num = rx_sq * ry_sq - rx_sq * y1p_sq - ry_sq * x1p_sq
    den = rx_sq * y1p_sq + ry_sq * x1p_sq
    co = math.sqrt(max(0.0, num / den)) if den else 0.0
    if large_arc_flag == sweep_flag:
        co = -co

    cxp = co * (rx * y1p) / ry
    cyp = co * (-ry * x1p) / rx

    cx = cos_phi * cxp - sin_phi * cyp + (x1 + x2) / 2.0
    cy = sin_phi * cxp + cos_phi * cyp + (y1 + y2) / 2.0

    ux, uy = (x1p - cxp) / rx, (y1p - cyp) / ry
    vx, vy = (-x1p - cxp) / rx, (-y1p - cyp) / ry

    theta1 = _angle(1.0, 0.0, ux, uy)
    dtheta = _angle(ux, uy, vx, vy)

    if sweep_flag == 0 and dtheta > 0:
        dtheta -= 2 * math.pi
    elif sweep_flag == 1 and dtheta < 0:
        dtheta += 2 * math.pi

    dtheta_deg = abs(math.degrees(dtheta))
    n = max(min_seg, int(math.ceil(dtheta_deg / deg_step)))

    pts = []
    for i in range(n + 1):
        t = theta1 + dtheta * i / n
        cos_t, sin_t = math.cos(t), math.sin(t)
        x = cx + rx * cos_t * cos_phi - ry * sin_t * sin_phi
        y = cy + rx * cos_t * sin_phi + ry * sin_t * cos_phi
        pts.append((x, y))
    return pts


def parse_path(d: str) -> list[list[Point]]:
    """Parse an SVG path `d` string into a list of flattened polylines
    (subpaths), each a list of (x, y) points in the path's own coordinate
    space (Tabler icons use a 24x24 grid)."""
    sc = _Scanner(d)
    subpaths: list[list[Point]] = []
    current: list[Point] = []
    cur = (0.0, 0.0)
    start = (0.0, 0.0)
    prev_ctrl: Point | None = None
    cmd: str | None = None
    last_cmd: str | None = None

    while not sc.eof():
        if sc.more_command_ahead():
            cmd = sc.read_command()
        else:
            if cmd is None:
                raise ValueError(f"Path data must start with a command: {d!r}")
            # Implicit repetition: a bare coordinate pair after M/m is an
            # implicit L/l; any other command simply repeats.
            if cmd == "M":
                cmd = "L"
            elif cmd == "m":
                cmd = "l"

        if cmd in ("M", "m"):
            x, y = sc.read_number(), sc.read_number()
            if cmd == "m":
                x, y = x + cur[0], y + cur[1]
            cur = (x, y)
            start = cur
            if current:
                subpaths.append(current)
            current = [cur]
            prev_ctrl = None

        elif cmd in ("L", "l"):
            x, y = sc.read_number(), sc.read_number()
            if cmd == "l":
                x, y = x + cur[0], y + cur[1]
            cur = (x, y)
            current.append(cur)
            prev_ctrl = None

        elif cmd in ("H", "h"):
            x = sc.read_number()
            if cmd == "h":
                x += cur[0]
            cur = (x, cur[1])
            current.append(cur)
            prev_ctrl = None

        elif cmd in ("V", "v"):
            y = sc.read_number()
            if cmd == "v":
                y += cur[1]
            cur = (cur[0], y)
            current.append(cur)
            prev_ctrl = None

        elif cmd in ("C", "c"):
            x1, y1 = sc.read_number(), sc.read_number()
            x2, y2 = sc.read_number(), sc.read_number()
            x, y = sc.read_number(), sc.read_number()
            if cmd == "c":
                x1, y1 = x1 + cur[0], y1 + cur[1]
                x2, y2 = x2 + cur[0], y2 + cur[1]
                x, y = x + cur[0], y + cur[1]
            pts = _flatten_cubic(cur, (x1, y1), (x2, y2), (x, y))
            current.extend(pts[1:])
            cur = (x, y)
            prev_ctrl = (x2, y2)

        elif cmd in ("S", "s"):
            x2, y2 = sc.read_number(), sc.read_number()
            x, y = sc.read_number(), sc.read_number()
            if cmd == "s":
                x2, y2 = x2 + cur[0], y2 + cur[1]
                x, y = x + cur[0], y + cur[1]
            if prev_ctrl is not None and last_cmd in ("C", "c", "S", "s"):
                x1, y1 = 2 * cur[0] - prev_ctrl[0], 2 * cur[1] - prev_ctrl[1]
            else:
                x1, y1 = cur
            pts = _flatten_cubic(cur, (x1, y1), (x2, y2), (x, y))
            current.extend(pts[1:])
            cur = (x, y)
            prev_ctrl = (x2, y2)

        elif cmd in ("Q", "q"):
            x1, y1 = sc.read_number(), sc.read_number()
            x, y = sc.read_number(), sc.read_number()
            if cmd == "q":
                x1, y1 = x1 + cur[0], y1 + cur[1]
                x, y = x + cur[0], y + cur[1]
            pts = _flatten_quad(cur, (x1, y1), (x, y))
            current.extend(pts[1:])
            cur = (x, y)
            prev_ctrl = (x1, y1)

        elif cmd in ("T", "t"):
            x, y = sc.read_number(), sc.read_number()
            if cmd == "t":
                x, y = x + cur[0], y + cur[1]
            if prev_ctrl is not None and last_cmd in ("Q", "q", "T", "t"):
                x1, y1 = 2 * cur[0] - prev_ctrl[0], 2 * cur[1] - prev_ctrl[1]
            else:
                x1, y1 = cur
            pts = _flatten_quad(cur, (x1, y1), (x, y))
            current.extend(pts[1:])
            cur = (x, y)
            prev_ctrl = (x1, y1)

        elif cmd in ("A", "a"):
            rx, ry = sc.read_number(), sc.read_number()
            x_rot = sc.read_number()
            large_arc = sc.read_flag()
            sweep = sc.read_flag()
            x, y = sc.read_number(), sc.read_number()
            if cmd == "a":
                x, y = x + cur[0], y + cur[1]
            pts = _flatten_arc(cur, rx, ry, x_rot, large_arc, sweep, (x, y))
            current.extend(pts[1:])
            cur = (x, y)
            prev_ctrl = None

        elif cmd in ("Z", "z"):
            if current and current[-1] != start:
                current.append(start)
            cur = start
            prev_ctrl = None

        else:  # pragma: no cover - _Scanner.read_command already validates
            raise ValueError(f"Unsupported path command {cmd!r}")

        last_cmd = cmd

    if current:
        subpaths.append(current)
    return subpaths


def render_icon(paths_d: list[str], size: int, color: tuple[int, int, int],
                 stroke: float = 2.0, ss: int = 4) -> Image.Image:
    """Rasterise a list of 24x24-grid path `d` strings into an RGBA image
    of `size`x`size`, stroked (not filled) in `color`. Draws at `ss`x
    supersample on a transparent canvas, then downsamples with LANCZOS."""
    ss = max(1, int(ss))
    ss_size = max(1, int(round(size * ss)))
    scale = ss_size / 24.0
    stroke_px = stroke * ss_size / 24.0
    radius = stroke_px / 2.0
    line_width = max(1, round(stroke_px))
    rgba = (color[0], color[1], color[2], 255)

    img = Image.new("RGBA", (ss_size, ss_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for d in paths_d:
        for poly in parse_path(d):
            if not poly:
                continue
            pts = [(x * scale, y * scale) for (x, y) in poly]
            if len(pts) >= 2:
                draw.line(pts, fill=rgba, width=line_width, joint="curve")
            # Round caps + safety circles at every vertex (start, end, and
            # interior joints) so short/degenerate segments (e.g. Tabler's
            # "h.01" dot trick) and curve joints all render as solid rounded
            # strokes instead of showing gaps or square joints.
            for (px, py) in pts:
                draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=rgba)

    if ss > 1:
        img = img.resize((size, size), Image.LANCZOS)
        # Lanczos ringing (Gibbs phenomenon) leaves a faint few-pixel halo of
        # near-zero alpha (single-digit out of 255) just outside the true
        # stroked edge. It's visually inert but pads out the alpha bbox, so
        # clamp it away; real antialiased edge pixels sit far above this.
        r, g, b, a = img.split()
        a = a.point(lambda v: 0 if v < 12 else v)
        img = Image.merge("RGBA", (r, g, b, a))
    return img


def render_icon_by_name(name: str, size: int, color: tuple[int, int, int],
                         stroke: float = 2.0, ss: int = 4) -> Image.Image:
    """Convenience wrapper: look the icon up in `engine.icons.ICONS` (with
    the same fallback rules as `resolve_icon`) and rasterise it."""
    from . import icons as _icons
    resolved = name if name in _icons.ICONS else _icons.resolve_icon(None)
    return render_icon(_icons.ICONS[resolved], size, color, stroke, ss)
