"""Helpers for the Conservation of Momentum (momentumcons) scene.

Primitives for a kitchen-table-warm explainer:
  - top-down figure standing/sliding on a frozen lake
  - a thrown bag
  - signed momentum bars (forward = +, backward = −)
  - a two-pan balance
  - a dashed isolated-system boundary
  - a rocket with exhaust
  - two colliding carts
  - momentum tokens (currency that moves but is never spent)

Pure #000000 void. font="sans" for all text.
"""

from manim import *
import numpy as np

VOID = "#000000"

ICE_COL    = "#3A4A5A"   # faint frozen-lake outline
FIG_COL    = "#EAE4D5"   # the person (warm off-white)
BAG_COL    = "#C98A4A"   # the heavy bag (warm tan)
PLUS_COL   = "#7FB8E8"   # forward / positive momentum (cool blue)
MINUS_COL  = "#E8A07F"   # backward / negative momentum (warm orange)
NEUTRAL    = "#8C98A6"   # boundaries, labels
LABEL_COL  = "#EAE4D5"
ROCKET_COL = "#D8D2C3"
EXHAUST_COL = "#E8A07F"
CART_A_COL = "#7FB8E8"
CART_B_COL = "#C98A4A"
TOKEN_COL  = "#EAD58C"   # momentum-currency token (warm gold)


# ---------------------------------------------------------------- text
def label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


# ---------------------------------------------------------------- ice
def frozen_lake(center=(0, 0, 0), w=12.0, h=6.6):
    """A faint rounded rectangle suggesting a frictionless frozen lake
    seen from directly above."""
    rect = RoundedRectangle(width=w, height=h, corner_radius=0.5,
                            stroke_color=ICE_COL, stroke_width=2,
                            fill_color=ICE_COL, fill_opacity=0.05)
    rect.move_to(center)
    # a couple of faint surface cracks
    c1 = Line([-w * 0.30, h * 0.18, 0], [-w * 0.05, -h * 0.10, 0],
              color=ICE_COL, stroke_width=1).set_opacity(0.35)
    c2 = Line([w * 0.10, h * 0.22, 0], [w * 0.32, -h * 0.05, 0],
              color=ICE_COL, stroke_width=1).set_opacity(0.30)
    g = VGroup(rect, c1, c2)
    g.move_to(center)
    return g


# ---------------------------------------------------------------- figure
def make_figure(pos=(0, 0, 0), scale=1.0, color=FIG_COL):
    """A simple top-down person: a head circle with two shoulder arcs.
    Reads clearly from directly above."""
    pos = np.array(pos, dtype=float)
    head = Circle(radius=0.30 * scale, fill_color=color, fill_opacity=1,
                  stroke_color=color, stroke_width=2)
    head.move_to([0, 0.18 * scale, 0])
    # body / shoulders as a filled rounded torso seen from above
    torso = Ellipse(width=0.86 * scale, height=0.52 * scale,
                    fill_color=color, fill_opacity=0.9,
                    stroke_color=color, stroke_width=2)
    torso.move_to([0, -0.18 * scale, 0])
    g = VGroup(torso, head)
    g.move_to(pos)
    return g


def make_bag(pos=(0, 0, 0), scale=1.0, color=BAG_COL):
    """A heavy bag (rounded square with a small handle), top-down."""
    pos = np.array(pos, dtype=float)
    body = RoundedRectangle(width=0.62 * scale, height=0.50 * scale,
                            corner_radius=0.10 * scale,
                            fill_color=color, fill_opacity=1,
                            stroke_color=color, stroke_width=2)
    handle = Arc(radius=0.16 * scale, start_angle=0, angle=PI,
                 color=color, stroke_width=5)
    handle.next_to(body, UP, buff=-0.04 * scale)
    g = VGroup(body, handle)
    g.move_to(pos)
    return g


