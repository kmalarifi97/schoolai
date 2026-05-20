"""Helpers for the Laws of Thermodynamics & Entropy (thermolaws) scene.

Primitives the 12 beats need:
  - stone_tablet:        a faint stone-tablet shape (blank, or inscribed)
  - energy_bar:          a fixed-length total bar split into colored forms
  - engine_box:          a box with heat-in, work-out, waste-heat-out arrows
  - balance_scale:       a two-pan balance with a needle (parity / capped)
  - ink_in_water:        beaker + ink that diffuses (forward); reverse helper
  - coffee_mug:          a mug whose contents cool toward room color
  - scatter_field:       ordered dots that scatter into disorder
  - entropy_bar:         a vertical bar that climbs, labeled 'entropy'
  - time_arrow:          a horizontal arrow labeled 'time'
  - never_stamp:         a struck-through "never" stamp / crossing X
  - small_label:         sans text helper
Pure #000000 void, font="sans" everywhere.
"""

from manim import *
import numpy as np

VOID = "#000000"

STONE      = "#9B958A"
STONE_DARK = "#5C5750"
INK        = "#3A4A66"
WATER      = "#2E5B7A"
HOT        = "#E07B4C"
COLD       = "#5C8AB0"
FUEL       = "#C9A24B"
MOTION     = "#7FB8E8"
HEAT       = "#E0654C"
WORK       = "#7FC8A0"
WASTE      = "#8A5340"
ENTROPY_C  = "#C97FB0"
PARCH      = "#EAE4D5"
NEVER_RED  = "#C0473A"


def small_label(text, pos, color=PARCH, size=26, opacity=0.95, slant=NORMAL):
    return Text(text, font="sans", font_size=size, color=color,
                slant=slant).move_to(pos).set_opacity(opacity)


def stone_tablet(pos, scale=1.0, faint=True):
    """A rounded-top stone tablet, blank. Use .add inscriptions on top."""
    w, h = 2.2 * scale, 3.0 * scale
    body = RoundedRectangle(width=w, height=h, corner_radius=0.45 * scale,
                            fill_color=STONE, fill_opacity=1.0,
                            stroke_color=STONE_DARK, stroke_width=2.4)
    inner = RoundedRectangle(width=w - 0.34 * scale, height=h - 0.34 * scale,
                             corner_radius=0.32 * scale,
                             fill_opacity=0, stroke_color=STONE_DARK,
                             stroke_width=1.4).set_opacity(0.5)
    g = VGroup(body, inner).move_to(pos)
    if faint:
        g.set_opacity(0.38)
    return g


def tablet_inscribe(tablet, label, num="I"):
    """Return a VGroup of inscription text positioned on a tablet."""
    c = tablet.get_center()
    roman = Text(num, font="sans", font_size=46, color=STONE_DARK,
                 weight=BOLD).move_to(c + np.array([0, 0.85, 0]))
    line = Line(c + np.array([-0.7, 0.42, 0]), c + np.array([0.7, 0.42, 0]),
                color=STONE_DARK, stroke_width=2).set_opacity(0.7)
    txt = Text(label, font="sans", font_size=22, color=STONE_DARK,
               line_spacing=0.9).scale_to_fit_width(1.7).move_to(
                   c + np.array([0, -0.3, 0]))
    return VGroup(roman, line, txt)


def tablet_arrow(tablet, color=ENTROPY_C):
    """A one-way arrow inscribed on a tablet (for the 2nd law)."""
    c = tablet.get_center()
    a = Arrow(c + np.array([-0.75, -0.2, 0]), c + np.array([0.75, -0.2, 0]),
              color=color, stroke_width=7, buff=0,
              max_tip_length_to_length_ratio=0.28)
    return a


