"""Helpers for Newton's Law of Universal Gravitation (newton) explainer.

The video holds a SPLIT FRAME throughout: the physical world on the LEFT,
the equation as a scoreboard that fills in on the RIGHT. The equation is

    F = G  m_1 m_2 / r^2

built up piece by piece across the beats and fully assembled at b8.

Visual contract (shared with the gravity series):
- Pure #000000 void background. Don't change it.
- font="sans" for ANY Text (Manim's default fallback collapses kerning).
- Color-binding: when a parameter is explained, the symbol in the equation
  AND its object on the LEFT glow the SAME color (RED).
- b10 reuses grav_helpers.make_fabric_3d for the curved-space "bend" callback.

This file owns newton-only primitives. Don't pollute grav_helpers.py.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Palette --------------------------------------------------------------
RED      = "#E04848"   # the "glow" / binding color for an explained term
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary text/guides
FAINT    = "#5A5446"   # faintest guide lines
MASS1    = "#5B9BD5"   # mass 1 — blue
MASS1_D  = "#3A6E9E"
MASS2    = "#D9A441"   # mass 2 — amber
MASS2_D  = "#A87A26"
NEUTRAL  = "#9AA8C0"
NEUTRAL_D= "#5E6B82"
COIN     = "#C9B07A"
COIN_D   = "#8C7A4E"


# ----------------------------------------------------------------------
# A mass body. Returns a Circle (so .animate.set_fill etc. work simply).
# ----------------------------------------------------------------------
def make_mass(pos=ORIGIN, r=0.45, color=MASS1, edge=MASS1_D):
    return Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=edge, stroke_width=2.5).move_to(pos)


# ----------------------------------------------------------------------
# A "pull" arrow between two points. Width/strength scalable so it can
# act as a live knob (thicker = stronger pull).
# ----------------------------------------------------------------------
def pull_arrow(start, end, color=CHALK, width=6, tip=0.22):
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    return Arrow(start, end, color=color, stroke_width=width,
                 buff=0.0, max_tip_length_to_length_ratio=tip,
                 max_stroke_width_to_length_ratio=999)


def double_pull(a_pos, b_pos, a_r, b_r, color=RED, width=6):
    """Two arrows pointing inward (each mass pulled toward the other)."""
    a_pos = np.array(a_pos, dtype=float)
    b_pos = np.array(b_pos, dtype=float)
    u = (b_pos - a_pos)
    u = u / np.linalg.norm(u)
    a_edge = a_pos + u * a_r
    b_edge = b_pos - u * b_r
    mid = (a_edge + b_edge) / 2.0
    arr_a = pull_arrow(a_edge + u * 0.05, mid - u * 0.05, color=color, width=width)
    arr_b = pull_arrow(b_edge - u * 0.05, mid + u * 0.05, color=color, width=width)
    return VGroup(arr_a, arr_b)


# ----------------------------------------------------------------------
# A coin (thin disc seen at slight angle) for the "two coins" beat.
# ----------------------------------------------------------------------
def make_coin(pos=ORIGIN, w=0.55):
    body = Ellipse(width=w, height=w * 0.34, fill_color=COIN,
                   fill_opacity=1, stroke_color=COIN_D, stroke_width=2)
    rim = Ellipse(width=w * 0.7, height=w * 0.22, fill_opacity=0,
                  stroke_color=COIN_D, stroke_width=1.2)
    return VGroup(body, rim).move_to(pos)


# ----------------------------------------------------------------------
# Text label helper (always font="sans").
# ----------------------------------------------------------------------
def label(text, pos=ORIGIN, size=28, color=CHALK, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=64, color=DIM, opacity=0.7):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


# ----------------------------------------------------------------------
# The split-frame divider line.
# ----------------------------------------------------------------------
def divider(x=0.4):
    return Line([x, -3.6, 0], [x, 3.6, 0], color=FAINT, stroke_width=1.5
                ).set_opacity(0.5)


# ----------------------------------------------------------------------
# The equation scoreboard — Newton's law of universal gravitation.
#
#     F = G  (m_1 m_2) / r^2
#
# Built so individual parts can be colored/animated by isolation index.
# We expose named handles:
#   eq.F      -> the F glyph
#   eq.eqsign -> the '='
#   eq.G      -> the G glyph
#   eq.frac   -> the m_1 m_2 / r^2 fraction
#   eq.m1     -> the m_1 part
#   eq.m2     -> the m_2 part
#   eq.r      -> the r (in r^2)
#   eq.rsq    -> the r^2 part
# ----------------------------------------------------------------------
def make_equation(pos=ORIGIN, scale=1.0):
    # Each numerator/denominator piece is its own MathTex arg so it gets its
    # own submobject. We avoid substrings_to_isolate (it breaks \frac by
    # isolating the bare "r" inside the control sequence).
    eq = MathTex(
        r"F", r"=", r"G",
        r"{m_1\,m_2", r"\over", r"r^2}",
    )
    eq.set_color(CHALK)
    eq.scale(scale)
    eq.move_to(pos)
    # Stable submobject layout:
    #   0 F   1 =   2 G   3 m_1 m_2 (numerator)   4 (fraction bar)   5 r^2
    eq.F      = eq[0]
    eq.eqsign = eq[1]
    eq.G      = eq[2]
    eq.num    = eq[3]      # m_1 m_2
    eq.bar    = eq[4]      # the over-bar
    eq.rsq    = eq[5]      # r^2
    eq.frac   = VGroup(eq[3], eq[4], eq[5])
    eq.m1     = eq[3][0:2]   # m_1 (m + subscript 1)
    eq.m2     = eq[3][2:4]   # m_2 (m + subscript 2)
    return eq


def eq_part(eq, tex):
    try:
        return eq.get_part_by_tex(tex)
    except Exception:
        return None
