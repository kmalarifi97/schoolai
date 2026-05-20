"""Helpers for the Temperature vs Thermal Energy (tempvsthermal) scene.

Primitives the 12 beats need:
  - match with a flame
  - a steaming bathtub
  - a thermometer with a settable reading
  - a particle swarm that vibrates / collides
  - one highlighted particle whose amplitude ties to a thermometer
  - sparse-fast particles vs a vast crowd of gentle particles
  - per-particle tiny energy bars merging into one big bar
  - a room outline that fills with warmth
All on pure #000000, font="sans".
"""

from manim import *
import numpy as np

VOID = "#000000"

FLAME_HOT   = "#FF6A2A"
FLAME_CORE  = "#FFD27A"
MATCH_WOOD  = "#C9A36B"
MATCH_HEAD  = "#7A4A3A"
WATER_BLUE  = "#5FA8C8"
WATER_DEEP  = "#3C7C96"
TUB_WHITE   = "#D8DCE0"
TUB_SHADE   = "#9AA0A6"
STEAM_COL   = "#BFD4DC"
THERM_GLASS = "#CFCFD4"
THERM_RED   = "#E5563B"
PART_COOL   = "#8FB8D8"
PART_HOT    = "#FF7A3C"
LABEL_COL   = "#EAE4D5"
ROOM_COL    = "#7E8A94"
WARM_FILL   = "#E58A4C"
BAR_COL     = "#E5A23C"


# ---------------------------------------------------------------- match
def make_match(pos=ORIGIN, scale=1.0, lit=True):
    """A matchstick lying with the head up; optional flame."""
    stick = RoundedRectangle(width=0.18 * scale, height=2.0 * scale,
                             corner_radius=0.06 * scale,
                             fill_color=MATCH_WOOD, fill_opacity=1,
                             stroke_width=0)
    head = Ellipse(width=0.30 * scale, height=0.34 * scale,
                   fill_color=MATCH_HEAD, fill_opacity=1, stroke_width=0)
    head.next_to(stick, UP, buff=-0.05 * scale)
    grp = VGroup(stick, head)
    if lit:
        grp.add(make_flame(scale=scale).next_to(head, UP, buff=-0.04 * scale))
    return grp.move_to(pos)


def make_flame(scale=1.0):
    """Teardrop flame: outer hot envelope + bright core."""
    def teardrop(w, h, col, op):
        pts = []
        n = 40
        for k in range(n + 1):
            a = PI * k / n
            x = w * np.sin(a)
            y = h * (0.5 - 0.5 * np.cos(a))
            pts.append([x, y, 0])
        for k in range(n + 1):
            a = PI * (n - k) / n
            x = -w * np.sin(a)
            y = h * (0.5 - 0.5 * np.cos(a))
            pts.append([x, y, 0])
        sh = VMobject(fill_color=col, fill_opacity=op, stroke_width=0)
        sh.set_points_smoothly([np.array(p) for p in pts])
        return sh
    outer = teardrop(0.28 * scale, 0.95 * scale, FLAME_HOT, 0.92)
    core = teardrop(0.14 * scale, 0.55 * scale, FLAME_CORE, 1.0)
    core.align_to(outer, DOWN).shift(UP * 0.05 * scale)
    return VGroup(outer, core)


# ---------------------------------------------------------------- bathtub
def make_bathtub(pos=ORIGIN, scale=1.0, steam=True):
    """A clawfoot-ish tub with water and rising steam wisps."""
    shell = VMobject(fill_color=TUB_WHITE, fill_opacity=1,
                     stroke_color=TUB_SHADE, stroke_width=2)
    w, h = 3.2 * scale, 1.5 * scale
    pts = [
        [-w / 2, h / 2, 0], [-w / 2, -h / 2 + 0.25 * scale, 0],
        [-w / 2 + 0.30 * scale, -h / 2, 0], [w / 2 - 0.30 * scale, -h / 2, 0],
        [w / 2, -h / 2 + 0.25 * scale, 0], [w / 2, h / 2, 0],
    ]
    shell.set_points_as_corners([np.array(p) for p in pts] + [np.array(pts[0])])
    rim = Ellipse(width=w, height=0.42 * scale, fill_color=TUB_WHITE,
                  fill_opacity=1, stroke_color=TUB_SHADE, stroke_width=2
                  ).move_to([0, h / 2, 0])
    water = Ellipse(width=w - 0.36 * scale, height=0.30 * scale,
                    fill_color=WATER_BLUE, fill_opacity=1,
                    stroke_color=WATER_DEEP, stroke_width=2
                    ).move_to([0, h / 2 - 0.05 * scale, 0])
    foot_l = RoundedRectangle(width=0.26 * scale, height=0.34 * scale,
                              corner_radius=0.08 * scale,
                              fill_color=TUB_SHADE, fill_opacity=1,
                              stroke_width=0
                              ).move_to([-w / 2 + 0.45 * scale,
                                         -h / 2 - 0.15 * scale, 0])
    foot_r = foot_l.copy().move_to([w / 2 - 0.45 * scale,
                                    -h / 2 - 0.15 * scale, 0])
    grp = VGroup(shell, foot_l, foot_r, rim, water)
    if steam:
        grp.add(make_steam(width=w * 0.7, base_y=h / 2 + 0.05 * scale,
                            scale=scale))
    return grp.move_to(pos)