# ---------------------------------------------------------------- bars
def momentum_bar(magnitude, direction=+1, origin=(0, 0, 0),
                 unit=1.4, color=None, height=0.46, label_text=None,
                 label_size=22):
    """A signed momentum bar. direction=+1 grows RIGHT (forward, plus,
    blue), direction=-1 grows LEFT (backward, minus, orange). `origin`
    is the bar's base (the zero line)."""
    if color is None:
        color = PLUS_COL if direction >= 0 else MINUS_COL
    origin = np.array(origin, dtype=float)
    length = max(0.001, magnitude * unit)
    if direction >= 0:
        rect = Rectangle(width=length, height=height,
                         fill_color=color, fill_opacity=0.9,
                         stroke_color=color, stroke_width=2)
        rect.move_to(origin + np.array([length / 2.0, 0, 0]))
    else:
        rect = Rectangle(width=length, height=height,
                         fill_color=color, fill_opacity=0.9,
                         stroke_color=color, stroke_width=2)
        rect.move_to(origin + np.array([-length / 2.0, 0, 0]))
    g = VGroup(rect)
    if label_text is not None:
        off = 0.42 if direction >= 0 else -0.42
        lbl = Text(label_text, font="sans", font_size=label_size,
                   color=color).move_to(origin + np.array(
                       [direction * (length + 0.0) + off, 0, 0]))
        # place label centered over the bar instead
        lbl.move_to(rect.get_center() + np.array([0, height / 2 + 0.30, 0]))
        g.add(lbl)
    return g


def sign_tag(text, pos, color, size=34):
    """A '+' or '−' tag."""
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(np.array(pos, dtype=float))


def zero_line(center=(0, 0, 0), height=3.4, color=NEUTRAL):
    """The vertical zero axis the signed bars are measured from."""
    center = np.array(center, dtype=float)
    ln = DashedLine(center + np.array([0, height / 2, 0]),
                    center + np.array([0, -height / 2, 0]),
                    color=color, stroke_width=2,
                    dash_length=0.12).set_opacity(0.55)
    z = Text("0", font="sans", font_size=22, color=color
             ).move_to(center + np.array([0, -height / 2 - 0.32, 0])
                       ).set_opacity(0.7)
    return VGroup(ln, z)


# ---------------------------------------------------------------- balance
def make_balance(center=(0, 0, 0), span=4.0, color=NEUTRAL):
    """A simple two-pan balance: a central fulcrum, a beam, two pans
    hanging level. Returns a VGroup; pans are .left_pan / .right_pan
    accessible by index: [0]=fulcrum,[1]=beam,[2]=left_pan,[3]=right_pan."""
    center = np.array(center, dtype=float)
    half = span / 2.0
    fulcrum = Triangle(color=color, fill_color=color, fill_opacity=0.6,
                       stroke_width=2).scale(0.34)
    fulcrum.move_to(center + np.array([0, -0.05, 0]))
    beam = Line(center + np.array([-half, 0.55, 0]),
                center + np.array([half, 0.55, 0]),
                color=color, stroke_width=4)
    post = Line(center + np.array([0, 0.55, 0]),
                center + np.array([0, 0.10, 0]),
                color=color, stroke_width=3)

    def pan(cx):
        cord_l = Line(center + np.array([cx - 0.5, 0.55, 0]),
                      center + np.array([cx - 0.35, -0.10, 0]),
                      color=color, stroke_width=1.5).set_opacity(0.7)
        cord_r = Line(center + np.array([cx + 0.5, 0.55, 0]),
                      center + np.array([cx + 0.35, -0.10, 0]),
                      color=color, stroke_width=1.5).set_opacity(0.7)
        dish = Arc(radius=0.55, start_angle=PI, angle=PI,
                   color=color, stroke_width=3)
        dish.move_to(center + np.array([cx, -0.22, 0]))
        return VGroup(cord_l, cord_r, dish)

    left_pan = pan(-half)
    right_pan = pan(half)
    g = VGroup(fulcrum, beam, post, left_pan, right_pan)
    return g


# ---------------------------------------------------------------- boundary
def isolated_boundary(center=(0, 0, 0), w=6.0, h=4.0, color=NEUTRAL,
                      with_label=True):
    """A dashed rounded rectangle marking an isolated system."""
    center = np.array(center, dtype=float)
    box = RoundedRectangle(width=w, height=h, corner_radius=0.4,
                           stroke_color=color, stroke_width=2.5,
                           fill_opacity=0)
    box.move_to(center)
    box = DashedVMobject(box, num_dashes=54).set_opacity(0.7)
    g = VGroup(box)
    if with_label:
        lbl = Text("isolated system", font="sans", font_size=24,
                   color=color).move_to(
                       center + np.array([0, h / 2 + 0.40, 0])
                   ).set_opacity(0.85)
        g.add(lbl)
    return g