def energy_bar(center, total_width=5.2, height=0.55, fracs=None, cols=None,
               labels=None):
    """A fixed-length total bar partitioned into colored forms.
    fracs sum to 1.0; the OUTER length never changes between calls."""
    if fracs is None:
        fracs = [0.34, 0.33, 0.33]
    if cols is None:
        cols = [FUEL, MOTION, HEAT]
    if labels is None:
        labels = ["fuel", "motion", "heat"]
    center = np.array(center, dtype=float)
    x0 = center[0] - total_width / 2.0
    segs = VGroup()
    labs = VGroup()
    for f, col, lab in zip(fracs, cols, labels):
        w = total_width * f
        seg = Rectangle(width=max(w, 0.001), height=height,
                        fill_color=col, fill_opacity=1.0,
                        stroke_color=VOID, stroke_width=1.2)
        seg.move_to([x0 + w / 2.0, center[1], 0])
        segs.add(seg)
        if lab:
            labs.add(small_label(lab, [x0 + w / 2.0, center[1] - height,
                                       0], size=20, color=col))
        x0 += w
    frame = Rectangle(width=total_width, height=height,
                      stroke_color=PARCH, stroke_width=2.0,
                      fill_opacity=0).move_to([center[0], center[1], 0])
    return VGroup(segs, frame, labs)


def engine_box(center, scale=1.0, show_waste=True, dial_pct=None):
    """An engine block: heat in (left), work out (right top),
    waste heat out (bottom). dial_pct: optional 0-100 efficiency dial."""
    center = np.array(center, dtype=float)
    box = RoundedRectangle(width=2.2 * scale, height=1.9 * scale,
                           corner_radius=0.14,
                           fill_color="#34302B", fill_opacity=1.0,
                           stroke_color=PARCH, stroke_width=2.4
                           ).move_to(center)
    gear = Circle(radius=0.42 * scale, color=PARCH, stroke_width=2.2,
                  fill_opacity=0).move_to(center)
    spokes = VGroup(*[
        Line(center, center + 0.42 * scale * np.array(
            [np.cos(a), np.sin(a), 0]), color=PARCH, stroke_width=2.0)
        for a in np.linspace(0, TAU, 7)[:-1]])
    elbl = small_label("engine", center + np.array([0, -1.25 * scale, 0]),
                       size=20, color=PARCH)

    hin = Arrow(center + np.array([-3.0, 0, 0]),
                center + np.array([-1.15 * scale, 0, 0]),
                color=HOT, stroke_width=7, buff=0,
                max_tip_length_to_length_ratio=0.22)
    hin_l = small_label("heat in", center + np.array([-2.3, 0.42, 0]),
                        size=20, color=HOT)
    wout = Arrow(center + np.array([1.15 * scale, 0.45, 0]),
                 center + np.array([3.0, 0.45, 0]),
                 color=WORK, stroke_width=7, buff=0,
                 max_tip_length_to_length_ratio=0.22)
    wout_l = small_label("work out", center + np.array([2.3, 0.92, 0]),
                         size=20, color=WORK)

    g = VGroup(box, gear, spokes, elbl, hin, hin_l, wout, wout_l)

    if show_waste:
        wst = Arrow(center + np.array([0, -1.0 * scale, 0]),
                    center + np.array([0, -2.6, 0]),
                    color=WASTE, stroke_width=7, buff=0,
                    max_tip_length_to_length_ratio=0.20)
        wst_l = small_label("waste heat",
                            center + np.array([1.05, -2.05, 0]),
                            size=20, color=WASTE)
        g.add(wst, wst_l)

    if dial_pct is not None:
        d = efficiency_dial(center + np.array([0, 2.4, 0]), pct=dial_pct)
        g.add(d)
    return g


def efficiency_dial(pos, pct=62, scale=1.0):
    """A semicircular dial 0-100% with a needle pinned at pct (< 100)."""
    pos = np.array(pos, dtype=float)
    arc = Arc(radius=0.95 * scale, start_angle=PI, angle=-PI,
              color=PARCH, stroke_width=3).move_arc_center_to(pos)
    # red danger zone near 100%
    red = Arc(radius=0.95 * scale, start_angle=0.0, angle=-PI * 0.18,
              color=NEVER_RED, stroke_width=6).move_arc_center_to(pos)
    ang = PI - PI * (pct / 100.0)
    tip = pos + 0.82 * scale * np.array([np.cos(ang), np.sin(ang), 0])
    needle = Line(pos, tip, color=HOT, stroke_width=4)
    hub = Dot(pos, radius=0.05, color=PARCH)
    lbl = small_label(f"{int(pct)}%", pos + np.array([0, -0.35, 0]),
                      size=22, color=PARCH)
    cap = small_label("100%", pos + np.array([1.05, 0.05, 0]),
                      size=16, color=NEVER_RED)
    return VGroup(arc, red, needle, hub, lbl, cap)


