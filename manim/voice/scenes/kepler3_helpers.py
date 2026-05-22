"""Helpers for the Kepler's Third Law (kepler3) explainer.

The video holds a SPLIT FRAME throughout: the orbital world on the LEFT,
the equation as a scoreboard that fills in on the RIGHT. The equation is

    (r_A / r_B)^3 = (T_A / T_B)^2

built up piece by piece across the beats and fully assembled at b10.

Visual contract (shared with the gravity series):
- Pure #000000 void background. Don't change it.
- font="sans" for ANY Text (Manim's default fallback collapses kerning).
- Color-binding: when a parameter is explained, the symbol in the equation
  AND its object on the LEFT glow the SAME color (RED). Planets A/B carry
  blue/green tints that also tint their subscripts.
- b13 reuses grav_helpers.make_fabric_3d for the curved-space "bend" callback.

This file owns kepler3-only primitives. Don't pollute grav_helpers.py.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Palette --------------------------------------------------------------
SUN_CORE = "#FFF4D6"
RED      = "#E04848"   # the "glow" / binding color for an explained term
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary text/guides
FAINT    = "#5A5446"   # faintest guide lines
PLANET_A = "#5B9BD5"   # planet A — blue
PLANET_AD= "#3A6E9E"
PLANET_B = "#6FBF73"   # planet B — green
PLANET_BD= "#4A8C50"
NEUTRAL  = "#9AA8C0"   # a generic single planet (cool slate)
NEUTRAL_D= "#5E6B82"
CLOCKFACE= "#E8E2D2"
CLOCKRIM = "#8C8576"


# ----------------------------------------------------------------------
# Sun — soft layered glow at a center.
# ----------------------------------------------------------------------
def make_sun(pos=ORIGIN, scale=1.0):
    g = VGroup()
    for r, op in [(0.85, 0.04), (0.65, 0.08), (0.45, 0.18), (0.30, 0.50)]:
        g.add(Circle(radius=r, color=SUN_CORE, fill_color=SUN_CORE,
                     fill_opacity=op, stroke_width=0))
    g.add(Circle(radius=0.16, color=WHITE, fill_color=WHITE,
                 fill_opacity=1.0, stroke_width=0))
    return g.scale(scale).move_to(pos)


# ----------------------------------------------------------------------
# A planet body. Returns a Circle (so .animate.set_fill etc. work simply).
# ----------------------------------------------------------------------
def make_planet(pos=ORIGIN, r=0.20, color=NEUTRAL, edge=NEUTRAL_D):
    return Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=edge, stroke_width=2).move_to(pos)


# ----------------------------------------------------------------------
# An orbit ring (dotted, calm). Centered on `center`, radius r.
# ----------------------------------------------------------------------
def orbit_ring(center=ORIGIN, r=1.8, color=FAINT, width=2.5, n_dashes=44):
    center = np.array(center, dtype=float)
    pts = []
    for i in range(121):
        ang = PI / 2 - 2 * np.pi * (i / 120)
        pts.append(center + np.array([r * np.cos(ang), r * np.sin(ang), 0]))
    base = VMobject().set_points_smoothly(pts)
    ring = DashedVMobject(base, num_dashes=n_dashes, dashed_ratio=0.55)
    ring.set_stroke(color, width=width)
    return ring


def planet_on_ring(center, ring_r, angle, **kw):
    center = np.array(center, dtype=float)
    p = center + np.array([ring_r * np.cos(angle), ring_r * np.sin(angle), 0])
    return make_planet(p, **kw)


# ----------------------------------------------------------------------
# Radius line from a center out to a point on the ring (the measurable r).
# ----------------------------------------------------------------------
def radius_line(center, angle, r, color=CHALK, width=4):
    center = np.array(center, dtype=float)
    end = center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
    return Line(center, end, color=color, stroke_width=width)


# ----------------------------------------------------------------------
# A small clock that "fills" to represent a year T. Returns a VGroup with
# .face, .rim, .wedge (the filled sector) and a helper to set the fill.
# ----------------------------------------------------------------------
def make_clock(pos=ORIGIN, r=0.55, color=CLOCKFACE, rim=CLOCKRIM):
    rim_c = Circle(radius=r, stroke_color=rim, stroke_width=3,
                   fill_color=VOID, fill_opacity=1)
    # tick marks
    ticks = VGroup()
    for k in range(12):
        ang = PI / 2 - 2 * np.pi * k / 12
        outer = np.array([np.cos(ang), np.sin(ang), 0]) * r
        inner = np.array([np.cos(ang), np.sin(ang), 0]) * (r * 0.84)
        ticks.add(Line(inner, outer, color=rim, stroke_width=2))
    hub = Dot(ORIGIN, radius=0.04, color=color)
    g = VGroup(rim_c, ticks, hub).move_to(pos)
    g.center_pt = np.array(pos, dtype=float)
    g.radius = r
    g.fill_color = color
    return g


def clock_wedge(clock, frac, color=None):
    """A filled pie sector covering `frac` (0..1) of the clock, starting
    from 12 o'clock and sweeping clockwise."""
    if color is None:
        color = clock.fill_color
    frac = float(np.clip(frac, 0.0, 1.0))
    c = clock.center_pt
    r = clock.radius * 0.92
    if frac <= 0.0:
        return VGroup()
    start = PI / 2
    n = max(2, int(64 * frac))
    pts = [c]
    for i in range(n + 1):
        ang = start - 2 * np.pi * frac * (i / n)
        pts.append(c + np.array([r * np.cos(ang), r * np.sin(ang), 0]))
    wedge = Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.65)
    return wedge


