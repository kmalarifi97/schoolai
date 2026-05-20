"""Helpers for the Rotational Kinetic Energy (rotke) scene.

Primitives: a heavy spinning flywheel with a fixed center, a 'speed = 0'
center tag, a hand grabbing the rim with sparks, rim mass elements that
streak around, per-piece speed vectors, mass-near-hub vs mass-at-rim
disks, a moment-of-inertia label, a potter's wheel, and a rolling ball
with forward + spin bars.

Pure #000000 void, font="sans".
"""

from manim import *
import numpy as np

VOID = "#000000"

WHEEL_BODY = "#7FB8E8"
WHEEL_DARK = "#3F5C74"
WHEEL_RIM  = "#A9CCE6"
HUB_COL    = "#EAE4D5"
SPOKE_COL  = "#5E7E96"
SPEED_COL  = "#F0C674"
ENERGY_COL = "#E8A24A"
MASS_COL   = "#E26D5A"
SPARK_COL  = "#FFD27A"
LABEL_COL  = "#EAE4D5"
DIM_COL    = "#8C98A6"
SPIN_COL   = "#9CC4E0"
FWD_COL    = "#7FD6A5"


def make_flywheel(pos=ORIGIN, radius=1.7, n_spokes=6, scale=1.0):
    """A heavy disk: dark filled body, bright rim ring, hub, and spokes.
    Center-symmetric so it reads as spinning when rotated."""
    radius = radius * scale
    body = Circle(radius=radius, fill_color=WHEEL_DARK, fill_opacity=0.55,
                  stroke_color=WHEEL_BODY, stroke_width=2.5)
    rim = Annulus(inner_radius=radius * 0.86, outer_radius=radius,
                  fill_color=WHEEL_RIM, fill_opacity=0.9, stroke_width=0)
    spokes = VGroup()
    for k in range(n_spokes):
        ang = TAU * k / n_spokes
        u = np.array([np.cos(ang), np.sin(ang), 0])
        sp = Line(u * radius * 0.16, u * radius * 0.84,
                  color=SPOKE_COL, stroke_width=4)
        spokes.add(sp)
    hub = Circle(radius=radius * 0.15, fill_color=HUB_COL, fill_opacity=1,
                 stroke_color=WHEEL_DARK, stroke_width=2)
    # an asymmetric notch so rotation is visible at any speed
    notch = Dot(radius=0.07 * scale, color=SPARK_COL).move_to(
        np.array([radius * 0.70, 0, 0]))
    g = VGroup(body, rim, spokes, hub, notch)
    g.move_to(pos)
    return g


def axis_pin(pos=ORIGIN, scale=1.0):
    """A small fixed-axis marker (cross + dot) for the wheel center."""
    d = 0.16 * scale
    h = Line([-d, 0, 0], [d, 0, 0], color=HUB_COL, stroke_width=3)
    v = Line([0, -d, 0], [0, d, 0], color=HUB_COL, stroke_width=3)
    c = Dot(radius=0.05 * scale, color=HUB_COL)
    return VGroup(h, v, c).move_to(pos)


def speed_zero_tag(pos, scale=1.0):
    """A 'speed = 0' tag pinned to a point, with a small leader dot."""
    dot = Dot(radius=0.07 * scale, color=HUB_COL).move_to(pos)
    box = Text("speed = 0", font="sans", font_size=26, color=LABEL_COL)
    box.next_to(pos, UP, buff=0.35)
    leader = Line(pos, box.get_bottom() + DOWN * 0.04,
                  color=DIM_COL, stroke_width=2)
    return VGroup(leader, dot, box)


def question_mark(pos, size=64, color=SPEED_COL):
    return Text("?", font="sans", font_size=size, color=color).move_to(pos)


def make_hand(scale=1.0):
    """A simple stylized grabbing hand: palm + curled fingers, opening left.
    Place by .move_to / .next_to; it grips toward its right side."""
    palm = RoundedRectangle(width=0.62 * scale, height=0.78 * scale,
                            corner_radius=0.16 * scale,
                            fill_color="#D9B48F", fill_opacity=1,
                            stroke_color="#7A5B40", stroke_width=2)
    fingers = VGroup()
    for k in range(3):
        f = RoundedRectangle(width=0.30 * scale, height=0.16 * scale,
                             corner_radius=0.07 * scale,
                             fill_color="#D9B48F", fill_opacity=1,
                             stroke_color="#7A5B40", stroke_width=2)
        f.move_to(palm.get_right() + RIGHT * 0.16 * scale
                  + (UP * (0.22 - 0.22 * k)) * scale)
        fingers.add(f)
    thumb = RoundedRectangle(width=0.16 * scale, height=0.30 * scale,
                             corner_radius=0.07 * scale,
                             fill_color="#D9B48F", fill_opacity=1,
                             stroke_color="#7A5B40", stroke_width=2)
    thumb.move_to(palm.get_right() + RIGHT * 0.04 * scale
                  + DOWN * 0.36 * scale)
    return VGroup(palm, fingers, thumb)


