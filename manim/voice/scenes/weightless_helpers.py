"""Helpers for the Weightlessness & Free Fall (weightless) scene.

Reuses make_earth from grav_helpers and adds:
- a simple astronaut figure
- a space station
- an elevator box with a person on a bathroom scale
- ballistic-arc / orbit-circle geometry helpers
- a big curved Earth surface (limb) for the cannonball-to-orbit beats
"""

from manim import *
import numpy as np

from grav_helpers import make_earth  # noqa: F401

VOID = "#000000"

SUIT      = "#E8E8EE"
SUIT_DARK = "#9AA0AC"
VISOR     = "#3A6B9A"
METAL     = "#B8BEC8"
METAL_DK  = "#6E7682"
PANEL     = "#2A4E78"
ARC_COL   = "#E8C97F"
ORBIT_COL = "#7FB8E8"
LAND_COL  = "#3A8B6B"
LABEL_COL = "#EAE4D5"
DIM_LABEL = "#8C98A6"


def make_astronaut(pos=ORIGIN, scale=1.0, tilt=0.0):
    """A small, readable spacesuit figure: helmet+visor, torso, limbs."""
    g = VGroup()
    helmet = Circle(radius=0.30, fill_color=SUIT, fill_opacity=1,
                    stroke_color=SUIT_DARK, stroke_width=2)
    visor = (Ellipse(width=0.34, height=0.26, fill_color=VISOR,
                     fill_opacity=1, stroke_color="#22405E", stroke_width=1.5)
             .shift(UP * 0.02))
    vhl = (Ellipse(width=0.12, height=0.08, fill_color=WHITE,
                   fill_opacity=0.35, stroke_width=0)
           .shift(LEFT * 0.07 + UP * 0.07))
    head = VGroup(helmet, visor, vhl).shift(UP * 0.74)

    torso = RoundedRectangle(width=0.52, height=0.62, corner_radius=0.16,
                             fill_color=SUIT, fill_opacity=1,
                             stroke_color=SUIT_DARK, stroke_width=2
                             ).shift(UP * 0.18)
    chest = (RoundedRectangle(width=0.22, height=0.16, corner_radius=0.04,
                              fill_color=SUIT_DARK, fill_opacity=0.8,
                              stroke_width=0).shift(UP * 0.20))

    def limb(a, b, w=0.16):
        return Line(a, b, color=SUIT, stroke_width=w * 100,
                    cap_style=CapStyleType.ROUND)

    arm_l = limb([-0.24, 0.34, 0], [-0.62, 0.04, 0])
    arm_r = limb([0.24, 0.34, 0], [0.60, 0.46, 0])
    leg_l = limb([-0.14, -0.14, 0], [-0.30, -0.78, 0])
    leg_r = limb([0.14, -0.14, 0], [0.34, -0.74, 0])

    g.add(arm_l, arm_r, leg_l, leg_r, torso, chest, head)
    g.scale(scale).rotate(tilt).move_to(pos)
    return g


def make_station(pos=ORIGIN, scale=1.0):
    """A compact space station: core module + two solar panel wings."""
    g = VGroup()
    core = RoundedRectangle(width=1.5, height=0.52, corner_radius=0.14,
                            fill_color=METAL, fill_opacity=1,
                            stroke_color=METAL_DK, stroke_width=2)
    dock = RoundedRectangle(width=0.26, height=0.30, corner_radius=0.05,
                            fill_color=METAL_DK, fill_opacity=1,
                            stroke_width=0).next_to(core, RIGHT, buff=-0.02)
    truss_l = Line([-0.75, 0, 0], [-1.7, 0, 0], color=METAL_DK,
                   stroke_width=4)
    truss_r = Line([0.75, 0, 0], [1.6, 0, 0], color=METAL_DK,
                   stroke_width=4)

    def panel(cx):
        p = VGroup()
        body = Rectangle(width=1.1, height=0.92, fill_color=PANEL,
                         fill_opacity=1, stroke_color="#1A3354",
                         stroke_width=1.5)
        for k in range(1, 4):
            p.add(Line([-0.55 + k * 0.275, -0.46, 0],
                       [-0.55 + k * 0.275, 0.46, 0],
                       color="#1A3354", stroke_width=1.2))
        p.add(body)
        p.add(Line([-0.55, 0, 0], [0.55, 0, 0], color="#1A3354",
                   stroke_width=1.2))
        return p.move_to([cx, 0, 0])

    g.add(truss_l, truss_r, panel(-2.35), panel(2.25), core, dock)
    g.scale(scale).move_to(pos)
    return g


def make_scale(width=0.9):
    """A flat bathroom scale (top face + readout window)."""
    base = RoundedRectangle(width=width, height=0.20, corner_radius=0.04,
                            fill_color="#C8CCD2", fill_opacity=1,
                            stroke_color="#7A7E86", stroke_width=1.5)
    win = RoundedRectangle(width=0.34, height=0.12, corner_radius=0.02,
                           fill_color="#101418", fill_opacity=1,
                           stroke_width=0).move_to(base.get_center())
    return VGroup(base, win)


