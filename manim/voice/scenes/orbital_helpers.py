"""Helpers for the Orbital Period / Kepler's Third Law (orbital) explainer.

The video holds a SPLIT FRAME throughout: the orbital world on the LEFT,
the period equation as a scoreboard that fills in on the RIGHT. The
equation is

    T = 2 pi sqrt( r^3 / (G m_s) )

derived at b4-b5 (gravity = centripetal, the planet's mass m_p cancels) and
fully assembled at b8.

Visual contract (shared with the gravity series):
- Pure #000000 void background. Don't change it.
- font="sans" for ANY Text (Manim's default fallback collapses kerning).
- Color-binding: when a parameter is explained, the symbol in the equation
  AND its object on the LEFT glow the SAME color (RED).
- b9-b10 reuse grav_helpers.make_fabric_3d for the curved-space "bend"
  callback (and ghost in kepler3's T^2 ~ r^3 form).

This file owns orbital-only primitives. Don't pollute grav_helpers.py.
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
PLANET   = "#5B9BD5"   # the planet — blue
PLANET_D = "#3A6E9E"
ORBITCOL = "#9AA8C0"
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


def make_planet(pos=ORIGIN, r=0.18, color=PLANET, edge=PLANET_D):
    return Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=edge, stroke_width=2).move_to(pos)


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


def radius_line(center, angle, r, color=CHALK, width=4):
    center = np.array(center, dtype=float)
    end = center + np.array([r * np.cos(angle), r * np.sin(angle), 0])
    return Line(center, end, color=color, stroke_width=width)


def planet_at(center, r, frac):
    """Planet position at fraction `frac` of one orbit (from 12 o'clock,
    clockwise)."""
    center = np.array(center, dtype=float)
    ang = PI / 2 - 2 * np.pi * frac
    return center + np.array([r * np.cos(ang), r * np.sin(ang), 0])


# ----------------------------------------------------------------------
# Clock that "fills" to represent a year T.
# ----------------------------------------------------------------------
def make_clock(pos=ORIGIN, r=0.55, color=CLOCKFACE, rim=CLOCKRIM):
    rim_c = Circle(radius=r, stroke_color=rim, stroke_width=3,
                   fill_color=VOID, fill_opacity=1)
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
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=0.65)


def clock_hand(clock, frac, color=CHALK, width=3):
    c = clock.center_pt
    r = clock.radius * 0.78
    ang = PI / 2 - 2 * np.pi * float(frac)
    end = c + np.array([r * np.cos(ang), r * np.sin(ang), 0])
    return Line(c, end, color=color, stroke_width=width)


# ----------------------------------------------------------------------
# Text helpers (always font="sans").
# ----------------------------------------------------------------------
def label(text, pos=ORIGIN, size=28, color=CHALK, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=64, color=DIM, opacity=0.7):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def divider(x=0.4):
    return Line([x, -3.6, 0], [x, 3.6, 0], color=FAINT, stroke_width=1.5
                ).set_opacity(0.5)


# ----------------------------------------------------------------------
# The period equation scoreboard:  T = 2 pi sqrt( r^3 / (G m_s) )
#
# We avoid substrings_to_isolate (it breaks \sqrt/\frac by isolating bare
# letters inside the control sequences). Instead the inner pieces are
# their own MathTex args.
#
# Exposed handles:
#   eq.T      -> T
#   eq.eqsign -> =
#   eq.coeff  -> 2 pi
#   eq.radsym -> the \sqrt sign + delimiters (the radical)
#   eq.rcube  -> r^3 (numerator)
#   eq.bar    -> fraction bar
#   eq.denom  -> G m_s (denominator)
#   eq.G      -> the G glyph in the denominator
#   eq.ms     -> the m_s glyph in the denominator
# ----------------------------------------------------------------------
def make_equation(pos=ORIGIN, scale=1.0):
    # Build the radical as ONE tex over the whole fraction so it spans
    # correctly, but keep the fraction pieces as separately addressable
    # args by reaching into the radical's submobject.
    #   layout: 0 T  1 =  2 2pi  3 sqrt{ r^3 / (G m_s) }
    eq = MathTex(
        r"T", r"=", r"2\pi",
        r"\sqrt{ {r^3 \over G\,m_s} }",
    )
    eq.set_color(CHALK)
    eq.scale(scale)
    eq.move_to(pos)
    eq.T      = eq[0]
    eq.eqsign = eq[1]
    eq.coeff  = eq[2]
    rad = eq[3]
    # rad glyphs (verified count 8 by position):
    #   [0]=sqrt sign, [1]=sqrt vinculum, [2]=r, [3]=exponent 3,
    #   [4]=fraction bar, [5]=G, [6]=m, [7]=subscript s
    eq.radsym = VGroup(rad[0], rad[1])
    eq.rcube  = rad[2:4]      # r and the exponent 3
    eq.bar    = rad[4]
    eq.G      = rad[5]
    eq.ms     = rad[6:8]      # m and subscript s
    eq.denom  = rad[5:8]
    eq.frac   = rad[2:8]
    return eq


# A cleaner single-string period equation for the assembled / final beats,
# where the radical correctly spans the fraction. Returns a MathTex with
# named .parts via index after a verified layout.
def make_equation_full(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"T", r"=", r"2\pi",
        r"\sqrt{\dfrac{r^3}{G\,m_s}}",
    )
    eq.set_color(CHALK)
    eq.scale(scale)
    eq.move_to(pos)
    eq.T      = eq[0]
    eq.eqsign = eq[1]
    eq.coeff  = eq[2]
    eq.rad    = eq[3]         # whole radical (sqrt + r^3/(G m_s))
    return eq


# The force-balance form for b4:  F_grav = F_centripetal
#   G m_s m_p / r^2  =  m_p v^2 / r
def make_balance(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"{G\,m_s\,m_p", r"\over", r"r^2}",
        r"=",
        r"{m_p\,v^2", r"\over", r"r}",
    )
    eq.set_color(CHALK)
    eq.scale(scale)
    eq.move_to(pos)
    # left numerator G m_s m_p ; left denom r^2 ; = ; right num m_p v^2 ; right denom r
    eq.lnum   = eq[0]
    eq.lbar   = eq[1]
    eq.ldenom = eq[2]
    eq.eqsign = eq[3]
    eq.rnum   = eq[4]
    eq.rbar   = eq[5]
    eq.rdenom = eq[6]
    # m_p appears in lnum (last 2 glyphs) and rnum (first 2 glyphs)
    eq.mp_left  = eq[0][-2:]    # m_p on the left
    eq.mp_right = eq[4][0:2]    # m_p on the right
    return eq
