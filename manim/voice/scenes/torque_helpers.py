"""Helpers for the Torque & Lever Arm (torque) scene.

Primitives: a bolt on a pivot, a wrench whose handle can be extended,
force arrows, the force line + perpendicular lever-arm highlight, and a
top-down door. Pure #000000 void, font="sans" for any text.
"""

from manim import *
import numpy as np

VOID = "#000000"

STEEL       = "#C8CCD2"   # wrench / bar metal
STEEL_DARK  = "#7E848C"
BOLT_COL    = "#9AA0A8"
BOLT_DARK   = "#5C6068"
FORCE_COL   = "#E8965A"   # push / force arrows
ROT_COL     = "#7FB8E8"   # rotation / torque arrows
LEVER_COL   = "#F2D74E"   # bright lever-arm highlight
LINE_FAINT  = "#5A6E80"   # force line of action (dashed, faint)
LABEL_COL   = "#EAE4D5"
DIM_COL     = "#8C98A6"
DOOR_COL    = "#B8A98C"
DOOR_DARK   = "#7E725C"


def make_bolt(pos, radius=0.34):
    """A hex-head bolt seen from the side / front (the pivot point)."""
    pos = np.array(pos, dtype=float)
    hexagon = RegularPolygon(n=6, radius=radius, start_angle=PI / 6,
                             fill_color=BOLT_COL, fill_opacity=1,
                             stroke_color=BOLT_DARK, stroke_width=2.0)
    inner = Circle(radius=radius * 0.42, fill_color=BOLT_DARK,
                   fill_opacity=1, stroke_width=0)
    dot = Dot(radius=0.025, color=LABEL_COL)
    return VGroup(hexagon, inner, dot).move_to(pos)


def pivot_dot(pos, color=LABEL_COL, r=0.06):
    """A small marker for the rotation axis."""
    return Dot(point=np.array(pos, dtype=float), radius=r, color=color)


def make_wrench(pivot, length=2.4, angle=0.0, jaw_radius=0.40):
    """A wrench: an open jaw gripping a bolt at `pivot`, with a straight
    handle of `length` extending at `angle` (radians, 0 = +x / right).
    Returns a VGroup positioned so the jaw centers on `pivot`."""
    pivot = np.array(pivot, dtype=float)
    u = np.array([np.cos(angle), np.sin(angle), 0])
    # straight handle as a thick rounded rectangle along +u from the jaw
    handle = RoundedRectangle(width=length, height=0.20, corner_radius=0.08,
                              fill_color=STEEL, fill_opacity=1,
                              stroke_color=STEEL_DARK, stroke_width=1.6)
    handle.rotate(angle)
    handle.move_to(pivot + u * (jaw_radius + length / 2.0))
    # open ring jaw around the bolt
    ring = Annulus(inner_radius=jaw_radius, outer_radius=jaw_radius + 0.16,
                   fill_color=STEEL, fill_opacity=1,
                   stroke_color=STEEL_DARK, stroke_width=1.6)
    ring.move_to(pivot)
    # the open mouth of the jaw (notch facing away from the handle)
    mouth = Sector(radius=jaw_radius + 0.20, angle=PI * 0.32,
                   start_angle=angle + PI - PI * 0.16,
                   fill_color=VOID, fill_opacity=1, stroke_width=0)
    mouth.move_to(pivot)
    return VGroup(ring, mouth, handle)


def force_arrow(start, vec, color=FORCE_COL, width=7, tip=0.32):
    """A straight force arrow from `start` along `vec`."""
    s = np.array(start, dtype=float)
    e = s + np.array(vec, dtype=float)
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=tip)


def rot_arrow(pivot, radius=0.95, start_angle=-PI / 3, sweep=PI * 0.95,
              color=ROT_COL, width=7):
    """A curved rotation arrow around `pivot` (counter-clockwise)."""
    pivot = np.array(pivot, dtype=float)
    arc = Arc(radius=radius, start_angle=start_angle, angle=sweep,
              arc_center=pivot, color=color, stroke_width=width)
    arc.add_tip(tip_length=0.26)
    return arc


def line_of_action(point, direction, half_len=4.0, color=LINE_FAINT):
    """A faint dashed line through `point` along `direction` (the force's
    extended line of action)."""
    point = np.array(point, dtype=float)
    d = np.array(direction, dtype=float)
    d = d / (np.linalg.norm(d) + 1e-9)
    a = point - d * half_len
    b = point + d * half_len
    return DashedLine(a, b, color=color, stroke_width=2.4,
                      dash_length=0.14).set_opacity(0.7)


def perp_foot(pivot, point, direction):
    """Foot of the perpendicular from `pivot` onto the line through
    `point` with `direction`. Returns the 3D foot coordinate."""
    pivot = np.array(pivot, dtype=float)
    point = np.array(point, dtype=float)
    d = np.array(direction, dtype=float)
    d = d / (np.linalg.norm(d) + 1e-9)
    t = np.dot(pivot - point, d)
    return point + d * t


def lever_arm(pivot, foot, color=LEVER_COL, width=7):
    """The bright perpendicular segment from pivot to the line of action."""
    return Line(np.array(pivot, dtype=float), np.array(foot, dtype=float),
                color=color, stroke_width=width)


def right_angle_mark(corner, dir_a, dir_b, size=0.22, color=LEVER_COL):
    """A small right-angle square at `corner` between unit-ish dir_a/dir_b."""
    corner = np.array(corner, dtype=float)
    a = np.array(dir_a, dtype=float); a = a / (np.linalg.norm(a) + 1e-9)
    b = np.array(dir_b, dtype=float); b = b / (np.linalg.norm(b) + 1e-9)
    p0 = corner + a * size
    p1 = corner + a * size + b * size
    p2 = corner + b * size
    return VMobject(color=color, stroke_width=2.4).set_points_as_corners(
        [p0, p1, p2])


def make_door_topdown(hinge, length=3.4, angle=0.0):
    """Top-down view of a door: a bar hinged at `hinge`, opening at
    `angle` (radians) from the closed (+x) position. Includes a small
    hinge marker and a handle dot near the free end."""
    hinge = np.array(hinge, dtype=float)
    u = np.array([np.cos(angle), np.sin(angle), 0])
    leaf = RoundedRectangle(width=length, height=0.16, corner_radius=0.05,
                            fill_color=DOOR_COL, fill_opacity=1,
                            stroke_color=DOOR_DARK, stroke_width=1.6)
    leaf.rotate(angle)
    leaf.move_to(hinge + u * (length / 2.0))
    hinge_m = VGroup(
        Circle(radius=0.12, fill_color=STEEL_DARK, fill_opacity=1,
               stroke_width=0),
        Dot(radius=0.04, color=LABEL_COL),
    ).move_to(hinge)
    handle = Dot(point=hinge + u * (length - 0.22), radius=0.09,
                 color=STEEL)
    return VGroup(leaf, hinge_m, handle)


def tau_label(pos, size=52, color=ROT_COL):
    return Text("τ", font="sans", font_size=size, color=color
                ).move_to(pos)


def small_label(text, pos, color=DIM_COL, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
