"""Helpers for the Equivalence Principle (equivalence) scene.

Primitives:
- split_word_mass: the word "mass" that cleanly splits into two halves
- make_block: a solid block (the pushed/hung object)
- make_hand: a simple pushing hand
- frictionless_plane: a hatched ground line marked frictionless
- spring_scale: a hanging spring scale the block dangles from
- make_ball: a simple sphere ball (heavy / light variants)
- side_panel: a labelled framed panel (Newton-side / Einstein-side)
- sealed_box: a sealed box with a small standing figure inside;
  optional thrust flame underneath (the rocket variant)
- small_label / big_text: text helpers (font=sans, on the VOID)

Reuses grav_helpers where natural.
"""

from manim import *
import numpy as np

from grav_helpers import make_earth  # noqa: F401

VOID = "#000000"

INK      = "#EAE4D5"   # warm off-white text
DIM      = "#8C98A6"   # dim label grey-blue
INERT    = "#E2B85A"   # inertial mass (amber)
GRAV     = "#7FB8E8"   # gravitational mass (blue)
BLOCK_F  = "#3A4250"   # block fill
BLOCK_S  = "#9AA8C0"   # block stroke
FLAME_O  = "#F2A444"   # flame outer
FLAME_I  = "#FFE08A"   # flame inner
EQ_COL   = "#EAE4D5"


def big_text(text, pos, size=60, color=INK, weight=NORMAL):
    return Text(text, font="sans", font_size=size, color=color,
                weight=weight).move_to(pos)


def small_label(text, pos, color=DIM, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def split_word_mass(center=ORIGIN, size=72, color=INK):
    """Returns (whole, left_half, right_half).

    `whole` is the centered word. left_half/right_half are the two
    pieces ('ma' / 'ss') already positioned to coincide with `whole`,
    so you can FadeOut(whole), FadeIn(halves) then animate them apart.
    """
    whole = Text("mass", font="sans", font_size=size, color=color
                 ).move_to(center)
    left = Text("ma", font="sans", font_size=size, color=color)
    right = Text("ss", font="sans", font_size=size, color=color)
    grp = VGroup(left, right).arrange(RIGHT, buff=0.04).move_to(center)
    return whole, left, right


def make_block(pos=ORIGIN, w=1.3, h=1.0, fill=BLOCK_F, stroke=BLOCK_S):
    body = Rectangle(width=w, height=h, fill_color=fill, fill_opacity=1,
                     stroke_color=stroke, stroke_width=2.0)
    hl = Rectangle(width=w * 0.30, height=h * 0.16,
                   fill_color="#C8D2E0", fill_opacity=0.30,
                   stroke_width=0).move_to([-w * 0.22, h * 0.26, 0])
    return VGroup(body, hl).move_to(pos)


def make_hand(pos=ORIGIN, facing=RIGHT):
    """A simple stylised pushing hand: palm + thumb, pointing `facing`."""
    palm = RoundedRectangle(width=0.62, height=0.78, corner_radius=0.16,
                            fill_color="#D8B48C", fill_opacity=1,
                            stroke_color="#A5835E", stroke_width=1.6)
    thumb = Ellipse(width=0.22, height=0.34, fill_color="#D8B48C",
                    fill_opacity=1, stroke_color="#A5835E",
                    stroke_width=1.4).move_to([0, 0.42, 0])
    cuff = Rectangle(width=0.66, height=0.22, fill_color="#5A6E80",
                     fill_opacity=1, stroke_width=0).move_to([-0.34, 0, 0])
    g = VGroup(cuff, palm, thumb)
    ang = np.arctan2(facing[1], facing[0])
    g.rotate(ang)
    return g.move_to(pos)


def frictionless_plane(y=-1.6, x0=-6.0, x1=6.0, color=DIM):
    """A ground line with light hatch marks + a frictionless tag."""
    line = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=2.5)
    hatch = VGroup()
    n = 22
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        hatch.add(Line([x, y, 0], [x - 0.18, y - 0.20, 0],
                       color=color, stroke_width=1.4).set_opacity(0.55))
    tag = small_label("frictionless", [x1 - 1.1, y - 0.45, 0],
                      color=color, size=20)
    return VGroup(line, hatch, tag)


