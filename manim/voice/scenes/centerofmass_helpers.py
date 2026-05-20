"""Helpers for the Center of Mass & Stability (centerofmass) scene.

Pure #000000 void. font="sans" for all text. Primitives:
  make_wrench        - a stylized open/box-end wrench, rotatable
  com_dot            - the marked center-of-mass point (filled + ring)
  parabola_path      - a smooth arc the com_dot can travel along
  make_L_shape       - an L-shaped metal piece (com falls in the notch)
  make_block         - a rectangular block with a marked base + com
  plumb_line         - a vertical dashed line from the com downward
  base_bracket       - a bracket spanning the base of support
  wide_shape / tall_shape - low-wide vs tall-narrow stability contrast
  make_figure        - a simple person; carry_load adds a bag in hand
  small_label / com_label
"""

from manim import *
import numpy as np

VOID = "#000000"

METAL      = "#C9CCD4"
METAL_DARK = "#6B6E78"
METAL_EDGE = "#8A8D96"
COM_COL    = "#E8B04A"   # warm amber for the center-of-mass marker
PATH_COL   = "#7FB8E8"   # cool blue for the traced arc
BASE_COL   = "#7FB8E8"
DIM_COL    = "#4A4D55"
LABEL_COL  = "#EAE4D5"
SKIN       = "#D8C2A8"
BODY_COL   = "#B8B8BE"
LOAD_COL   = "#C98A4A"


# ---------------------------------------------------------------- wrench
def make_wrench(scale=1.0, color=METAL):
    """A stylized combination wrench lying horizontally, centered at origin.

    Built from a shaft plus an open-end jaw (left) and a ring box-end
    (right). Returned as a VGroup so it can be rotated as one rigid body.
    """
    shaft = RoundedRectangle(
        width=2.6, height=0.34, corner_radius=0.14,
        fill_color=color, fill_opacity=1,
        stroke_color=METAL_EDGE, stroke_width=1.5,
    )
    # open-end jaw on the left
    head_l = RoundedRectangle(
        width=0.72, height=0.92, corner_radius=0.12,
        fill_color=color, fill_opacity=1,
        stroke_color=METAL_EDGE, stroke_width=1.5,
    ).move_to(shaft.get_left() + LEFT * 0.30)
    notch = Polygon(
        head_l.get_center() + np.array([-0.40, 0.46, 0]),
        head_l.get_center() + np.array([0.05, 0.12, 0]),
        head_l.get_center() + np.array([0.05, -0.12, 0]),
        head_l.get_center() + np.array([-0.40, -0.46, 0]),
        fill_color=VOID, fill_opacity=1, stroke_width=0,
    )
    # box-end ring on the right
    ring_o = Circle(radius=0.52, fill_color=color, fill_opacity=1,
                    stroke_color=METAL_EDGE, stroke_width=1.5
                    ).move_to(shaft.get_right() + RIGHT * 0.34)
    ring_i = Circle(radius=0.26, fill_color=VOID, fill_opacity=1,
                    stroke_width=0).move_to(ring_o.get_center())
    w = VGroup(shaft, head_l, notch, ring_o, ring_i)
    w.scale(scale)
    return w


# ----------------------------------------------------------- com marker
def com_dot(point, scale=1.0, color=COM_COL):
    """Marked center-of-mass point: filled core + thin surrounding ring."""
    core = Dot(point=np.array(point, dtype=float), radius=0.10 * scale,
               color=color)
    ring = Circle(radius=0.20 * scale, stroke_color=color,
                  stroke_width=2.4, fill_opacity=0
                  ).move_to(np.array(point, dtype=float))
    return VGroup(core, ring)


def com_crosshair(point, scale=1.0, color=COM_COL):
    """The classic com symbol: a circle quartered with alternating fill feel."""
    p = np.array(point, dtype=float)
    ring = Circle(radius=0.22 * scale, stroke_color=color,
                  stroke_width=2.6, fill_opacity=0).move_to(p)
    h = Line(p + LEFT * 0.22 * scale, p + RIGHT * 0.22 * scale,
             color=color, stroke_width=2.0)
    v = Line(p + DOWN * 0.22 * scale, p + UP * 0.22 * scale,
             color=color, stroke_width=2.0)
    return VGroup(ring, h, v)


