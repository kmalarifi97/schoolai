"""Helpers for the Impulse–Momentum Theorem (impulse) scene.

Primitives the 12 beats need:
  - make_car(crumple=True/False): a simple side-view car; the crumple
    variant has a long deformable nose, the rigid variant a short stiff
    nose. crumple_car(...) returns a deformed copy.
  - make_wall(): the rigid barrier.
  - make_driver(): a tiny stick figure that sits in a car.
  - momentum_bar(value): a horizontal filled bar standing for p (how
    much motion there is to stop).
  - force_time_graph(kind): force-vs-time axes with a shaded area.
    "wide"  -> low and wide   (long time, small force)
    "narrow"-> tall and narrow (short time, big force)
    Both shaded areas are tuned to be equal — the visual point of impulse.
  - icon_airbag / icon_knees / icon_boxer: simple iconic figures.
  - small_label / big_label: text helpers, font="sans".

Pure #000000 void. font="sans" for every Text.
"""

from manim import *
import numpy as np

VOID = "#000000"

CAR_BODY   = "#C9A24B"   # warm brass
CAR_DARK   = "#7C6020"
CRUMPLE    = "#8C5A2A"   # crumple-zone amber
WALL_COL   = "#9AA0A6"
WALL_DARK  = "#5C6166"
WHEEL_COL  = "#3A3A3E"
P_COLOR    = "#7FB8E8"   # momentum blue
F_COLOR    = "#E8835A"   # force amber-red
AREA_COL   = "#E8C25A"   # impulse shaded area
AXIS_COL   = "#8C98A6"
LABEL_COL  = "#EAE4D5"
GREEN_OK   = "#7FB890"
RED_NOT    = "#C96A5A"


# ----------------------------------------------------------------------
# Cars
# ----------------------------------------------------------------------
def _wheels(body_w, y_bottom, scale):
    r = 0.16 * scale
    w1 = VGroup(
        Circle(radius=r, fill_color=WHEEL_COL, fill_opacity=1,
               stroke_color="#1E1E20", stroke_width=2),
        Circle(radius=r * 0.42, fill_color="#6A6A70", fill_opacity=1,
               stroke_width=0),
    ).move_to([-body_w * 0.30, y_bottom, 0])
    w2 = w1.copy().move_to([body_w * 0.30, y_bottom, 0])
    return VGroup(w1, w2)


def make_car(crumple=True, scale=1.0, color=CAR_BODY):
    """Side-view car facing RIGHT (toward the wall).

    crumple=True  -> long soft nose (the crumple zone), drawn distinct.
    crumple=False -> short rigid nose, stiff.
    Origin at car center; nose tip is the rightmost point.
    """
    s = scale
    cabin_w = 1.5 * s
    cabin_h = 0.62 * s
    base_h  = 0.42 * s
    nose_w  = (1.05 if crumple else 0.42) * s

    # lower body slab
    body = RoundedRectangle(
        width=cabin_w + nose_w, height=base_h, corner_radius=0.06 * s,
        fill_color=color, fill_opacity=1,
        stroke_color=CAR_DARK, stroke_width=2,
    )
    body.move_to([0, 0, 0])
    body.shift(LEFT * (nose_w * 0.5))  # body sits left of nose

    # cabin
    cabin = Polygon(
        [-cabin_w * 0.42, base_h * 0.5, 0],
        [-cabin_w * 0.18, base_h * 0.5 + cabin_h, 0],
        [ cabin_w * 0.20, base_h * 0.5 + cabin_h, 0],
        [ cabin_w * 0.40, base_h * 0.5, 0],
        fill_color=color, fill_opacity=1,
        stroke_color=CAR_DARK, stroke_width=2,
    ).shift(LEFT * (nose_w * 0.5))
    win = Polygon(
        [-cabin_w * 0.30, base_h * 0.5 + 0.05 * s, 0],
        [-cabin_w * 0.15, base_h * 0.5 + cabin_h - 0.07 * s, 0],
        [ cabin_w * 0.15, base_h * 0.5 + cabin_h - 0.07 * s, 0],
        [ cabin_w * 0.27, base_h * 0.5 + 0.05 * s, 0],
        fill_color="#11161B", fill_opacity=1, stroke_width=0,
    ).shift(LEFT * (nose_w * 0.5))

    # nose / crumple zone — distinct color + accordion lines if crumple
    nose_left = body.get_right()[0] - 0.001
    nose = Rectangle(
        width=nose_w, height=base_h * 0.92,
        fill_color=(CRUMPLE if crumple else WALL_DARK), fill_opacity=1,
        stroke_color=CAR_DARK, stroke_width=2,
    )
    nose.move_to([nose_left + nose_w * 0.5, 0, 0])
    extra = VGroup()
    if crumple:
        for k in range(1, 4):
            x = nose_left + nose_w * (k / 4.0)
            extra.add(Line([x, -base_h * 0.40, 0], [x, base_h * 0.40, 0],
                            color=CAR_DARK, stroke_width=2).set_opacity(0.7))

    total_w = cabin_w + nose_w
    wheels = _wheels(total_w, -base_h * 0.5 - 0.02 * s, s)
    wheels.shift(LEFT * (nose_w * 0.5))

    car = VGroup(body, nose, extra, cabin, win, wheels)
    car.crumple = crumple
    car.scale_factor = s
    car.nose_ref = nose
    return car


