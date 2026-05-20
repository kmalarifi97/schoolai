"""Helpers for the Angular Motion (angular) scene.

Primitives: a top-down rotating disk, hub/rim dots, a rigid spoke through
both dots, an angle wedge with theta/omega/alpha labels, and the
linear-vs-angular cascade. Pure #000000 void, font="sans".
"""

from manim import *
import numpy as np

VOID = "#000000"

DISK_FILL   = "#1C2530"
DISK_STROKE = "#5A7186"
RIM_COL     = "#7FB8E8"   # the rim child / fast point
HUB_COL     = "#E8B57F"   # the hub child / slow point
SPOKE_COL   = "#CDB4F0"
WEDGE_COL   = "#7FB8E8"
LABEL_COL   = "#EAE4D5"
FAINT_COL   = "#8C98A6"
GLOW_COL    = "#9FE0C8"


def make_disk(center=(0, 0, 0), radius=2.4):
    """Top-down rotating disk: filled circle, rim ring, center pivot."""
    c = np.array(center, dtype=float)
    face = Circle(radius=radius, fill_color=DISK_FILL, fill_opacity=1.0,
                  stroke_color=DISK_STROKE, stroke_width=3).move_to(c)
    rim = Circle(radius=radius, stroke_color=DISK_STROKE, stroke_width=3,
                 fill_opacity=0).move_to(c)
    pivot = Dot(point=c, radius=0.055, color=DISK_STROKE)
    return VGroup(face, rim, pivot)


def hub_dot(center=(0, 0, 0), radius=2.4, frac=0.34, color=HUB_COL):
    """The near-center child: a dot at frac*radius from the center."""
    c = np.array(center, dtype=float)
    return Dot(point=c + np.array([frac * radius, 0, 0]),
               radius=0.13, color=color)


def rim_dot(center=(0, 0, 0), radius=2.4, frac=0.92, color=RIM_COL):
    """The edge child: a dot out near the rim."""
    c = np.array(center, dtype=float)
    return Dot(point=c + np.array([frac * radius, 0, 0]),
               radius=0.13, color=color)


def rigid_spoke(center=(0, 0, 0), radius=2.4, hub_frac=0.34, rim_frac=0.92,
                color=SPOKE_COL):
    """A straight rigid spoke from center out through hub & rim dots."""
    c = np.array(center, dtype=float)
    end = c + np.array([radius * (rim_frac + 0.04), 0, 0])
    return Line(c, end, color=color, stroke_width=5)


def angle_wedge(center=(0, 0, 0), radius=1.4, start_ang=0.0, sweep=PI / 3,
                color=WEDGE_COL, opacity=0.32):
    """A filled pie-slice wedge showing angle swept from start_ang.

    Sector's arc center is its vertex; pin that vertex to `center`.
    """
    c = np.array(center, dtype=float)
    sec = Sector(radius=radius, start_angle=start_ang,
                 angle=sweep, fill_color=color, fill_opacity=opacity,
                 stroke_color=color, stroke_width=2.5)
    sec.shift(c - sec.get_arc_center())
    return sec


def greek_label(symbol, pos, size=46, color=LABEL_COL):
    """A single Greek/Latin symbol label (theta, omega, alpha, r)."""
    return Text(symbol, font="sans", font_size=size, color=color,
                slant=ITALIC).move_to(pos)


def small_label(text, pos, color=FAINT_COL, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def cascade(labels, pos, color=LABEL_COL, arrow_color=FAINT_COL,
            label_text=None, size=44, dx=2.0):
    """Horizontal X -> V -> A (or theta -> omega -> alpha) cascade with
    derivative arrows between terms. `labels` is a 3-tuple of symbols.
    Returns VGroup(terms_vgroup, arrows_vgroup)."""
    p = np.array(pos, dtype=float)
    terms = VGroup()
    for k, s in enumerate(labels):
        t = Text(s, font="sans", font_size=size, color=color,
                 slant=ITALIC).move_to(p + np.array([k * dx, 0, 0]))
        terms.add(t)
    arrows = VGroup()
    for k in range(len(labels) - 1):
        a = Arrow(terms[k].get_right() + RIGHT * 0.10,
                  terms[k + 1].get_left() + LEFT * 0.10,
                  color=arrow_color, stroke_width=3.5,
                  buff=0.05, max_tip_length_to_length_ratio=0.30)
        arrows.add(a)
    return VGroup(terms, arrows)
