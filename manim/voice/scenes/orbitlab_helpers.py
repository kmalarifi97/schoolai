"""Helpers for the Build a Stable Orbit (orbitlab) project-story.

A narrative: Sami trying to make a moon circle his planet exactly once.
It spirals in, flies off, sags and crashes. He rebuilds it in PhET
Gravity and Orbits, predicts-then-runs, then the ending calls back to
three earlier concept videos (two rocks pulling, Earth's field arrows,
a ball thrown so fast it never lands).

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Calm, low-key palette — deep space, cool stone, faint glows. No hype.
PLANET   = "#6E8C9B"   # the planet body (cool slate-blue)
PLANET_D = "#4A6470"   # planet terminator / edge
MOON     = "#C9C2B2"   # the moon (pale stone)
MOON_D   = "#8C8576"   # moon shadow
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary
FAINT    = "#5A5446"   # faintest guide lines
IDEAL    = "#7FB8E8"   # the hoped-for circle (cool, calm)
PULL     = "#D98C5F"   # gravity / inward pull (warm)
STRAIGHT = "#E8C46B"   # straight-line tendency (gold)
TRACE    = "#9BD6B0"   # path trace (soft green)
FAIL     = "#C98A6B"   # a failed attempt arc (warm)
STAR     = "#E8C46B"   # the PhET star
ROCK_A   = "#C9A66B"   # callback rock (big)
ROCK_B   = "#A88B57"   # callback rock (small)
EARTH    = "#7FB8E8"   # callback Earth


# ----------------------------------------------------------------------
# The planet — a quiet body, center of the story.
# ----------------------------------------------------------------------
def make_planet(pos=ORIGIN, r=0.85, color=PLANET):
    body = Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=PLANET_D, stroke_width=2)
    # a soft terminator arc for a touch of dimension
    term = Arc(radius=r * 0.96, start_angle=PI * 0.35,
               angle=PI * 0.95, color=PLANET_D, stroke_width=2
               ).set_opacity(0.5)
    g = VGroup(body, term).move_to(pos)
    g.body = body
    g.planet_r = r
    return g


# ----------------------------------------------------------------------
# The moon — a small pale dot the story moves around.
# ----------------------------------------------------------------------
def make_moon(pos=ORIGIN, r=0.16, color=MOON):
    d = Circle(radius=r, fill_color=color, fill_opacity=1,
               stroke_color=MOON_D, stroke_width=1.5)
    d.move_to(pos)
    return d


def moon_dot(pos, color=MOON, r=0.13):
    """The moon as a single quiet dot (for path animation)."""
    return Dot(point=pos, radius=r, color=color)


# ----------------------------------------------------------------------
# Inward gravity-force arrow: from the moon, straight toward the planet
# center. Redrawable wherever the moon is.
# ----------------------------------------------------------------------
def gravity_arrow(moon_pos, planet_pos, length=0.95, color=PULL):
    moon_pos = np.array(moon_pos, dtype=float)
    planet_pos = np.array(planet_pos, dtype=float)
    d = planet_pos - moon_pos
    n = np.linalg.norm(d)
    if n < 1e-6:
        d = np.array([-1.0, 0.0, 0.0]); n = 1.0
    u = d / n
    start = moon_pos
    end = moon_pos + u * length
    return Arrow(start, end, color=color, stroke_width=5, buff=0.0,
                 max_tip_length_to_length_ratio=0.32,
                 max_stroke_width_to_length_ratio=8)


# ----------------------------------------------------------------------
# Straight-line tendency arrow: the moon "wants to keep going straight"
# along its current velocity direction (tangent).
# ----------------------------------------------------------------------
def straight_arrow(moon_pos, direction, length=1.05, color=STRAIGHT):
    moon_pos = np.array(moon_pos, dtype=float)
    direction = np.array(direction, dtype=float)
    n = np.linalg.norm(direction)
    if n < 1e-6:
        direction = np.array([0.0, 1.0, 0.0]); n = 1.0
    u = direction / n
    start = moon_pos
    end = moon_pos + u * length
    return Arrow(start, end, color=color, stroke_width=5, buff=0.0,
                 max_tip_length_to_length_ratio=0.30,
                 max_stroke_width_to_length_ratio=8)


# ----------------------------------------------------------------------
# Path families, all around a center.
#   spiral_in   : decaying radius, ends at the planet (too slow)
#   closed_circle : a clean closed lap (matched)
#   escape_path : opens out and leaves the frame (too fast)
# Each returns a VMobject path.
# ----------------------------------------------------------------------
def spiral_in_path(center, r0=2.6, turns=1.6, r_end=0.85, n=160,
                    color=FAIL, width=4, start_angle=PI / 2):
    center = np.array(center, dtype=float)
    pts = []
    total = turns * 2 * np.pi
    for i in range(n + 1):
        t = i / n
        ang = start_angle - total * t
        r = r0 + (r_end - r0) * t
        pts.append(center + np.array([r * np.cos(ang),
                                      r * np.sin(ang), 0]))
    path = VMobject().set_points_smoothly(pts)
    path.set_stroke(color, width=width)
    return path


def closed_circle_path(center, r=1.9, n=120, color=TRACE, width=4,
                       start_angle=PI / 2):
    center = np.array(center, dtype=float)
    pts = []
    for i in range(n + 1):
        ang = start_angle - 2 * np.pi * (i / n)
        pts.append(center + np.array([r * np.cos(ang),
                                      r * np.sin(ang), 0]))
    path = VMobject().set_points_smoothly(pts)
    path.set_stroke(color, width=width)
    return path


def escape_path(center, r0=1.7, n=120, color=FAIL, width=4,
                start_angle=PI / 2, open_rate=2.4):
    """Curves once near the planet then straightens out and leaves."""
    center = np.array(center, dtype=float)
    pts = []
    for i in range(n + 1):
        t = i / n
        ang = start_angle - 1.3 * np.pi * t
        r = r0 * (1.0 + open_rate * t * t)
        pts.append(center + np.array([r * np.cos(ang),
                                      r * np.sin(ang), 0]))
    path = VMobject().set_points_smoothly(pts)
    path.set_stroke(color, width=width)
    return path


def radial_fall_path(start, center, planet_r=0.85, n=40, color=FAIL,
                      width=4):
    """Straight radial drop from start onto the planet surface."""
    start = np.array(start, dtype=float)
    center = np.array(center, dtype=float)
    d = center - start
    nrm = np.linalg.norm(d)
    u = d / nrm
    end = center - u * planet_r
    pts = [start + (end - start) * (i / n) for i in range(n + 1)]
    path = VMobject().set_points_as_corners(pts)
    path.set_stroke(color, width=width)
    return path


def dotted_circle(center, r=1.9, color=IDEAL, width=3, n=120):
    """The calm dotted hoped-for circle."""
    base = closed_circle_path(center, r=r, n=n, color=color,
                              width=width)
    return DashedVMobject(base, num_dashes=40, dashed_ratio=0.55
                          ).set_stroke(color, width=width)


def ellipse_path(center, a=2.4, b=1.4, n=120, color=FAIL, width=4,
                 phase=0.0):
    """An egg-shaped (elliptical) attempt."""
    center = np.array(center, dtype=float)
    pts = []
    for i in range(n + 1):
        ang = phase + 2 * np.pi * (i / n)
        pts.append(center + np.array([a * np.cos(ang),
                                      b * np.sin(ang), 0]))
    path = VMobject().set_points_smoothly(pts)
    path.set_stroke(color, width=width)
    return path


def trace_dot(pos, color=MOON, r=0.11):
    return Dot(point=pos, radius=r, color=color)


# ----------------------------------------------------------------------
# Ball-on-curved-ground inset: a ball thrown along a curving surface,
# the arc closing back into an orbit (the "never lands" idea).
# Returns a VGroup; .arc is the ball's arc path.
# ----------------------------------------------------------------------
def curved_ground_inset(pos=ORIGIN, scale=1.0):
    R = 1.5
    ground = Arc(radius=R, start_angle=PI * 0.20, angle=PI * 0.60,
                 color=DIM, stroke_width=3).set_opacity(0.7)
    center = ground.get_arc_center()
    # the ball's flatter arc, departing the surface and curving with it
    pts = []
    for i in range(61):
        t = i / 60
        ang = PI * 0.80 - PI * 0.60 * t
        rr = R + 0.55 * np.sin(np.pi * t)   # rises off the ground
        pts.append(center + np.array([rr * np.cos(ang),
                                      rr * np.sin(ang), 0]))
    arc = VMobject().set_points_smoothly(pts)
    arc.set_stroke(STRAIGHT, width=4)
    ball = Dot(pts[0], radius=0.10, color=CHALK)
    g = VGroup(ground, arc, ball).scale(scale).move_to(pos)
    g.arc = arc
    g.ball = ball
    return g


# ----------------------------------------------------------------------
# PhET "Gravity and Orbits" layout: a star + a planet/body, a gravity
# force arrow, mass/distance controls, a path trace, play button,
# velocity control, run counter.
# ----------------------------------------------------------------------
def slider(pos=ORIGIN, frac=0.5, w=2.4, label="mass"):
    rail = Line(LEFT * w / 2, RIGHT * w / 2, color=DIM, stroke_width=3
                ).set_opacity(0.6)
    knob = Circle(radius=0.11, fill_color=CHALK, fill_opacity=1,
                  stroke_width=0)
    knob.move_to(LEFT * w / 2 + RIGHT * w * float(np.clip(frac, 0, 1)))
    grp = VGroup(rail, knob)
    lbl = Text(label, font="sans", font_size=18, color=DIM)
    lbl.next_to(grp, DOWN, buff=0.14)
    out = VGroup(grp, lbl).move_to(pos)
    out.knob = knob
    out.rail = rail
    return out


def gravity_orbits_panel(pos=ORIGIN, scale=1.0, body_angle=PI / 2,
                         orbit_r=1.7, with_trace=True):
    """Star at center, body on a ring, gravity arrow inward, plus a
    drawn partial trace. Controls live separately (see make_controls)."""
    star = VGroup(
        Circle(radius=0.40, fill_color=STAR, fill_opacity=1,
               stroke_width=0),
        Circle(radius=0.62, fill_color=STAR, fill_opacity=0.18,
               stroke_width=0))
    body_pos = np.array([orbit_r * np.cos(body_angle),
                         orbit_r * np.sin(body_angle), 0])
    body = Circle(radius=0.17, fill_color=PLANET, fill_opacity=1,
                  stroke_color=PLANET_D, stroke_width=1.5
                  ).move_to(body_pos)
    garrow = gravity_arrow(body_pos, ORIGIN, length=0.8, color=PULL)
    grp = VGroup(star, body, garrow)
    if with_trace:
        tr = closed_circle_path(ORIGIN, r=orbit_r, color=TRACE,
                                width=3)
        tr = DashedVMobject(tr, num_dashes=44, dashed_ratio=0.5
                            ).set_stroke(TRACE, width=3)
        grp.add(tr)
        grp.trace = tr
    grp.star = star
    grp.body = body
    grp.garrow = garrow
    grp.scale(scale).move_to(pos)
    return grp


def make_controls(pos=ORIGIN, scale=1.0):
    """Mass / mass / distance sliders stacked, PhET-style."""
    m1 = slider([0, 0.9, 0], frac=0.65, w=2.2, label="star mass")
    m2 = slider([0, 0.0, 0], frac=0.40, w=2.2, label="moon mass")
    dd = slider([0, -0.9, 0], frac=0.55, w=2.2, label="distance")
    frame = Rectangle(width=3.0, height=3.0, stroke_color=FAINT,
                      stroke_width=1.5, fill_opacity=0)
    frame.set_stroke(FAINT, opacity=0.5)
    g = VGroup(frame, m1, m2, dd)
    g.scale(scale).move_to(pos)
    g.m1, g.m2, g.dd = m1, m2, dd
    return g


def play_button(pos=ORIGIN, r=0.42, color=CHALK):
    circ = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    tri.scale(r * 0.55).rotate(-PI / 2)
    tri.move_to(circ.get_center() + RIGHT * r * 0.08)
    return VGroup(circ, tri).move_to(pos)


def velocity_control(pos=ORIGIN, frac=0.5, w=2.8):
    return slider(pos=pos, frac=frac, w=w, label="launch speed")


def run_counter(pos=ORIGIN, used=0, total=3):
    g = VGroup()
    for k in range(total):
        d = Circle(radius=0.12,
                   fill_color=(CHALK if k < used else VOID),
                   fill_opacity=(1 if k < used else 0),
                   stroke_color=DIM, stroke_width=2)
        d.move_to([k * 0.42, 0, 0])
        g.add(d)
    lbl = Text(f"{total} runs", font="sans", font_size=20, color=DIM)
    lbl.next_to(g, DOWN, buff=0.16)
    return VGroup(g, lbl).move_to(pos)


# ----------------------------------------------------------------------
# The three faint callback icons — must echo the concept-video imagery.
#   rocks : two rocks with a force line (gravitation video)
#   field : Earth with radial field arrows crowding inward (gfield)
#   thrown: a ball's arc closing into an orbit around Earth (weightless)
# Faint by default: they flicker in the void as memories.
# ----------------------------------------------------------------------
def callback_rocks(pos=ORIGIN, scale=1.0, opacity=0.85):
    big = Circle(radius=0.34, fill_color=ROCK_A, fill_opacity=1,
                 stroke_color=DIM, stroke_width=1.5)
    big.move_to(LEFT * 1.1)
    small = Circle(radius=0.21, fill_color=ROCK_B, fill_opacity=1,
                   stroke_color=DIM, stroke_width=1.5)
    small.move_to(RIGHT * 1.1)
    a1 = Arrow(big.get_right(), big.get_right() + RIGHT * 0.55,
               color=PULL, stroke_width=4, buff=0.05,
               max_tip_length_to_length_ratio=0.4)
    a2 = Arrow(small.get_left(), small.get_left() + LEFT * 0.55,
               color=PULL, stroke_width=4, buff=0.05,
               max_tip_length_to_length_ratio=0.4)
    line = DashedLine(big.get_center(), small.get_center(),
                      color=FAINT, stroke_width=2).set_opacity(0.6)
    g = VGroup(line, big, small, a1, a2).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_field(pos=ORIGIN, scale=1.0, opacity=0.85):
    earth = Circle(radius=0.46, fill_color=EARTH, fill_opacity=1,
                   stroke_color=PLANET_D, stroke_width=1.5)
    arrows = VGroup()
    for k in range(12):
        ang = 2 * np.pi * k / 12
        outer = np.array([np.cos(ang), np.sin(ang), 0]) * 1.45
        inner = np.array([np.cos(ang), np.sin(ang), 0]) * 0.60
        arrows.add(Arrow(outer, inner, color=PULL, stroke_width=3,
                         buff=0.0,
                         max_tip_length_to_length_ratio=0.35))
    g = VGroup(arrows, earth).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_thrown(pos=ORIGIN, scale=1.0, opacity=0.85):
    earth = Circle(radius=0.34, fill_color=EARTH, fill_opacity=1,
                   stroke_color=PLANET_D, stroke_width=1.5)
    # a ball thrown from the surface, its arc curving around and
    # closing into an orbit clearly outside the Earth
    orbit_r = 1.30
    pts = []
    for i in range(81):
        t = i / 80
        ang = PI / 2 - 2 * np.pi * t
        pts.append(np.array([orbit_r * np.cos(ang),
                             orbit_r * np.sin(ang), 0]))
    arc = VMobject().set_points_smoothly(pts)
    # stroke-only: never let this closed path take a fill (a closed
    # VMobject with set_opacity fills like a disc — documented gotcha)
    arc.set_fill(opacity=0).set_stroke(STRAIGHT, width=4,
                                       opacity=opacity)
    ball = Dot(pts[0], radius=0.10, color=CHALK)
    earth.set_opacity(opacity)
    ball.set_opacity(opacity)
    g = VGroup(earth, arc, ball).scale(scale).move_to(pos)
    g.arc = arc
    g.ball = ball
    g._cb_opacity = opacity
    return g


def small_label(text, pos, color=CHALK, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=48, color=DIM, opacity=0.6):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