def spring_scale(top=np.array([0, 3.0, 0]), coils=7, length=1.6,
                 width=0.42, color=BLOCK_S):
    """A hanging spring (zig-zag) anchored at `top`, with a small hook
    at the bottom. Returns (group, hook_point)."""
    anchor = Line(top + np.array([-0.5, 0, 0]),
                  top + np.array([0.5, 0, 0]),
                  color=color, stroke_width=3)
    pts = [top]
    for k in range(coils):
        frac = (k + 0.5) / coils
        side = -1 if k % 2 == 0 else 1
        pts.append(top + np.array([side * width / 2,
                                   -length * frac, 0]))
    bottom = top + np.array([0, -length - 0.12, 0])
    pts.append(top + np.array([0, -length, 0]))
    pts.append(bottom)
    spring = VMobject(stroke_color=color, stroke_width=2.4)
    spring.set_points_as_corners([np.array(p, dtype=float) for p in pts])
    hook = Arc(radius=0.10, start_angle=PI, angle=-PI,
               color=color, stroke_width=2.4).move_to(
                   bottom + np.array([0, -0.10, 0]))
    g = VGroup(anchor, spring, hook)
    hook_point = bottom + np.array([0, -0.20, 0])
    return g, hook_point


def make_ball(pos=ORIGIN, radius=0.40, big=True):
    """A simple shaded ball. big -> dark heavy ball, else pale light ball."""
    if big:
        fill, stroke, hl = "#3A3F47", "#7C8696", "#AEB8C6"
    else:
        fill, stroke, hl = "#C8CEDA", "#8C98A6", WHITE
    body = Circle(radius=radius, fill_color=fill, fill_opacity=1,
                  stroke_color=stroke, stroke_width=1.8)
    sheen = (Ellipse(width=radius * 0.55, height=radius * 0.30,
                     fill_color=hl, fill_opacity=0.45, stroke_width=0)
             .shift(np.array([-radius * 0.32, radius * 0.36, 0])))
    return VGroup(body, sheen).move_to(pos)


def _stick_figure(scale=1.0, color=INK):
    head = Circle(radius=0.16 * scale, color=color, stroke_width=2.6,
                  fill_opacity=0).move_to([0, 0.78 * scale, 0])
    body = Line([0, 0.62 * scale, 0], [0, 0.04 * scale, 0],
                color=color, stroke_width=2.6)
    arms = Line([-0.26 * scale, 0.46 * scale, 0],
                [0.26 * scale, 0.46 * scale, 0],
                color=color, stroke_width=2.6)
    leg_l = Line([0, 0.04 * scale, 0], [-0.20 * scale, -0.46 * scale, 0],
                 color=color, stroke_width=2.6)
    leg_r = Line([0, 0.04 * scale, 0], [0.20 * scale, -0.46 * scale, 0],
                 color=color, stroke_width=2.6)
    return VGroup(head, body, arms, leg_l, leg_r)


def sealed_box(pos=ORIGIN, size=2.6, with_flame=False, color=BLOCK_S):
    """A sealed box with an identical small figure standing on its floor.
    If with_flame, a thrust flame is drawn below it (the rocket case)."""
    box = Square(side_length=size, fill_color="#10141A", fill_opacity=1,
                 stroke_color=color, stroke_width=2.6)
    floor = Line([-size / 2, -size / 2, 0], [size / 2, -size / 2, 0],
                 color=color, stroke_width=3.2)
    fig = _stick_figure(scale=size / 2.6, color=INK)
    fig.move_to([0, -size / 2 + 0.50 * (size / 2.6), 0])
    g = VGroup(box, floor, fig)
    parts = {"box": box, "fig": fig}
    if with_flame:
        cx, by = 0.0, -size / 2
        outer = Polygon([cx - 0.34, by, 0], [cx + 0.34, by, 0],
                        [cx, by - 0.95, 0],
                        fill_color=FLAME_O, fill_opacity=0.95,
                        stroke_width=0)
        inner = Polygon([cx - 0.17, by, 0], [cx + 0.17, by, 0],
                        [cx, by - 0.55, 0],
                        fill_color=FLAME_I, fill_opacity=0.95,
                        stroke_width=0)
        flame = VGroup(outer, inner)
        g.add(flame)
        parts["flame"] = flame
    g.move_to(pos)
    return g, parts


def side_panel(pos=ORIGIN, w=5.4, h=4.4, title="Newton",
               accent=DIM):
    """A framed panel with a title bar — Newton-side / Einstein-side."""
    frame = Rectangle(width=w, height=h, stroke_color=accent,
                      stroke_width=2.2, fill_opacity=0)
    bar = small_label(title, pos + np.array([0, h / 2 + 0.34, 0]),
                      color=accent, size=28)
    g = VGroup(frame, bar).move_to([pos[0], pos[1], 0])
    frame.move_to(pos)
    bar.move_to(pos + np.array([0, h / 2 + 0.34, 0]))
    return VGroup(frame, bar)


def gravity_arrow(start, length=1.1, color=GRAV, width=5):
    s = np.array(start, dtype=float)
    e = s + np.array([0, -length, 0])
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.28)


def push_arrow(start, length=1.0, color=INERT, width=5):
    s = np.array(start, dtype=float)
    e = s + np.array([length, 0, 0])
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.28)