def parabola_path(start, end, height, color=PATH_COL, width=3.0):
    """A smooth downward-opening arc from start to end peaking `height`
    above the chord midpoint. Returns a VMobject curve."""
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    pts = []
    for t in np.linspace(0, 1, 60):
        x = s[0] + (e[0] - s[0]) * t
        y = s[1] + (e[1] - s[1]) * t
        y += 4 * height * t * (1 - t)
        pts.append([x, y, 0])
    c = VMobject(stroke_color=color, stroke_width=width)
    c.set_points_smoothly([np.array(p) for p in pts])
    return c


def point_on_parabola(start, end, height, t):
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    x = s[0] + (e[0] - s[0]) * t
    y = s[1] + (e[1] - s[1]) * t + 4 * height * t * (1 - t)
    return np.array([x, y, 0])


# ----------------------------------------------------------- L-shape
def make_L_shape(scale=1.0, color=METAL, center=ORIGIN):
    """An L-shaped metal piece. Its true centroid lies OUTSIDE the
    metal, inside the empty notch. Returns (shape, com_point)."""
    # L occupying: vertical arm + horizontal foot
    a = 1.0 * scale          # thickness
    L = 2.4 * scale          # leg length
    pts = [
        [0, 0, 0],
        [L, 0, 0],
        [L, a, 0],
        [a, a, 0],
        [a, L, 0],
        [0, L, 0],
    ]
    poly = Polygon(*[np.array(p) for p in pts],
                   fill_color=color, fill_opacity=1,
                   stroke_color=METAL_EDGE, stroke_width=2.0)
    # centroid of an L = composite of two rectangles
    # rect A: horizontal foot  L x a   centroid (L/2, a/2)
    # rect B: vertical arm  a x (L-a)  centroid (a/2, a+(L-a)/2)
    Aa = L * a
    Ab = a * (L - a)
    cx = (Aa * (L / 2) + Ab * (a / 2)) / (Aa + Ab)
    cy = (Aa * (a / 2) + Ab * (a + (L - a) / 2)) / (Aa + Ab)
    grp = VGroup(poly)
    shift = np.array(center, dtype=float) - poly.get_center()
    grp.shift(shift)
    com_pt = np.array([cx, cy, 0]) + shift
    return grp, com_pt


# ----------------------------------------------------------- block
def make_block(width=1.6, height=2.4, color=METAL, center=ORIGIN):
    """A rectangular block. Returns (block, com_point_local_to_center)."""
    blk = Rectangle(width=width, height=height,
                    fill_color=color, fill_opacity=1,
                    stroke_color=METAL_EDGE, stroke_width=2.0)
    blk.move_to(np.array(center, dtype=float))
    return blk


def ground_line(y=-2.4, x_half=6.0, color="#5A5D66"):
    return Line([-x_half, y, 0], [x_half, y, 0],
                color=color, stroke_width=3.0)


def plumb_line(com_point, y_bottom, color=COM_COL, width=2.4):
    """A dashed vertical line straight down from the com to y_bottom."""
    cp = np.array(com_point, dtype=float)
    ln = DashedLine(cp, np.array([cp[0], y_bottom, 0]),
                    color=color, stroke_width=width,
                    dash_length=0.14)
    return ln


def base_bracket(x_left, x_right, y, color=BASE_COL, width=3.0):
    """A bracket spanning [x_left, x_right] at height y marking the
    base of support."""
    span = Line([x_left, y, 0], [x_right, y, 0],
                color=color, stroke_width=width)
    tickL = Line([x_left, y - 0.12, 0], [x_left, y + 0.12, 0],
                 color=color, stroke_width=width)
    tickR = Line([x_right, y - 0.12, 0], [x_right, y + 0.12, 0],
                 color=color, stroke_width=width)
    return VGroup(span, tickL, tickR)