def balance_scale(center, tilt=0.0, scale=1.0):
    """A balance: beam can tilt; needle stuck at parity (tilt small)."""
    center = np.array(center, dtype=float)
    base = Line(center + np.array([0, -1.5, 0]),
                center + np.array([0, 0.6, 0]),
                color=PARCH, stroke_width=4)
    foot = Line(center + np.array([-0.7, -1.5, 0]),
                center + np.array([0.7, -1.5, 0]),
                color=PARCH, stroke_width=4)
    pivot = center + np.array([0, 0.6, 0])
    beam = Line(pivot + np.array([-1.6, 0, 0]),
                pivot + np.array([1.6, 0, 0]),
                color=PARCH, stroke_width=5).rotate(tilt, about_point=pivot)
    lp = beam.get_start()
    rp = beam.get_end()
    panL = Arc(radius=0.5, start_angle=PI, angle=PI, color=WORK,
               stroke_width=3).move_arc_center_to(lp + np.array([0, -0.55, 0]))
    panR = Arc(radius=0.5, start_angle=PI, angle=PI, color=HOT,
               stroke_width=3).move_arc_center_to(rp + np.array([0, -0.55, 0]))
    wL = Line(lp, lp + np.array([0, -0.55, 0]), color=PARCH, stroke_width=2)
    wR = Line(rp, rp + np.array([0, -0.55, 0]), color=PARCH, stroke_width=2)
    needle = Line(pivot, pivot + np.array([0, 0.65, 0]),
                  color=HOT, stroke_width=4).rotate(tilt * 0.4,
                                                    about_point=pivot)
    return VGroup(base, foot, beam, panL, panR, wL, wR, needle)


def make_beaker(center, scale=1.0):
    center = np.array(center, dtype=float)
    w, h = 2.0 * scale, 2.6 * scale
    glass = VGroup(
        Line(center + [-w / 2, h / 2, 0], center + [-w / 2, -h / 2, 0],
             color="#9FB8C8", stroke_width=3),
        Line(center + [-w / 2, -h / 2, 0], center + [w / 2, -h / 2, 0],
             color="#9FB8C8", stroke_width=3),
        Line(center + [w / 2, -h / 2, 0], center + [w / 2, h / 2, 0],
             color="#9FB8C8", stroke_width=3),
    )
    water = Rectangle(width=w - 0.08, height=h - 0.5,
                      fill_color=WATER, fill_opacity=0.45,
                      stroke_width=0).move_to(center + [0, -0.25, 0])
    return VGroup(glass, water), center


def ink_blobs(center, spread=0.0, n=22, base=0.10, seed=3):
    """Ink dots near `center`. spread=0 -> tight drop; spread=1 -> diffused."""
    rng = np.random.default_rng(seed)
    center = np.array(center, dtype=float)
    g = VGroup()
    for _ in range(n):
        ang = rng.uniform(0, TAU)
        r = (base + spread * 1.05) * np.sqrt(rng.uniform(0, 1))
        p = center + np.array([np.cos(ang), np.sin(ang) * 0.85, 0]) * r
        op = float(np.clip(0.85 - 0.45 * spread, 0.30, 0.9))
        d = Dot(p, radius=0.10 - 0.03 * spread, color=INK).set_opacity(op)
        g.add(d)
    return g