def crumple_car(car, amount=0.55):
    """Return a deformed copy of `car`: the nose squashed inward.
    `amount` 0..1 = fraction of nose width removed (visually compresses)."""
    c = car.copy()
    nose = c[1]
    nw = nose.width
    new_w = max(0.06, nw * (1.0 - amount))
    right_x = nose.get_right()[0]
    nose.stretch_to_fit_width(new_w)
    nose.next_to(c[0].get_right(), RIGHT, buff=0)
    nose.align_to([right_x, 0, 0], RIGHT) if False else None
    # keep accordion lines collapsed against the body
    for ln in c[2]:
        ln.move_to(c[0].get_right() + RIGHT * 0.03)
    return c


def make_driver(scale=1.0, color=LABEL_COL):
    """A tiny stick figure (sits in / stands by a car)."""
    s = scale
    head = Circle(radius=0.12 * s, color=color, fill_opacity=1,
                  stroke_width=0)
    head.move_to([0, 0.55 * s, 0])
    body = Line([0, 0.43 * s, 0], [0, 0.05 * s, 0], color=color,
                stroke_width=4)
    arm = Line([-0.16 * s, 0.34 * s, 0], [0.16 * s, 0.34 * s, 0],
               color=color, stroke_width=4)
    leg1 = Line([0, 0.05 * s, 0], [-0.14 * s, -0.30 * s, 0],
                color=color, stroke_width=4)
    leg2 = Line([0, 0.05 * s, 0], [0.14 * s, -0.30 * s, 0],
                color=color, stroke_width=4)
    return VGroup(head, body, arm, leg1, leg2)


def make_wall(height=4.0, x=0.0):
    """A rigid vertical barrier with hatching, left face at x."""
    w = 0.42
    slab = Rectangle(width=w, height=height, fill_color=WALL_COL,
                     fill_opacity=1, stroke_color=WALL_DARK,
                     stroke_width=2)
    slab.move_to([x + w * 0.5, 0, 0])
    hatch = VGroup()
    n = int(height / 0.34)
    for k in range(n + 1):
        y0 = -height / 2 + k * 0.34
        hatch.add(Line([x + w, y0, 0], [x + w + 0.22, y0 + 0.22, 0],
                        color=WALL_DARK, stroke_width=2).set_opacity(0.7))
    return VGroup(slab, hatch)


# ----------------------------------------------------------------------
# Momentum bar
# ----------------------------------------------------------------------
def momentum_bar(value=1.0, max_value=1.0, length=3.4, height=0.5,
                 color=P_COLOR, label="p", show_label=True):
    """Horizontal bar standing for momentum. value/max_value sets fill."""
    frame = Rectangle(width=length, height=height, stroke_color=AXIS_COL,
                       stroke_width=2, fill_opacity=0)
    frac = float(np.clip(value / max_value, 0.0, 1.0))
    fill = Rectangle(width=max(0.001, length * frac), height=height,
                     fill_color=color, fill_opacity=0.85, stroke_width=0)
    fill.align_to(frame, LEFT)
    g = VGroup(frame, fill)
    if show_label:
        lab = Text(label, font="sans", font_size=34, color=LABEL_COL,
                   slant=ITALIC).next_to(frame, UP, buff=0.18)
        g.add(lab)
    g.bar_frame = frame
    g.bar_fill = fill
    return g