# ------------------------------------------------ wide vs tall shapes
def wide_shape(center=ORIGIN, color=METAL):
    """A low, wide trapezoid-ish block (hard to tip)."""
    body = Polygon(
        np.array([-1.7, -0.55, 0]), np.array([1.7, -0.55, 0]),
        np.array([1.35, 0.55, 0]), np.array([-1.35, 0.55, 0]),
        fill_color=color, fill_opacity=1,
        stroke_color=METAL_EDGE, stroke_width=2.0,
    )
    body.move_to(np.array(center, dtype=float))
    return body


def tall_shape(center=ORIGIN, color=METAL):
    """A tall, narrow block (easy to tip)."""
    body = Rectangle(width=0.85, height=3.0,
                     fill_color=color, fill_opacity=1,
                     stroke_color=METAL_EDGE, stroke_width=2.0)
    body.move_to(np.array(center, dtype=float))
    return body


# ----------------------------------------------------------- figure
def make_figure(center=ORIGIN, scale=1.0, lean=0.0, color=BODY_COL):
    """A simple standing person. `lean` (radians) tilts the torso+head
    backward (negative leans left/back). Returns a VGroup.
    Feet stay planted; body pivots about the hip point."""
    c = np.array(center, dtype=float)
    hip = c + np.array([0, 0.0, 0]) * scale

    # legs (planted)
    legL = Line(hip + np.array([-0.12, 0, 0]) * scale,
                hip + np.array([-0.20, -1.0, 0]) * scale,
                color=color, stroke_width=7)
    legR = Line(hip + np.array([0.12, 0, 0]) * scale,
                hip + np.array([0.20, -1.0, 0]) * scale,
                color=color, stroke_width=7)
    feet = Line(hip + np.array([-0.34, -1.0, 0]) * scale,
                hip + np.array([0.34, -1.0, 0]) * scale,
                color=color, stroke_width=7)

    # torso + head + arms group that leans about the hip
    torso = Line(hip, hip + np.array([0, 1.05, 0]) * scale,
                 color=color, stroke_width=8)
    head = Circle(radius=0.26 * scale, fill_color=color, fill_opacity=1,
                  stroke_width=0).move_to(hip + np.array([0, 1.40, 0]) * scale)
    armL = Line(hip + np.array([0, 0.85, 0]) * scale,
                hip + np.array([0.55, 0.35, 0]) * scale,
                color=color, stroke_width=6)
    armR = Line(hip + np.array([0, 0.85, 0]) * scale,
                hip + np.array([0.62, 0.30, 0]) * scale,
                color=color, stroke_width=6)
    upper = VGroup(torso, head, armL, armR)
    if abs(lean) > 1e-6:
        upper.rotate(lean, about_point=hip)

    fig = VGroup(legL, legR, feet, upper)
    fig.hip = hip
    fig.hand = hip + np.array([0.60, 0.32, 0]) * scale
    if abs(lean) > 1e-6:
        # recompute hand after rotation
        rel = fig.hand - hip
        ca, sa = np.cos(lean), np.sin(lean)
        fig.hand = hip + np.array([ca * rel[0] - sa * rel[1],
                                   sa * rel[0] + ca * rel[1], 0])
    return fig


def make_load(at_point, scale=1.0, color=LOAD_COL):
    """A heavy bag/box held at `at_point`."""
    p = np.array(at_point, dtype=float)
    box = RoundedRectangle(width=0.7 * scale, height=0.85 * scale,
                           corner_radius=0.06,
                           fill_color=color, fill_opacity=1,
                           stroke_color="#8A5A2A", stroke_width=1.6)
    box.move_to(p + np.array([0.18 * scale, -0.45 * scale, 0]))
    return box


# ----------------------------------------------------------- labels
def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(np.array(pos, dtype=float)).set_opacity(opacity)


def com_label(pos, color=COM_COL, size=28):
    return Text("center of mass", font="sans", font_size=size,
                color=color).move_to(np.array(pos, dtype=float))
