"""Helpers for the Work–Energy Theorem (workenergy) scene.

Primitives:
  - make_figure: a simple stick person, optionally in a "straining" pose
  - make_wall: a tall solid wall
  - sweat_drop: a small drop
  - make_cart: a little cart with wheels
  - force_arrow / displacement_arrow: labelled arrows
  - work_region: a shaded force x distance rectangle
  - energy_bar: a vertical "energy of motion" bar that can fill / drain
  - small_label / big_label: text helpers (font=sans)

Pure #000000 void. font="sans" everywhere.
"""

from manim import *
import numpy as np

VOID = "#000000"

BODY_COL   = "#EAE4D5"   # warm off-white for the figure
WALL_COL   = "#5A5A62"
WALL_EDGE  = "#8C8C96"
CART_COL   = "#C9A14A"   # warm cart
CART_DARK  = "#6E5A22"
FORCE_COL  = "#E8825A"   # force = warm orange
DISP_COL   = "#7FB8E8"   # displacement = cool blue
WORK_COL   = "#9CC97F"   # work shading = green
ENERGY_COL = "#9CC97F"   # motion-energy bar = green (same family as work)
NEG_COL    = "#E05A5A"   # negative work / draining = red
SWEAT_COL  = "#7FB8E8"
LABEL_COL  = "#EAE4D5"
FAINT      = "#8C98A6"


# ----------------------------------------------------------------------
def make_figure(pos=ORIGIN, scale=1.0, straining=False, facing=1):
    """A simple stick figure. If straining, arms reach forward (toward
    `facing`: +1 = right, -1 = left) and the body leans into the push."""
    s = scale
    g = VGroup()
    head = Circle(radius=0.22 * s, color=BODY_COL, stroke_width=4,
                  fill_opacity=0)
    head.move_to(UP * 1.30 * s)
    # torso
    torso = Line(UP * 1.08 * s, DOWN * 0.05 * s, color=BODY_COL,
                 stroke_width=5)
    # legs
    leg_l = Line(DOWN * 0.05 * s, DOWN * 0.95 * s + LEFT * 0.30 * s,
                 color=BODY_COL, stroke_width=5)
    leg_r = Line(DOWN * 0.05 * s, DOWN * 0.95 * s + RIGHT * 0.30 * s,
                 color=BODY_COL, stroke_width=5)
    g.add(head, torso, leg_l, leg_r)

    if straining:
        # both arms reach forward toward `facing`, slightly apart
        sh = UP * 0.85 * s
        hand = np.array([facing * 0.72 * s, 0.55 * s, 0])
        arm_u = Line(sh, hand + UP * 0.12 * s, color=BODY_COL,
                     stroke_width=5)
        arm_l = Line(sh, hand - UP * 0.12 * s, color=BODY_COL,
                     stroke_width=5)
        g.add(arm_u, arm_l)
        g.rotate(-facing * 0.12)  # lean into the push
    else:
        sh = UP * 0.85 * s
        arm_l = Line(sh, sh + np.array([facing * 0.55 * s, -0.45 * s, 0]),
                     color=BODY_COL, stroke_width=5)
        arm_r = Line(sh, sh + np.array([-facing * 0.30 * s, -0.55 * s, 0]),
                     color=BODY_COL, stroke_width=5)
        g.add(arm_l, arm_r)

    return g.move_to(pos)


def make_wall(pos=ORIGIN, height=4.4, width=0.7):
    """A tall solid wall (heavy, immovable)."""
    body = Rectangle(width=width, height=height,
                     fill_color=WALL_COL, fill_opacity=1,
                     stroke_color=WALL_EDGE, stroke_width=2)
    g = VGroup(body)
    # a few brick lines so it reads as a wall
    n = 6
    for k in range(1, n):
        y = -height / 2 + k * height / n
        g.add(Line([-width / 2, y, 0], [width / 2, y, 0],
                   color=WALL_EDGE, stroke_width=1).set_opacity(0.5))
    return g.move_to(pos)


def sweat_drop(pos, scale=1.0):
    """A small teardrop-ish blob."""
    d = Circle(radius=0.10 * scale, fill_color=SWEAT_COL, fill_opacity=0.9,
               stroke_width=0)
    tip = Triangle(color=SWEAT_COL, fill_opacity=0.9, stroke_width=0
                   ).scale(0.10 * scale).next_to(d, UP, buff=-0.05 * scale)
    return VGroup(tip, d).move_to(pos)