def coffee_mug(center, scale=1.0, temp=1.0):
    """A mug. temp 1.0 = hot (HOT color + steam); 0.0 = room (COLD)."""
    center = np.array(center, dtype=float)
    body = RoundedRectangle(width=1.5 * scale, height=1.7 * scale,
                            corner_radius=0.12,
                            fill_color="#E8E2D3", fill_opacity=1.0,
                            stroke_color="#B8B0A0", stroke_width=2.5
                            ).move_to(center)
    liq_col = interpolate_color(ManimColor(COLD), ManimColor(HOT), temp)
    liq = Rectangle(width=1.3 * scale, height=0.34,
                    fill_color=liq_col, fill_opacity=1.0,
                    stroke_width=0).move_to(center + [0, 0.6 * scale, 0])
    handle = Arc(radius=0.42 * scale, start_angle=-PI / 2, angle=PI,
                 color="#B8B0A0", stroke_width=5).move_to(
                     center + [0.95 * scale, 0, 0])
    g = VGroup(body, liq, handle)
    if temp > 0.45:
        steam = VGroup(*[
            ArcBetweenPoints(center + [dx, 0.9 * scale, 0],
                             center + [dx + 0.18, 1.7 * scale, 0],
                             angle=PI * 0.5, color="#C8C8C8",
                             stroke_width=2.5).set_opacity(
                                 0.55 * temp)
            for dx in (-0.3, 0.0, 0.3)])
        g.add(steam)
    return g


def scatter_field(center, disorder=0.0, n_side=5, gap=0.42, seed=11):
    """A grid of dots. disorder=0 -> tidy lattice; 1 -> scattered random."""
    rng = np.random.default_rng(seed)
    center = np.array(center, dtype=float)
    g = VGroup()
    half = (n_side - 1) / 2.0
    for ix in range(n_side):
        for iy in range(n_side):
            base = center + np.array([(ix - half) * gap,
                                      (iy - half) * gap, 0])
            jit = rng.uniform(-1, 1, 3) * np.array([1.6, 1.6, 0]) * disorder
            d = Dot(base + jit, radius=0.09,
                    color=interpolate_color(ManimColor(MOTION),
                                            ManimColor(ENTROPY_C),
                                            disorder))
            g.add(d)
    return g


def entropy_bar(bottom_center, frac=0.2, height=3.2, width=0.55):
    """A vertical entropy bar, fill fraction `frac` (0..1), labeled."""
    bc = np.array(bottom_center, dtype=float)
    frame = Rectangle(width=width, height=height, stroke_color=PARCH,
                      stroke_width=2, fill_opacity=0).move_to(
                          bc + [0, height / 2, 0])
    fh = max(height * frac, 0.001)
    fill = Rectangle(width=width - 0.06, height=fh,
                     fill_color=ENTROPY_C, fill_opacity=1.0,
                     stroke_width=0).move_to(bc + [0, fh / 2, 0])
    lbl = small_label("entropy", bc + [0, -0.32, 0], size=22,
                      color=ENTROPY_C)
    return VGroup(frame, fill, lbl)


def time_arrow(center, length=6.0, color=PARCH):
    center = np.array(center, dtype=float)
    a = Arrow(center + [-length / 2, 0, 0], center + [length / 2, 0, 0],
              color=color, stroke_width=4, buff=0,
              max_tip_length_to_length_ratio=0.06)
    lbl = small_label("time", center + [0, -0.42, 0], size=22, color=color)
    return VGroup(a, lbl)


def never_stamp(center, scale=1.0):
    """A struck-through 'never' — word with a diagonal slash."""
    center = np.array(center, dtype=float)
    word = Text("never", font="sans", font_size=int(34 * scale),
                color=NEVER_RED, weight=BOLD).move_to(center)
    slash = Line(center + np.array([-1.0, -0.45, 0]) * scale,
                 center + np.array([1.0, 0.45, 0]) * scale,
                 color=NEVER_RED, stroke_width=5)
    return VGroup(word, slash)


def cross_out(mobj, color=NEVER_RED):
    """A big X over a mobject's bounding box."""
    c = mobj.get_center()
    w = mobj.width / 2 + 0.2
    h = mobj.height / 2 + 0.2
    return VGroup(
        Line(c + [-w, -h, 0], c + [w, h, 0], color=color, stroke_width=6),
        Line(c + [-w, h, 0], c + [w, -h, 0], color=color, stroke_width=6),
    )