def make_steam(width=2.0, base_y=0.0, scale=1.0, n=3):
    """A few gentle sinuous steam wisps."""
    g = VGroup()
    for i in range(n):
        x0 = -width / 2 + width * (i + 0.5) / n
        pts = []
        for k in range(22):
            t = k / 21
            y = base_y + t * 1.5 * scale
            x = x0 + 0.22 * scale * np.sin(t * 3.4 * PI + i)
            pts.append([x, y, 0])
        w = VMobject(stroke_color=STEAM_COL, stroke_width=3,
                     fill_opacity=0)
        w.set_points_smoothly([np.array(p) for p in pts])
        w.set_stroke(opacity=0.55)
        g.add(w)
    return g


# ---------------------------------------------------------------- thermometer
def make_thermometer(pos=ORIGIN, scale=1.0, fill_frac=0.5,
                     label=None, label_col=LABEL_COL):
    """Vertical thermometer; fill_frac in [0,1] sets the red column."""
    fill_frac = float(np.clip(fill_frac, 0.04, 1.0))
    stem_h = 2.6 * scale
    stem_w = 0.30 * scale
    bulb_r = 0.34 * scale
    glass = VGroup(
        RoundedRectangle(width=stem_w, height=stem_h,
                         corner_radius=stem_w / 2,
                         fill_color=VOID, fill_opacity=1,
                         stroke_color=THERM_GLASS, stroke_width=2.4),
        Circle(radius=bulb_r, fill_color=THERM_RED, fill_opacity=1,
               stroke_color=THERM_GLASS, stroke_width=2.4),
    )
    glass[1].move_to(glass[0].get_bottom() + DOWN * (bulb_r * 0.55))
    col_h = stem_h * 0.92 * fill_frac
    col = RoundedRectangle(width=stem_w * 0.52, height=max(col_h, 0.05),
                           corner_radius=stem_w * 0.26,
                           fill_color=THERM_RED, fill_opacity=1,
                           stroke_width=0)
    col.move_to(glass[0].get_bottom() + UP * (col_h / 2 + 0.02 * scale))
    grp = VGroup(glass, col)
    # tick marks
    ticks = VGroup()
    for k in range(1, 6):
        ty = glass[0].get_bottom()[1] + stem_h * 0.16 * k
        ticks.add(Line([stem_w / 2, ty, 0], [stem_w / 2 + 0.10 * scale, ty, 0],
                        stroke_color=THERM_GLASS, stroke_width=1.6))
    grp.add(ticks)
    grp.move_to(pos)
    if label:
        lab = Text(label, font="sans", font_size=24 * scale,
                   color=label_col).next_to(grp, DOWN, buff=0.25 * scale)
        grp.add(lab)
    return grp


# ---------------------------------------------------------------- particles
def particle_swarm(center, n=18, radius=1.4, hot=False, seed=0,
                   dot_r=0.09):
    """A cluster of particle dots. Returns VGroup; positions random in disc."""
    rng = np.random.default_rng(seed)
    col = PART_HOT if hot else PART_COOL
    g = VGroup()
    for _ in range(n):
        a = rng.uniform(0, TAU)
        rr = radius * np.sqrt(rng.uniform(0, 1))
        p = np.array(center, dtype=float) + np.array(
            [rr * np.cos(a), rr * np.sin(a), 0])
        d = Dot(point=p, radius=dot_r, color=col)
        d.set_fill(col, opacity=0.95)
        g.add(d)
    return g


def jiggle(scene, group, amp=0.16, steps=5, run_time=1.0, seed=1):
    """Animate every dot doing a small random vibration about its center."""
    rng = np.random.default_rng(seed)
    homes = [d.get_center().copy() for d in group]
    per = run_time / steps
    for _ in range(steps):
        anims = []
        for d, h in zip(group, homes):
            off = rng.uniform(-amp, amp, size=2)
            anims.append(d.animate.move_to(h + np.array([off[0], off[1], 0])))
        scene.play(*anims, run_time=per, rate_func=rate_functions.linear)
    scene.play(*[d.animate.move_to(h) for d, h in zip(group, homes)],
               run_time=per, rate_func=rate_functions.linear)


def energy_bar(height, pos=ORIGIN, width=0.7, color=BAR_COL, label=None,
               label_col=LABEL_COL):
    """A vertical filled bar, grows from its bottom edge."""
    bar = Rectangle(width=width, height=max(height, 0.04),
                    fill_color=color, fill_opacity=0.9, stroke_width=0)
    bar.move_to(pos, aligned_edge=DOWN)
    if label:
        lab = Text(label, font="sans", font_size=22, color=label_col)
        lab.next_to(bar, DOWN, buff=0.22)
        return VGroup(bar, lab)
    return VGroup(bar)


def make_room(pos=ORIGIN, scale=1.0):
    """A simple house/room outline (rectangle with a roof)."""
    body = Rectangle(width=2.6 * scale, height=2.0 * scale,
                     stroke_color=ROOM_COL, stroke_width=3,
                     fill_opacity=0)
    roof = Polygon([-1.45 * scale, 1.0 * scale, 0],
                   [0, 2.0 * scale, 0],
                   [1.45 * scale, 1.0 * scale, 0],
                   stroke_color=ROOM_COL, stroke_width=3, fill_opacity=0)
    return VGroup(body, roof).move_to(pos)


def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def q_mark(pos, size=60, color=LABEL_COL):
    return Text("?", font="sans", font_size=size, color=color).move_to(pos)