def make_cart(pos=ORIGIN, scale=1.0):
    """A small cart: body + two wheels."""
    s = scale
    body = RoundedRectangle(width=1.5 * s, height=0.66 * s,
                            corner_radius=0.10 * s,
                            fill_color=CART_COL, fill_opacity=1,
                            stroke_color=CART_DARK, stroke_width=2)
    body.shift(UP * 0.30 * s)
    w1 = Circle(radius=0.20 * s, fill_color=CART_DARK, fill_opacity=1,
                stroke_color=BODY_COL, stroke_width=2)
    w1.move_to(body.get_corner(DL) + RIGHT * 0.32 * s + DOWN * 0.06 * s)
    w2 = Circle(radius=0.20 * s, fill_color=CART_DARK, fill_opacity=1,
                stroke_color=BODY_COL, stroke_width=2)
    w2.move_to(body.get_corner(DR) + LEFT * 0.32 * s + DOWN * 0.06 * s)
    return VGroup(body, w1, w2).move_to(pos)


def force_arrow(start, length=1.4, direction=RIGHT, color=FORCE_COL,
                label="F", label_color=None, width=7):
    """A bold force arrow with an italic label above it."""
    s = np.array(start, dtype=float)
    d = np.array(direction, dtype=float)
    d = d / (np.linalg.norm(d) + 1e-9)
    e = s + d * length
    a = Arrow(s, e, color=color, stroke_width=width, buff=0,
              max_tip_length_to_length_ratio=0.30, tip_length=0.30)
    g = VGroup(a)
    if label:
        lc = label_color if label_color else color
        t = Text(label, font="sans", font_size=30, color=lc, slant=ITALIC)
        t.next_to(a, UP, buff=0.12)
        g.add(t)
    return g


def displacement_arrow(start, length=2.4, direction=RIGHT, color=DISP_COL,
                       label="d", width=5):
    """A thinner displacement arrow with label below."""
    s = np.array(start, dtype=float)
    d = np.array(direction, dtype=float)
    d = d / (np.linalg.norm(d) + 1e-9)
    e = s + d * length
    a = Arrow(s, e, color=color, stroke_width=width, buff=0,
              max_tip_length_to_length_ratio=0.20, tip_length=0.24)
    g = VGroup(a)
    if label:
        t = Text(label, font="sans", font_size=28, color=color,
                 slant=ITALIC)
        t.next_to(a, DOWN, buff=0.12)
        g.add(t)
    return g


def work_region(corner, w=3.0, h=1.1, color=WORK_COL, label="W = F · d"):
    """A shaded rectangle representing force x distance, anchored at its
    bottom-left `corner`. Returns (rect, label_text)."""
    rect = Rectangle(width=w, height=h, fill_color=color, fill_opacity=0.32,
                     stroke_color=color, stroke_width=2)
    rect.move_to(np.array(corner, dtype=float) + np.array([w / 2, h / 2, 0]))
    lbl = Text(label, font="sans", font_size=28, color=color)
    lbl.move_to(rect.get_center())
    return rect, lbl


class EnergyBar(VGroup):
    """A vertical bar that represents energy of motion. `set_level(f)`
    sets the fill fraction 0..1. Color can be swapped (e.g. to red while
    draining)."""

    def __init__(self, pos=ORIGIN, height=3.0, width=0.7,
                 color=ENERGY_COL, label="energy of motion", **kw):
        super().__init__(**kw)
        self.bar_h = height
        self.bar_w = width
        self.fill_col = color
        self.frame = Rectangle(width=width, height=height,
                               stroke_color=FAINT, stroke_width=2,
                               fill_opacity=0)
        self.fill = Rectangle(width=width, height=0.001,
                              fill_color=color, fill_opacity=0.85,
                              stroke_width=0)
        self._seat()
        self.caption = Text(label, font="sans", font_size=24,
                            color=FAINT)
        self.caption.next_to(self.frame, DOWN, buff=0.22)
        self.add(self.frame, self.fill, self.caption)
        self.move_to(pos)
        self._origin = pos

    def _seat(self):
        self.fill.align_to(self.frame, DOWN)
        self.fill.move_to([self.frame.get_center()[0],
                           self.frame.get_bottom()[1]
                           + self.fill.height / 2, 0])

    def set_level(self, frac):
        frac = float(np.clip(frac, 0.0, 1.0))
        h = max(0.001, frac * self.bar_h)
        new = Rectangle(width=self.bar_w, height=h,
                        fill_color=self.fill_col, fill_opacity=0.85,
                        stroke_width=0)
        new.move_to([self.frame.get_center()[0],
                     self.frame.get_bottom()[1] + h / 2, 0])
        self.fill.become(new)
        return self

    def set_color_to(self, color):
        self.fill_col = color
        self.fill.set_fill(color, opacity=0.85)
        return self


def small_label(text, pos, color=LABEL_COL, size=26, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def big_label(text, pos, color=LABEL_COL, size=40, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def zero_tag(pos, size=64, color=NEG_COL):
    return Text("0", font="sans", font_size=size, color=color).move_to(pos)
