"""Helpers for the surface-gravity (surfaceg) explainer.

The video holds a SPLIT FRAME throughout: the physical world (a person on
the Earth) on the LEFT, the equation as a scoreboard that fills in on the
RIGHT. The equation begins as

    m g = G * (m m_E) / r_E^2

and after the m's cancel becomes

    g = G * m_E / r_E^2

Visual contract (shared with the gravity series):
- Pure #000000 void background. Don't change it.
- font="sans" for ANY Text (Manim's default fallback collapses kerning).
- Color-binding: when a parameter is explained, the symbol in the equation
  AND its object on the LEFT glow the SAME color (RED).
- b8 reuses grav_helpers.make_fabric_3d for the curved-space "bend" callback.

This file owns surfaceg-only primitives. Don't pollute grav_helpers.py.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Palette --------------------------------------------------------------
RED      = "#E04848"   # the "glow" / binding color for an explained term
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary text/guides
FAINT    = "#5A5446"   # faintest guide lines
EARTH    = "#2A6BB5"   # earth blue
EARTH_D  = "#1A4885"
EARTH_G  = "#3A8B30"   # earth green land
MOON     = "#B8B8B8"   # moon grey
MOON_D   = "#7C7C7C"
SKIN     = "#D8B48C"
SHIRT    = "#5B9BD5"


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
# A small stick-figure person. Returns a VGroup; `feet` is its base point.
# ----------------------------------------------------------------------
def make_person(pos=ORIGIN, scale=1.0, color=CHALK):
    g = VGroup()
    head = Circle(radius=0.14, fill_color=SKIN, fill_opacity=1,
                  stroke_color=color, stroke_width=2).move_to([0, 0.78, 0])
    body = Line([0, 0.62, 0], [0, 0.18, 0], color=color, stroke_width=5)
    arm_l = Line([0, 0.52, 0], [-0.22, 0.30, 0], color=color, stroke_width=4)
    arm_r = Line([0, 0.52, 0], [0.22, 0.30, 0], color=color, stroke_width=4)
    leg_l = Line([0, 0.18, 0], [-0.16, -0.10, 0], color=color, stroke_width=4)
    leg_r = Line([0, 0.18, 0], [0.16, -0.10, 0], color=color, stroke_width=4)
    g.add(body, arm_l, arm_r, leg_l, leg_r, head)
    g.scale(scale).move_to(pos)
    g.feet = g.get_bottom()
    return g


# ----------------------------------------------------------------------
# A planet body (earth or moon style) with land splotches + highlight.
# Returns a VGroup; `.body` is the outer circle for easy recolor.
# ----------------------------------------------------------------------
def make_world(pos=ORIGIN, r=0.95, kind="earth"):
    if kind == "earth":
        fill, edge, land = EARTH, EARTH_D, EARTH_G
    else:
        fill, edge, land = MOON, MOON_D, "#9A9A9A"
    body = Circle(radius=r, fill_color=fill, fill_opacity=1,
                  stroke_color=edge, stroke_width=2.5)
    feats = VGroup()
    splotches = [(-0.32, 0.18, 0.26), (0.30, -0.22, 0.20),
                 (0.12, 0.40, 0.15), (-0.18, -0.36, 0.18)]
    for dx, dy, rr in splotches:
        feats.add(Circle(radius=rr * r, fill_color=land, fill_opacity=1,
                         stroke_width=0).shift([dx * r, dy * r, 0]))
    hl = Ellipse(width=0.5 * r, height=0.28 * r, fill_color=WHITE,
                 fill_opacity=0.22, stroke_width=0
                 ).shift([-0.34 * r, 0.36 * r, 0])
    g = VGroup(body, feats, hl).move_to(pos)
    g.body = body
    g.center_pt = np.array(pos, dtype=float)
    g.radius = r
    return g


# ----------------------------------------------------------------------
# A radius line from a world's center to its surface.
# ----------------------------------------------------------------------
def radius_line(world, angle=PI / 2, color=CHALK, width=4):
    c = world.center_pt
    end = c + np.array([world.radius * np.cos(angle),
                        world.radius * np.sin(angle), 0])
    return Line(c, end, color=color, stroke_width=width)


# ----------------------------------------------------------------------
# A feather (light) and a hammer (heavy) — used in the b4 cancellation.
# ----------------------------------------------------------------------
def make_feather(pos=ORIGIN, scale=1.0, color="#D8E0EE"):
    spine = Line([0, 0.35, 0], [0, -0.35, 0], color=color, stroke_width=3)
    barbs = VGroup()
    for t in np.linspace(0.1, 0.9, 7):
        y = 0.35 - 0.70 * t
        w = 0.18 * np.sin(np.pi * t)
        barbs.add(Line([0, y, 0], [-w, y + 0.06, 0], color=color,
                       stroke_width=2))
        barbs.add(Line([0, y, 0], [w, y + 0.06, 0], color=color,
                       stroke_width=2))
    g = VGroup(spine, barbs).scale(scale).move_to(pos)
    return g


def make_hammer(pos=ORIGIN, scale=1.0):
    handle = Rectangle(width=0.08, height=0.55, fill_color="#9A6B3A",
                       fill_opacity=1, stroke_width=0).shift([0, -0.12, 0])
    head = Rectangle(width=0.38, height=0.20, fill_color="#8C8C8C",
                     fill_opacity=1, stroke_color="#5A5A5A",
                     stroke_width=2).shift([0, 0.22, 0])
    g = VGroup(handle, head).scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# The equation scoreboard.
#
# Initial form (b3):   m g = G \frac{m\, m_E}{r_E^{2}}
# Final form  (b5+):   g = G \frac{m_E}{r_E^{2}}
#
# We build TWO MathTex objects with isolated substrings so the m's can be
# struck/cancelled (b4) and the symbols color-bound (b5..b9).
#
# make_equation_full() -> the m g = G m m_E / r_E^2 form
#   .mg_m   -> the left-side 'm' (in m g)
#   .g      -> the left-side 'g'
#   .G      -> big G
#   .num_m  -> the numerator 'm'
#   .m_E    -> the m_E in numerator
#   .r_E    -> the r_E base in denominator
#
# make_equation_reduced() -> the g = G m_E / r_E^2 form (post-cancellation)
#   .g, .G, .m_E, .r_E exposed similarly.
# ----------------------------------------------------------------------
def make_equation_full(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"m", r"g", r"=", r"G", r"\frac{m\,m_E}{r_E^{2}}",
        substrings_to_isolate=["m_E", "r_E"],
    )
    eq.set_color(CHALK)
    eq.scale(scale).move_to(pos)
    return eq


def make_equation_reduced(pos=ORIGIN, scale=1.0):
    eq = MathTex(
        r"g", r"=", r"G", r"\frac{m_E}{r_E^{2}}",
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