def spark_burst(center, n=9, r_in=0.05, r_out=0.40, scale=1.0):
    """Short radial spark lines emanating from a contact point."""
    center = np.array(center, dtype=float)
    g = VGroup()
    rng = np.random.default_rng(4)
    for k in range(n):
        ang = TAU * k / n + rng.uniform(-0.18, 0.18)
        u = np.array([np.cos(ang), np.sin(ang), 0])
        a = (r_in + rng.uniform(0.0, 0.06)) * scale
        b = (r_out * rng.uniform(0.6, 1.0)) * scale
        ln = Line(center + u * a, center + u * b,
                  color=SPARK_COL, stroke_width=3)
        g.add(ln)
    return g


def rim_element(angle, center, radius, scale=1.0, color=MASS_COL):
    """A small mass dot sitting on the rim at the given angle."""
    center = np.array(center, dtype=float)
    u = np.array([np.cos(angle), np.sin(angle), 0])
    return Dot(radius=0.10 * scale, color=color).move_to(
        center + u * radius)


def tangent_speed_arrow(angle, center, radius, length=0.7,
                        color=SPEED_COL, scale=1.0):
    """A velocity arrow tangent to the circle (counter-clockwise) at angle."""
    center = np.array(center, dtype=float)
    pos = center + np.array([np.cos(angle), np.sin(angle), 0]) * radius
    tang = np.array([-np.sin(angle), np.cos(angle), 0])
    tail = pos
    head = pos + tang * length * scale
    return Arrow(tail, head, color=color, stroke_width=4, buff=0,
                 max_tip_length_to_length_ratio=0.32, tip_length=0.16)


def energy_bar(height, pos, width=0.5, color=ENERGY_COL, label=None,
               max_h=3.0):
    """A vertical filled energy bar growing upward from `pos` (its base
    center). Optional text label below."""
    h = float(np.clip(height, 0.001, max_h))
    bar = Rectangle(width=width, height=h, fill_color=color,
                    fill_opacity=0.9, stroke_color=color, stroke_width=2)
    bar.move_to(np.array(pos, dtype=float) + np.array([0, h / 2.0, 0]))
    if label is None:
        return bar
    txt = Text(label, font="sans", font_size=22, color=LABEL_COL)
    txt.next_to(np.array(pos, dtype=float), DOWN, buff=0.18)
    return VGroup(bar, txt)


def mass_disk(pos, radius=1.3, at_rim=True, scale=1.0, n_blobs=8):
    """A disk with mass concentrated either near the hub or at the rim.
    Same total 'mass' (same number of blobs), different placement."""
    radius = radius * scale
    ring = Circle(radius=radius, stroke_color=WHEEL_BODY, stroke_width=2,
                  fill_opacity=0)
    hub = Dot(radius=0.07 * scale, color=HUB_COL)
    blobs = VGroup()
    rr = radius * (0.90 if at_rim else 0.28)
    for k in range(n_blobs):
        ang = TAU * k / n_blobs
        u = np.array([np.cos(ang), np.sin(ang), 0])
        blobs.add(Dot(radius=0.11 * scale, color=MASS_COL).move_to(u * rr))
    g = VGroup(ring, blobs, hub)
    g.move_to(pos)
    return g


def moi_label(pos, size=28, color=LABEL_COL):
    return Text("moment of inertia", font="sans", font_size=size,
                color=color).move_to(pos)


def make_potters_wheel(pos=ORIGIN, scale=1.0):
    """A potter's wheel: a broad flat disk seen slightly from above,
    with a center spindle and a clay lump."""
    plate = Ellipse(width=2.6 * scale, height=0.9 * scale,
                    fill_color=WHEEL_DARK, fill_opacity=0.7,
                    stroke_color=WHEEL_BODY, stroke_width=2.5)
    rim = Ellipse(width=2.6 * scale, height=0.9 * scale,
                  stroke_color=WHEEL_RIM, stroke_width=4, fill_opacity=0)
    spindle = Line(ORIGIN, UP * 0.42 * scale, color=SPOKE_COL,
                   stroke_width=5)
    clay = Ellipse(width=0.7 * scale, height=0.40 * scale,
                   fill_color="#9C6B4A", fill_opacity=1,
                   stroke_color="#5E3F2C", stroke_width=2)
    clay.move_to(UP * 0.40 * scale)
    g = VGroup(plate, rim, spindle, clay)
    g.move_to(pos)
    return g


def make_ball(pos=ORIGIN, radius=0.45, scale=1.0):
    """A solid ball with a marker dot so rolling/spin reads."""
    radius = radius * scale
    b = Circle(radius=radius, fill_color=WHEEL_BODY, fill_opacity=0.85,
               stroke_color=WHEEL_RIM, stroke_width=2.5)
    mark = Dot(radius=0.08 * scale, color=SPARK_COL).move_to(
        np.array(ORIGIN) + RIGHT * radius * 0.62)
    g = VGroup(b, mark)
    g.move_to(pos)
    return g


def make_slope(width=8.0, drop=3.0, base_y=-2.6, x0=-4.4):
    """A ramp line going down-right; returns (line, start_pt, end_pt)."""
    start = np.array([x0, base_y + drop, 0])
    end = np.array([x0 + width, base_y, 0])
    ln = Line(start, end, color=DIM_COL, stroke_width=4)
    return ln, start, end


def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