# ----------------------------------------------------------------------
# Force-vs-time graphs (equal shaded areas)
# ----------------------------------------------------------------------
def force_time_graph(kind="wide", width=4.2, height=2.8,
                     title=None, color=F_COLOR):
    """Force-vs-time axes with a shaded impulse area.

    "wide"   : low plateau over a long time.
    "narrow" : tall spike over a short time.
    The shaded-area integrals are tuned ~equal (the whole point).
    Returns a VGroup; .area is the shaded polygon, .axes the axes group.
    """
    ax_o = np.array([-width / 2, -height / 2, 0])
    x_axis = Arrow(ax_o, ax_o + np.array([width, 0, 0]), buff=0,
                   color=AXIS_COL, stroke_width=3,
                   max_tip_length_to_length_ratio=0.04)
    y_axis = Arrow(ax_o, ax_o + np.array([0, height, 0]), buff=0,
                   color=AXIS_COL, stroke_width=3,
                   max_tip_length_to_length_ratio=0.05)
    t_lbl = Text("time", font="sans", font_size=22, color=AXIS_COL
                 ).next_to([ax_o[0] + width, ax_o[1], 0], DOWN, buff=0.16)
    f_lbl = Text("force", font="sans", font_size=22, color=AXIS_COL
                 ).next_to([ax_o[0], ax_o[1] + height, 0], UP,
                           buff=0.12).shift(RIGHT * 0.1)

    # Equal areas: wide -> w=0.78*W, h=0.32*H ; narrow -> w=0.30*W, h=0.83*H
    # area_wide  = 0.78*0.32 = 0.2496 ; area_narrow = 0.30*0.83 = 0.249
    if kind == "wide":
        bw, bh = 0.78 * width, 0.32 * height
        rise = 0.10 * width      # gentle ramp up/down
    else:
        bw, bh = 0.30 * width, 0.83 * height
        rise = 0.05 * width

    x0 = ax_o[0] + 0.10 * width
    pts = [
        [x0, ax_o[1], 0],
        [x0 + rise, ax_o[1] + bh, 0],
        [x0 + bw - rise, ax_o[1] + bh, 0],
        [x0 + bw, ax_o[1], 0],
    ]
    area = Polygon(*pts, fill_color=AREA_COL, fill_opacity=0.45,
                   stroke_color=AREA_COL, stroke_width=3)
    curve_top = VMobject(color=F_COLOR, stroke_width=4)
    curve_top.set_points_as_corners(pts[1:3])

    g = VGroup(x_axis, y_axis, t_lbl, f_lbl, area, curve_top)
    if title:
        ttl = Text(title, font="sans", font_size=24, color=LABEL_COL
                   ).next_to([ax_o[0] + width / 2, ax_o[1] + height, 0],
                             UP, buff=0.10)
        g.add(ttl)
    g.area = area
    g.axes_origin = ax_o
    g.box_w = bw
    g.box_h = bh
    return g


# ----------------------------------------------------------------------
# Icons (airbag / knees / boxer)
# ----------------------------------------------------------------------
def icon_airbag(scale=1.0):
    s = scale
    head = Circle(radius=0.16 * s, color=LABEL_COL, fill_opacity=1,
                  stroke_width=0).move_to([0, 0.55 * s, 0])
    torso = Line([0, 0.40 * s, 0], [0, -0.10 * s, 0], color=LABEL_COL,
                 stroke_width=5)
    bag = Circle(radius=0.34 * s, fill_color="#E8E2D0", fill_opacity=0.9,
                 stroke_color="#B8B2A0", stroke_width=2)
    bag.move_to([0.42 * s, 0.18 * s, 0])
    return VGroup(bag, torso, head)


def icon_knees(scale=1.0):
    s = scale
    head = Circle(radius=0.14 * s, color=LABEL_COL, fill_opacity=1,
                  stroke_width=0).move_to([0, 0.62 * s, 0])
    spine = Line([0, 0.48 * s, 0], [0, 0.10 * s, 0], color=LABEL_COL,
                 stroke_width=5)
    thigh = Line([0, 0.10 * s, 0], [0.26 * s, -0.10 * s, 0],
                 color=LABEL_COL, stroke_width=5)
    shin = Line([0.26 * s, -0.10 * s, 0], [0.10 * s, -0.46 * s, 0],
                color=LABEL_COL, stroke_width=5)
    arc = Arc(radius=0.20 * s, start_angle=-PI / 2, angle=PI / 2,
              color=GREEN_OK, stroke_width=3
              ).move_to([0.20 * s, -0.06 * s, 0])
    return VGroup(spine, thigh, shin, arc, head)


def icon_boxer(scale=1.0):
    s = scale
    head = Circle(radius=0.15 * s, color=LABEL_COL, fill_opacity=1,
                  stroke_width=0).move_to([-0.10 * s, 0.55 * s, 0])
    torso = Line([-0.10 * s, 0.42 * s, 0], [0.10 * s, -0.05 * s, 0],
                 color=LABEL_COL, stroke_width=5)
    arm = Line([0.0 * s, 0.30 * s, 0], [0.34 * s, 0.40 * s, 0],
               color=LABEL_COL, stroke_width=5)
    glove = Circle(radius=0.12 * s, fill_color=RED_NOT, fill_opacity=1,
                   stroke_width=0).move_to([0.40 * s, 0.42 * s, 0])
    leg1 = Line([0.10 * s, -0.05 * s, 0], [-0.10 * s, -0.46 * s, 0],
                color=LABEL_COL, stroke_width=5)
    leg2 = Line([0.10 * s, -0.05 * s, 0], [0.32 * s, -0.42 * s, 0],
                color=LABEL_COL, stroke_width=5)
    # lean-back arc cue
    sway = Arc(radius=0.30 * s, start_angle=PI * 0.55, angle=-PI * 0.5,
               color=GREEN_OK, stroke_width=3).move_to([-0.05 * s, 0.20 * s, 0])
    return VGroup(torso, arm, glove, leg1, leg2, sway, head)


# ----------------------------------------------------------------------
# Text helpers
# ----------------------------------------------------------------------
def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def big_label(text, pos, color=LABEL_COL, size=44):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos)