def make_person(scale=1.0):
    """A simple standing person (for the elevator/scale beats)."""
    g = VGroup()
    head = Circle(radius=0.16, fill_color="#E2C7A0", fill_opacity=1,
                  stroke_color="#B89A78", stroke_width=1.5).shift(UP * 0.92)
    body = RoundedRectangle(width=0.34, height=0.62, corner_radius=0.12,
                            fill_color="#5A7FA8", fill_opacity=1,
                            stroke_color="#3E5C7E", stroke_width=1.5
                            ).shift(UP * 0.42)
    arm_l = Line([-0.17, 0.58, 0], [-0.27, 0.10, 0], color="#5A7FA8",
                 stroke_width=11, cap_style=CapStyleType.ROUND)
    arm_r = Line([0.17, 0.58, 0], [0.27, 0.10, 0], color="#5A7FA8",
                 stroke_width=11, cap_style=CapStyleType.ROUND)
    leg_l = Line([-0.09, 0.12, 0], [-0.11, -0.20, 0], color="#3E5C7E",
                 stroke_width=12, cap_style=CapStyleType.ROUND)
    leg_r = Line([0.09, 0.12, 0], [0.11, -0.20, 0], color="#3E5C7E",
                 stroke_width=12, cap_style=CapStyleType.ROUND)
    g.add(arm_l, arm_r, leg_l, leg_r, body, head)
    g.scale(scale)
    return g


def make_elevator(width=2.4, height=3.2):
    """An open-front elevator car: walls + floor, no front face so the
    person and scale inside read clearly."""
    wall = "#4A5260"
    floor = Line([-width / 2, -height / 2, 0], [width / 2, -height / 2, 0],
                 color="#7A828E", stroke_width=6)
    ceil = Line([-width / 2, height / 2, 0], [width / 2, height / 2, 0],
                color=wall, stroke_width=4)
    left = Line([-width / 2, -height / 2, 0], [-width / 2, height / 2, 0],
                color=wall, stroke_width=4)
    right = Line([width / 2, -height / 2, 0], [width / 2, height / 2, 0],
                 color=wall, stroke_width=4)
    return VGroup(floor, ceil, left, right)


def make_cable(top, attach, broken=False):
    """A vertical cable from `top` down to `attach`."""
    if not broken:
        return Line(top, attach, color="#9AA0AC", stroke_width=4)
    mid = (np.array(top) + np.array(attach)) / 2
    upper = Line(top, mid + np.array([0.05, 0.10, 0]),
                 color="#9AA0AC", stroke_width=4)
    lower = Line(mid + np.array([-0.05, -0.10, 0]), attach,
                 color="#9AA0AC", stroke_width=4)
    return VGroup(upper, lower)


def big_label(text, pos, color=LABEL_COL, size=64, weight=BOLD):
    return Text(text, font="sans", font_size=size, color=color,
                weight=weight).move_to(pos)


def small_label(text, pos, color=DIM_LABEL, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def question_mark(pos, color=LABEL_COL, size=72):
    return Text("?", font="sans", font_size=size, color=color,
                weight=BOLD).move_to(pos)


def earth_limb(center, radius, color="#2A6BB5", fill_op=1.0):
    """A large Earth as a curved surface (the visible ground curving away).
    `center` is far below frame so only the top arc shows."""
    body = Circle(radius=radius, fill_color=color, fill_opacity=fill_op,
                  stroke_color="#1A4885", stroke_width=2).move_to(center)
    return body


def ballistic_arc(launch, vx, g=9.8, t_max=2.0, n=60, color=ARC_COL):
    """A simple parabolic trajectory polyline from `launch` with horizontal
    speed vx (scene units/s) under downward accel g (scene units/s^2)."""
    launch = np.array(launch, dtype=float)
    pts = []
    for k in range(n):
        t = t_max * k / (n - 1)
        x = launch[0] + vx * t
        y = launch[1] - 0.5 * g * t * t
        pts.append(np.array([x, y, 0]))
    line = VMobject(stroke_color=color, stroke_width=4)
    line.set_points_smoothly(pts)
    return line


def curved_fall_arc(center, radius, theta0, theta1, drop, color=ARC_COL):
    """An arc that starts tangent at the limb (angle theta0, measured from
    +x at `center`) and travels to theta1, rising slightly above the
    surface then curving back down toward it — a 'long throw around a
    curved Earth'. `drop` sets the max height above the surface."""
    center = np.array(center, dtype=float)
    pts = []
    n = 70
    for k in range(n):
        s = k / (n - 1)
        th = theta0 + (theta1 - theta0) * s
        # height profile: rises then returns to surface (sin bump)
        h = drop * np.sin(np.pi * s)
        r = radius + h
        pts.append(center + np.array([r * np.cos(th), r * np.sin(th), 0]))
    line = VMobject(stroke_color=color, stroke_width=4)
    line.set_points_smoothly(pts)
    return line


def orbit_circle(center, radius, color=ORBIT_COL, width=3, dashed=False):
    if dashed:
        return DashedVMobject(
            Circle(radius=radius, color=color, stroke_width=width
                   ).move_to(center), num_dashes=64)
    return Circle(radius=radius, color=color, stroke_width=width
                  ).move_to(center)


def point_on_circle(center, radius, theta):
    center = np.array(center, dtype=float)
    return center + np.array([radius * np.cos(theta),
                              radius * np.sin(theta), 0])