# ---------------------------------------------------------------- rocket
def make_rocket(pos=(0, 0, 0), scale=1.0, color=ROCKET_COL):
    """A simple upright rocket: body + nose cone + two fins."""
    pos = np.array(pos, dtype=float)
    body = RoundedRectangle(width=0.6 * scale, height=1.5 * scale,
                            corner_radius=0.12 * scale,
                            fill_color=color, fill_opacity=1,
                            stroke_color=color, stroke_width=2)
    nose = Triangle(color=color, fill_color=color, fill_opacity=1,
                    stroke_width=2).scale(0.42 * scale)
    nose.next_to(body, UP, buff=-0.06 * scale)
    fin_l = Polygon([-0.30 * scale, -0.75 * scale, 0],
                    [-0.62 * scale, -1.05 * scale, 0],
                    [-0.30 * scale, -0.35 * scale, 0],
                    color=color, fill_color=color, fill_opacity=1,
                    stroke_width=1)
    fin_r = Polygon([0.30 * scale, -0.75 * scale, 0],
                    [0.62 * scale, -1.05 * scale, 0],
                    [0.30 * scale, -0.35 * scale, 0],
                    color=color, fill_color=color, fill_opacity=1,
                    stroke_width=1)
    g = VGroup(body, nose, fin_l, fin_r)
    g.move_to(pos)
    return g


def exhaust_plume(top=(0, 0, 0), scale=1.0, color=EXHAUST_COL):
    """A downward exhaust plume — a few translucent flame triangles."""
    top = np.array(top, dtype=float)
    # billowing exhaust: a wide soft cloud of overlapping puffs below
    g = VGroup()
    puffs = [
        (0.0, -0.30, 0.34, 0.55),
        (-0.30, -0.55, 0.30, 0.45),
        (0.30, -0.55, 0.30, 0.45),
        (0.0, -0.78, 0.40, 0.40),
        (-0.45, -0.95, 0.26, 0.32),
        (0.45, -0.95, 0.26, 0.32),
        (0.0, -1.10, 0.30, 0.28),
    ]
    for dx, dy, r, op in puffs:
        c = Circle(radius=r * scale, fill_color=color, fill_opacity=op,
                   stroke_width=0)
        c.move_to([dx * scale, dy * scale, 0])
        g.add(c)
    # hot core
    core = Circle(radius=0.22 * scale, fill_color="#EAD58C",
                  fill_opacity=0.85, stroke_width=0)
    core.move_to([0, -0.34 * scale, 0])
    g.add(core)
    g.move_to(top + np.array([0, -0.55 * scale, 0]))
    return g


# ---------------------------------------------------------------- carts
def make_cart(pos=(0, 0, 0), scale=1.0, color=CART_A_COL):
    """A small cart: rounded box body + two wheels."""
    pos = np.array(pos, dtype=float)
    body = RoundedRectangle(width=1.05 * scale, height=0.55 * scale,
                            corner_radius=0.08 * scale,
                            fill_color=color, fill_opacity=1,
                            stroke_color=color, stroke_width=2)
    w1 = Circle(radius=0.15 * scale, fill_color=NEUTRAL, fill_opacity=1,
                stroke_width=0)
    w2 = Circle(radius=0.15 * scale, fill_color=NEUTRAL, fill_opacity=1,
                stroke_width=0)
    w1.move_to([-0.30 * scale, -0.32 * scale, 0])
    w2.move_to([0.30 * scale, -0.32 * scale, 0])
    g = VGroup(body, w1, w2)
    g.move_to(pos)
    return g


# ---------------------------------------------------------------- token
def momentum_token(pos=(0, 0, 0), scale=1.0, color=TOKEN_COL):
    """A momentum 'currency' token: a small coin with a 'p' on it."""
    pos = np.array(pos, dtype=float)
    coin = Circle(radius=0.26 * scale, fill_color=color, fill_opacity=1,
                  stroke_color="#B89A4A", stroke_width=2)
    rim = Circle(radius=0.20 * scale, color="#B89A4A", stroke_width=1.4,
                 fill_opacity=0).set_opacity(0.7)
    p = Text("p", font="sans", font_size=int(22 * scale), color="#5A4A1A",
             slant=ITALIC)
    g = VGroup(coin, rim, p)
    g.move_to(pos)
    return g


def arrow_between(start, end, color=PLUS_COL, width=5):
    """A straight momentum arrow."""
    return Arrow(np.array(start, dtype=float), np.array(end, dtype=float),
                 color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.28)
