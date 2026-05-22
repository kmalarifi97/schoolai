"""Helpers for the weigh-the-Earth (weighearth) explainer.

The video holds a SPLIT FRAME throughout: the physical world (the Earth, a
scale, the Cavendish apparatus) on the LEFT, the equation as a scoreboard
on the RIGHT. The equation begins as

    g = G * m_E / r_E^2

and is rearranged to isolate the Earth's mass:

    m_E = g * r_E^2 / G

Visual contract (shared with the gravity series):
- Pure #000000 void background. Don't change it.
- font="sans" for ANY Text (Manim's default fallback collapses kerning).
- Color-binding: when a parameter is explained, the symbol in the equation
  AND its object on the LEFT glow the SAME color (RED).
- b8 reuses grav_helpers.make_fabric_3d for the curved-space "bend" callback,
  with the Earth now labeled by its mass.

This file owns weighearth-only primitives. Don't pollute grav_helpers.py.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Palette --------------------------------------------------------------
RED      = "#E04848"   # the "glow" / binding color for an explained term
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary text/guides
FAINT    = "#5A5446"   # faintest guide lines
EARTH    = "#2A6BB5"
EARTH_D  = "#1A4885"
EARTH_G  = "#3A8B30"
SUN_CORE = "#FFF4D6"
BRASS    = "#C9A24B"
STEEL    = "#9AA8C0"


# ----------------------------------------------------------------------
# Text label helper (always font="sans").
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
# An Earth body with land splotches + highlight. `.body` is the outer circle.
# ----------------------------------------------------------------------
def make_earth(pos=ORIGIN, r=0.95):
    body = Circle(radius=r, fill_color=EARTH, fill_opacity=1,
                  stroke_color=EARTH_D, stroke_width=2.5)
    feats = VGroup()
    for dx, dy, rr in [(-0.32, 0.18, 0.26), (0.30, -0.22, 0.20),
                       (0.12, 0.40, 0.15), (-0.18, -0.36, 0.18)]:
        feats.add(Circle(radius=rr * r, fill_color=EARTH_G, fill_opacity=1,
                         stroke_width=0).shift([dx * r, dy * r, 0]))
    hl = Ellipse(width=0.5 * r, height=0.28 * r, fill_color=WHITE,
                 fill_opacity=0.22, stroke_width=0
                 ).shift([-0.34 * r, 0.36 * r, 0])
    g = VGroup(body, feats, hl).move_to(pos)
    g.body = body
    g.center_pt = np.array(pos, dtype=float)
    g.radius = r
    return g


def radius_line(earth, angle=-PI / 4, color=CHALK, width=4):
    c = earth.center_pt
    end = c + np.array([earth.radius * np.cos(angle),
                        earth.radius * np.sin(angle), 0])
    return Line(c, end, color=color, stroke_width=width)


# ----------------------------------------------------------------------
# Sun — soft layered glow.
# ----------------------------------------------------------------------
def make_sun(pos=ORIGIN, scale=1.0):
    g = VGroup()
    for r, op in [(0.85, 0.04), (0.65, 0.08), (0.45, 0.18), (0.30, 0.50)]:
        g.add(Circle(radius=r, color=SUN_CORE, fill_color=SUN_CORE,
                     fill_opacity=op, stroke_width=0))
    g.add(Circle(radius=0.16, color=WHITE, fill_color=WHITE,
                 fill_opacity=1.0, stroke_width=0))
    return g.scale(scale).move_to(pos)


def make_planet(pos=ORIGIN, r=0.18, color=STEEL, edge="#5E6B82"):
    return Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=edge, stroke_width=2).move_to(pos)


# ----------------------------------------------------------------------
# A balance scale (used for the "you can't weigh the Earth" beat). Returns
# a VGroup with .left_pan and .right_pan exposed.
# ----------------------------------------------------------------------
def make_scale(pos=ORIGIN, scale=1.0, tilt=0.0):
    base = Line([0, -1.0, 0], [0, 0.6, 0], color=STEEL, stroke_width=5)
    stand = Line([-0.5, -1.0, 0], [0.5, -1.0, 0], color=STEEL,
                 stroke_width=5)
    beam = Line([-1.1, 0.6, 0], [1.1, 0.6, 0], color=STEEL, stroke_width=5)
    beam.rotate(tilt, about_point=np.array([0, 0.6, 0]))
    lp_anchor = beam.get_start()
    rp_anchor = beam.get_end()

    def pan(anchor):
        cup = Arc(radius=0.32, start_angle=PI, angle=PI, color=STEEL,
                  stroke_width=3)
        cup.move_to(anchor + np.array([0, -0.55, 0]))
        h1 = Line(anchor, cup.get_left(), color=STEEL, stroke_width=2)
        h2 = Line(anchor, cup.get_right(), color=STEEL, stroke_width=2)
        return VGroup(h1, h2, cup)
    left_pan = pan(lp_anchor)
    right_pan = pan(rp_anchor)
    g = VGroup(stand, base, beam, left_pan, right_pan).scale(scale).move_to(pos)
    g.left_pan = left_pan
    g.right_pan = right_pan
    return g


# ----------------------------------------------------------------------
# Cavendish torsion balance: two small masses on a horizontal rod hung from
# a fiber, with two large masses nearby. Schematic but readable.
# ----------------------------------------------------------------------
def make_cavendish(pos=ORIGIN, scale=1.0):
    fiber = Line([0, 1.2, 0], [0, 0.2, 0], color=DIM, stroke_width=1.5)
    support = Line([-0.7, 1.2, 0], [0.7, 1.2, 0], color=STEEL, stroke_width=4)
    rod = Line([-0.9, 0.2, 0], [0.9, 0.2, 0], color=STEEL, stroke_width=3)
    small_l = Circle(radius=0.10, fill_color=STEEL, fill_opacity=1,
                     stroke_width=0).move_to([-0.9, 0.2, 0])
    small_r = Circle(radius=0.10, fill_color=STEEL, fill_opacity=1,
                     stroke_width=0).move_to([0.9, 0.2, 0])
    big_l = Circle(radius=0.20, fill_color=BRASS, fill_opacity=1,
                   stroke_color="#8C6F2E", stroke_width=2).move_to([-1.25, -0.1, 0])
    big_r = Circle(radius=0.20, fill_color=BRASS, fill_opacity=1,
                   stroke_color="#8C6F2E", stroke_width=2).move_to([1.25, 0.5, 0])
    g = VGroup(support, fiber, rod, small_l, small_r, big_l, big_r)
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# A simple stone (for the "drop a stone" g-measurement).
# ----------------------------------------------------------------------
def make_stone(pos=ORIGIN, r=0.13):
    return Circle(radius=r, fill_color="#6E6E6E", fill_opacity=1,
                  stroke_color="#4A4A4A", stroke_width=2).move_to(pos)


# ----------------------------------------------------------------------
# The equation scoreboard.
#
# Start form (b1):   g = G \frac{m_E}{r_E^{2}}
# Target form (b4+): m_E = \frac{g\, r_E^{2}}{G}
#
# make_equation_g()   -> g = G m_E / r_E^2
# make_equation_mE()  -> m_E = g r_E^2 / G
# Both isolate "m_E" and "r_E" for color-binding via get_part_by_tex.
# ----------------------------------------------------------------------
def make_equation_g(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"g", r"=", r"G", r"\frac{m_E}{r_E^{2}}",
        substrings_to_isolate=["m_E", "r_E"],
    )
    eq.set_color(CHALK)
    eq.scale(scale).move_to(pos)
    return eq


def make_equation_mE(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"m_E", r"=", r"\frac{g\,r_E^{2}}{G}",
        substrings_to_isolate=["m_E", "r_E"],
    )
    eq.set_color(CHALK)
    eq.scale(scale).move_to(pos)
    return eq


def part(eq, tex):
    try:
        return eq.get_part_by_tex(tex)
    except Exception:
        return None
