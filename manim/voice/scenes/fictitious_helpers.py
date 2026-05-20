"""Helpers for the Fictitious Forces (centrifugal & Coriolis) scene.

Primitives:
  - top_down_car : a small car seen from above, with a passenger dot
  - curve_path   : a smooth left-curving road arc
  - outward_arrow: a short straight arrow
  - rotating_disk: a top-down platform/disk with spokes + rim ticks
  - make_globe   : a simple stylised rotating-globe disk
  - frame_label  : small caption text
  - split_divider: a thin vertical divider for split-screen beats
"""

from manim import *
import numpy as np

VOID = "#000000"

CAR_BODY   = "#C9D6E8"
CAR_TRIM   = "#6E7F94"
PASSENGER  = "#E8C46A"
ROAD_COL   = "#3A4654"
PATH_COL   = "#7FB8E8"
FORCE_COL  = "#E07A5F"
DISK_COL   = "#2E3A47"
DISK_RIM   = "#7FB8E8"
BALL_COL   = "#EAE4D5"
GLOBE_SEA  = "#23415E"
GLOBE_LAND = "#3E6B4A"
FLOW_COL   = "#7FB8E8"
LABEL_COL  = "#8C98A6"
ACCENT     = "#EAE4D5"


def top_down_car(pos=(0, 0, 0), scale=1.0, angle=0.0):
    """A car seen from directly above: rounded body, windshield band,
    and a passenger dot offset toward the right side of the cabin."""
    s = scale
    body = RoundedRectangle(width=1.05 * s, height=1.85 * s,
                            corner_radius=0.28 * s,
                            fill_color=CAR_BODY, fill_opacity=1,
                            stroke_color=CAR_TRIM, stroke_width=2)
    windshield = RoundedRectangle(width=0.82 * s, height=0.46 * s,
                                  corner_radius=0.12 * s,
                                  fill_color=CAR_TRIM, fill_opacity=0.55,
                                  stroke_width=0).shift(UP * 0.52 * s)
    rear = RoundedRectangle(width=0.82 * s, height=0.34 * s,
                            corner_radius=0.10 * s,
                            fill_color=CAR_TRIM, fill_opacity=0.35,
                            stroke_width=0).shift(DOWN * 0.55 * s)
    passenger = Dot(radius=0.15 * s, color=PASSENGER).shift(
        RIGHT * 0.24 * s + UP * 0.10 * s)
    g = VGroup(body, windshield, rear, passenger)
    g.rotate(angle)
    g.move_to(np.array(pos, dtype=float))
    return g


def curve_path(start=(-5.0, -2.0, 0), end=(2.2, 2.3, 0), bend=-3.0,
                color=ROAD_COL, width=46, stroke_only=False):
    """A smooth left-curving road as a thick arc. `bend` < 0 curves left."""
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    arc = ArcBetweenPoints(s, e, angle=bend)
    arc.set_stroke(color=color, width=width)
    if stroke_only:
        arc.set_fill(opacity=0)
    return arc


def outward_arrow(start, vec, color=FORCE_COL, width=6):
    s = np.array(start, dtype=float)
    e = s + np.array(vec, dtype=float)
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.32, tip_length=0.26)


def straight_dashed(start, end, color=PATH_COL, width=3):
    return DashedLine(np.array(start, dtype=float),
                      np.array(end, dtype=float),
                      color=color, stroke_width=width,
                      dash_length=0.16).set_opacity(0.85)


def rotating_disk(center=(0, 0, 0), radius=2.6, n_spokes=8,
                  fill=DISK_COL, rim=DISK_RIM):
    """A top-down platform: filled disk, bright rim, spokes and one
    bright reference spoke so its rotation is legible."""
    c = np.array(center, dtype=float)
    disk = Circle(radius=radius, fill_color=fill, fill_opacity=1,
                  stroke_color=rim, stroke_width=3).move_to(c)
    spokes = VGroup()
    for k in range(n_spokes):
        ang = TAU * k / n_spokes
        u = np.array([np.cos(ang), np.sin(ang), 0])
        spokes.add(Line(c, c + u * radius, color=rim,
                        stroke_width=1.6).set_opacity(0.45))
    ref = Line(c, c + np.array([radius, 0, 0]), color=ACCENT,
               stroke_width=4).set_opacity(0.9)
    hub = Dot(point=c, radius=0.12, color=ACCENT)
    return VGroup(disk, spokes, ref, hub)


def make_globe(center=(0, 0, 0), radius=2.4):
    """A stylised globe: ocean disk, two soft land blobs, an axis tilt,
    and faint latitude lines."""
    c = np.array(center, dtype=float)
    sea = Circle(radius=radius, fill_color=GLOBE_SEA, fill_opacity=1,
                 stroke_color=FLOW_COL, stroke_width=2.5).move_to(c)
    land1 = Ellipse(width=1.5, height=1.9, fill_color=GLOBE_LAND,
                    fill_opacity=0.9, stroke_width=0
                    ).move_to(c + np.array([-0.7, 0.5, 0]))
    land2 = Ellipse(width=1.2, height=1.0, fill_color=GLOBE_LAND,
                    fill_opacity=0.9, stroke_width=0
                    ).move_to(c + np.array([0.9, -0.8, 0]))
    lats = VGroup()
    for dy in (-1.3, -0.6, 0.0, 0.6, 1.3):
        w = 2 * np.sqrt(max(radius ** 2 - dy ** 2, 0.04))
        lats.add(Ellipse(width=w, height=0.20, stroke_color=FLOW_COL,
                         stroke_width=1.2, fill_opacity=0
                         ).move_to(c + np.array([0, dy, 0])).set_opacity(0.30))
    clip = Circle(radius=radius).move_to(c)
    land = VGroup(land1, land2)
    return VGroup(sea, land, lats), clip


def curved_flow(center, r0, span=PI * 0.7, start_ang=0.6, color=FLOW_COL,
                width=5, clockwise=True):
    """A curving flow arrow along an arc around `center` (for winds/
    currents that get steered by Coriolis)."""
    c = np.array(center, dtype=float)
    sign = -1 if clockwise else 1
    a0 = start_ang
    a1 = start_ang + sign * span
    p0 = c + r0 * np.array([np.cos(a0), np.sin(a0), 0])
    p1 = c + r0 * np.array([np.cos(a1), np.sin(a1), 0])
    arc = ArcBetweenPoints(p0, p1, angle=sign * span)
    arc.set_stroke(color=color, width=width)
    tip = ArrowTriangleFilledTip(color=color).scale(0.9)
    arc.add_tip(tip)
    return arc


def frame_label(text, pos, color=LABEL_COL, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(np.array(pos, dtype=float)).set_opacity(opacity)


def big_label(text, pos, color=ACCENT, size=40):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(np.array(pos, dtype=float))


def split_divider(x=0.0, color="#3A4654"):
    return DashedLine([x, -3.6, 0], [x, 3.6, 0], color=color,
                      stroke_width=2, dash_length=0.14).set_opacity(0.55)
