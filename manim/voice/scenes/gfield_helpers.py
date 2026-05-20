"""Helpers for the Gravitational Field (gfield) scene.

Reuses make_earth / make_rock from grav_helpers and adds field-arrow
primitives: radial inward arrows around a body whose length and density
scale with proximity (the field gets stronger near the mass).
"""

from manim import *
import numpy as np

from grav_helpers import make_earth, make_rock  # noqa: F401

VOID = "#000000"

FIELD_COLOR = "#7FB8E8"
FIELD_FAINT = "#4A6E8C"
G_LABEL_COL = "#EAE4D5"
MOON_GREY   = "#B8B8BE"
MOON_DARK   = "#6E6E76"


def make_moon(pos, scale=1.0):
    """A small cratered grey moon."""
    body = Circle(radius=0.26 * scale, fill_color=MOON_GREY, fill_opacity=1,
                  stroke_color=MOON_DARK, stroke_width=1.4)
    cr1 = Circle(radius=0.06 * scale, fill_color=MOON_DARK, fill_opacity=0.7,
                 stroke_width=0).shift((LEFT * 0.08 + UP * 0.06) * scale)
    cr2 = Circle(radius=0.045 * scale, fill_color=MOON_DARK, fill_opacity=0.7,
                 stroke_width=0).shift((RIGHT * 0.10 + DOWN * 0.07) * scale)
    cr3 = Circle(radius=0.035 * scale, fill_color=MOON_DARK, fill_opacity=0.7,
                 stroke_width=0).shift((RIGHT * 0.02 + UP * 0.12) * scale)
    hl = (Ellipse(width=0.14 * scale, height=0.08 * scale, fill_color=WHITE,
                  fill_opacity=0.18, stroke_width=0)
          .shift((LEFT * 0.09 + UP * 0.09) * scale))
    return VGroup(body, cr1, cr2, cr3, hl).move_to(pos)


def down_arrow(start, length=1.2, color=FIELD_COLOR, width=5):
    """A single straight arrow pointing straight down from `start`."""
    s = np.array(start, dtype=float)
    e = s + np.array([0, -length, 0])
    return Arrow(s, e, color=color, stroke_width=width,
                 buff=0, max_tip_length_to_length_ratio=0.28)


def radial_field(center, body_radius=0.40, n_rings=3, n_per_ring=12,
                  inner_gap=0.30, ring_step=1.05, color=FIELD_COLOR,
                  faint=FIELD_FAINT, max_radius=None):
    """Radial INWARD field arrows around a body.

    Arrows point toward `center`. Closer rings: longer arrows, more of them,
    brighter. Far rings: shorter, thinner, fainter — never zero.
    Returns a VGroup of Arrows.
    """
    center = np.array(center, dtype=float)
    g = VGroup()
    for k in range(n_rings):
        r_tail = body_radius + inner_gap + ring_step * (k + 1)
        if max_radius is not None and r_tail > max_radius:
            break
        # field strength ~ 1/r^2 feel, mapped to arrow length
        strength = 1.0 / ((k + 1) ** 1.35)
        arrow_len = 0.30 + 1.05 * strength
        r_head = max(body_radius + 0.10, r_tail - arrow_len)
        # density: more arrows close in, fewer far out
        count = max(6, int(round(n_per_ring * (1.0 - 0.18 * k))))
        # color/opacity ramp
        t = k / max(1, n_rings - 1)
        col = interpolate_color(ManimColor(color), ManimColor(faint), t)
        op = 0.95 - 0.55 * t
        sw = 4.6 - 2.0 * t
        for j in range(count):
            ang = TAU * j / count + (0.12 * k)
            u = np.array([np.cos(ang), np.sin(ang), 0])
            tail = center + u * r_tail
            head = center + u * r_head
            a = Arrow(tail, head, color=col, stroke_width=sw,
                      buff=0, max_tip_length_to_length_ratio=0.22,
                      tip_length=0.18)
            a.set_opacity(op)
            g.add(a)
    return g


def field_arrow_at(center, point, body_radius=0.40, color=FIELD_COLOR):
    """A single field arrow at `point` pointing toward `center`,
    length scaled by 1/r^2-ish proximity. Used for the test mass."""
    center = np.array(center, dtype=float)
    point = np.array(point, dtype=float)
    v = center - point
    r = np.linalg.norm(v)
    u = v / r if r > 1e-6 else np.array([0, -1.0, 0])
    ref = body_radius + 1.35  # reference distance
    strength = (ref / max(r, body_radius + 0.2)) ** 2
    arrow_len = float(np.clip(0.45 + 0.55 * strength, 0.35, 1.7))
    tail = point
    head = point + u * arrow_len
    return Arrow(tail, head, color=color, stroke_width=5,
                 buff=0, max_tip_length_to_length_ratio=0.30)


def g_label(pos, size=40, color=G_LABEL_COL):
    return Text("g", font="sans", font_size=size, color=color,
                slant=ITALIC).move_to(pos)


def small_label(text, pos, color=WHITE, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