# ----------------------------------------------------------------------
# A clock hand pointing at a given fraction of a full turn.
# ----------------------------------------------------------------------
def clock_hand(clock, frac, color=CHALK, width=3):
    c = clock.center_pt
    r = clock.radius * 0.78
    ang = PI / 2 - 2 * np.pi * float(frac)
    end = c + np.array([r * np.cos(ang), r * np.sin(ang), 0])
    return Line(c, end, color=color, stroke_width=width)


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
# The equation scoreboard — Kepler's third law, built so individual parts
# can be colored/animated by isolation index. We use a single MathTex with
# substring isolation so r, T and subscripts can each be recolored.
#
# Layout (on the RIGHT half), assembled at b10:
#     ( r_A / r_B )^3  =  ( T_A / T_B )^2
#
# We expose:
#   eq.r_terms  -> the two r glyphs
#   eq.t_terms  -> the two T glyphs
#   eq.subA     -> the two 'A' subscripts
#   eq.subB     -> the two 'B' subscripts
#   eq.cube     -> the ^3 exponent
#   eq.square   -> the ^2 exponent
#   eq.lhs      -> whole left side group
#   eq.rhs      -> whole right side group
#   eq.eqsign   -> the '='
# ----------------------------------------------------------------------
def make_equation(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"\left(", r"\frac{r_A}{r_B}", r"\right)", r"^{3}",
        r"=",
        r"\left(", r"\frac{T_A}{T_B}", r"\right)", r"^{2}",
        substrings_to_isolate=["r_A", "r_B", "T_A", "T_B", "A", "B"],
    )
    eq.set_color(CHALK)
    eq.scale(scale)
    eq.move_to(pos)
    # Stable top-level submobject layout (verified):
    #   0 \left(  1 r_A/r_B  2 \right)  3 ^3  4 =
    #   5 \left(  6 T_A/T_B  7 \right)  8 ^2
    eq.lp_l   = eq[0]      # left "("
    eq.rfrac  = eq[1]      # the r_A/r_B fraction
    eq.rp_l   = eq[2]      # left ")"
    eq.cube   = eq[3]      # ^3
    eq.eqsign = eq[4]      # =
    eq.lp_r   = eq[5]      # right "("
    eq.tfrac  = eq[6]      # the T_A/T_B fraction
    eq.rp_r   = eq[7]      # right ")"
    eq.square = eq[8]      # ^2
    eq.lhs    = VGroup(eq[0], eq[1], eq[2])           # (r_A/r_B) without ^3
    eq.rhs    = VGroup(eq[5], eq[6], eq[7])           # (T_A/T_B) without ^2
    return eq


# Convenience: get the slot mobjects by searching the tex strings.
def eq_part(eq, tex):
    try:
        return eq.get_part_by_tex(tex)
    except Exception:
        return None
