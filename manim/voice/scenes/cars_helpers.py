"""Helpers for the cars / v² (kinetic energy) scene."""

from manim import *
import numpy as np


VOID = "#000000"

# Palette
CAR_BODY     = "#C03C2C"
CAR_BODY_HI  = "#FF6A52"
CAR_DARK     = "#5C0F08"
CAR_GLASS    = "#7CC6FF"
WHEEL_BLACK  = "#101218"
WHEEL_RIM    = "#5C6068"
ROAD_GREY    = "#2A2D33"
ROAD_LINE    = "#E8DC52"
SKY_TINT     = "#0E1A2E"
WALL_GREY    = "#7C808A"
WALL_DARK    = "#3E4148"
PERSON_BODY  = "#3B6AB0"
PERSON_PANTS = "#262A33"
SKIN_TONE    = "#D5A887"
BAR_GREEN    = "#7FE08C"
BAR_RED      = "#FF5A4E"
BAR_BG       = "#22272E"
NEEDLE_RED   = "#D03A1B"
DIAL_BG      = "#1C1F26"
DIAL_RING    = "#7E8290"
DANGER_GLOW  = "#FF5A1A"
IMPACT_RED   = "#E04A2A"
BARRIER_GREY = "#9CA0A8"


# -----------------------------------------------------------------------------
# Car (side profile)
# -----------------------------------------------------------------------------

def make_car(center=np.array([0,0,0]), scale=1.0, body_color=CAR_BODY,
             flipped=False, crumple=0.0):
    """
    Simple side-view sedan.
    `crumple` ∈ [0, 1]: extent of front-end deformation.
    Front faces RIGHT by default; pass flipped=True for left-facing.
    """
    # Lower body (chassis)
    lower = RoundedRectangle(width=2.6, height=0.55, corner_radius=0.10,
                             fill_color=body_color, fill_opacity=1,
                             stroke_color=CAR_DARK, stroke_width=1.6
                             ).shift(DOWN*0.35)
    # Upper body (cabin) — trapezoid
    cabin = Polygon(
        [-0.85, -0.10, 0], [-0.55, 0.45, 0],
        [ 0.55, 0.45, 0], [ 0.85, -0.10, 0],
        fill_color=body_color, fill_opacity=1,
        stroke_color=CAR_DARK, stroke_width=1.6,
    )
    # Windows
    win_l = Polygon(
        [-0.75, -0.05, 0], [-0.50, 0.38, 0],
        [-0.08, 0.38, 0], [-0.08, -0.05, 0],
        fill_color=CAR_GLASS, fill_opacity=0.9, stroke_width=0,
    )
    win_r = Polygon(
        [0.08, -0.05, 0], [0.08, 0.38, 0],
        [0.50, 0.38, 0], [0.75, -0.05, 0],
        fill_color=CAR_GLASS, fill_opacity=0.9, stroke_width=0,
    )
    # Highlight stripe
    hl = Rectangle(width=2.40, height=0.06,
                   fill_color=CAR_BODY_HI, fill_opacity=0.7,
                   stroke_width=0).shift(DOWN*0.22)
    # Headlight (front-right)
    headlight = Ellipse(width=0.16, height=0.10, fill_color="#FFE08A",
                        fill_opacity=1, stroke_width=0
                        ).shift(RIGHT*1.18 + DOWN*0.20)
    # Wheels
    wheel_l_o = Circle(radius=0.30, fill_color=WHEEL_BLACK, fill_opacity=1,
                       stroke_color="#000", stroke_width=1.0
                       ).shift(LEFT*0.85 + DOWN*0.75)
    wheel_l_i = Circle(radius=0.14, fill_color=WHEEL_RIM, fill_opacity=1,
                       stroke_width=0).shift(LEFT*0.85 + DOWN*0.75)
    wheel_r_o = wheel_l_o.copy().shift(RIGHT*1.70)
    wheel_r_i = wheel_l_i.copy().shift(RIGHT*1.70)

    g = VGroup(wheel_l_o, wheel_r_o, lower, hl, cabin, win_l, win_r,
               wheel_l_i, wheel_r_i, headlight)
    g.scale(scale).move_to(center)
    if flipped:
        g.flip(RIGHT)

    if crumple > 0.001:
        # squash front (right side) and add jagged outline
        squash_x = -1.0 * crumple    # contract front by up to 100%
        front_squish = Polygon(
            [ 1.30 - 0.7*crumple, -0.60, 0],
            [ 0.90 - 0.5*crumple, -0.10, 0],
            [ 0.40, -0.10, 0],
            [ 0.40, -0.60, 0],
            fill_color=CAR_DARK, fill_opacity=0.85, stroke_width=0,
        )
        cracks = VGroup(
            Line([0.9, 0.2, 0], [1.1, -0.3, 0],
                 stroke_color="#000", stroke_width=2),
            Line([0.95, -0.1, 0], [1.25, -0.5, 0],
                 stroke_color="#000", stroke_width=2),
        )
        g.add(front_squish, cracks)
    return g


# -----------------------------------------------------------------------------
# Road
# -----------------------------------------------------------------------------

def make_road(y=-2.4, width=14.0):
    """Asphalt strip + yellow dashed centre line."""
    asphalt = Rectangle(width=width, height=1.0, fill_color=ROAD_GREY,
                        fill_opacity=1, stroke_width=0).move_to([0, y, 0])
    edge_top = Line([-width/2, y+0.50, 0], [width/2, y+0.50, 0],
                    stroke_color="#5A5C62", stroke_width=2).set_opacity(0.7)
    edge_bot = edge_top.copy().shift(DOWN*1.0)
    dashes = VGroup()
    for x in np.arange(-width/2 + 0.4, width/2, 1.1):
        d = Rectangle(width=0.55, height=0.08, fill_color=ROAD_LINE,
                      fill_opacity=0.85, stroke_width=0
                      ).move_to([x, y, 0])
        dashes.add(d)
    return VGroup(asphalt, dashes, edge_top, edge_bot)


# -----------------------------------------------------------------------------
# Speedometer
# -----------------------------------------------------------------------------

def make_speedometer(center=np.array([0,0,0]), radius=0.85, value_kmh=60,
                     max_kmh=200, label=True):
    """
    Round speedometer with needle. value_kmh ∈ [0, max_kmh].
    Returns VGroup(dial, ticks, needle, [label]).
    """
    dial = Circle(radius=radius, fill_color=DIAL_BG, fill_opacity=1,
                  stroke_color=DIAL_RING, stroke_width=2.0)
    # tick marks
    ticks = VGroup()
    for i in range(11):
        t = i / 10.0
        ang = PI * (1 - t)   # from 180° to 0°
        outer = np.array([np.cos(ang), np.sin(ang), 0]) * radius * 0.92
        inner = np.array([np.cos(ang), np.sin(ang), 0]) * radius * 0.80
        tick = Line(inner, outer, stroke_color=DIAL_RING, stroke_width=2.0)
        ticks.add(tick)
    # needle
    frac = min(1.0, max(0.0, value_kmh / max_kmh))
    ang = PI * (1 - frac)
    tip  = np.array([np.cos(ang), np.sin(ang), 0]) * radius * 0.72
    needle = Line(ORIGIN, tip, stroke_color=NEEDLE_RED, stroke_width=5)
    cap = Circle(radius=0.06, fill_color=NEEDLE_RED, fill_opacity=1,
                 stroke_width=0)
    g = VGroup(dial, ticks, needle, cap)
    if label:
        lbl = Text(f"{value_kmh}", font="sans", font_size=22, color="#EAE4D5"
                   ).move_to(DOWN*radius*0.35)
        g.add(lbl)
    g.move_to(center)
    return g


# -----------------------------------------------------------------------------
# Wall + person
# -----------------------------------------------------------------------------

def make_wall(base=np.array([0,-2.4,0]), height=1.0, width=1.4):
    """Block-style wall sitting on the road. height in scene units."""
    block = Rectangle(width=width, height=height,
                      fill_color=WALL_GREY, fill_opacity=1,
                      stroke_color=WALL_DARK, stroke_width=1.4)
    block.move_to(base + UP*height/2)
    # brick lines (subtle)
    bricks = VGroup()
    rows = max(2, int(height / 0.30))
    for j in range(1, rows):
        y = base[1] + j * (height / rows)
        ln = Line([base[0] - width/2 + 0.05, y, 0],
                  [base[0] + width/2 - 0.05, y, 0],
                  stroke_color=WALL_DARK, stroke_width=1).set_opacity(0.5)
        bricks.add(ln)
    return VGroup(block, bricks)


def make_person(center=np.array([0,0,0]), scale=1.0, color=PERSON_BODY,
                arms_up=False):
    """Simple front-facing stick-style person."""
    head = Circle(radius=0.22, fill_color=SKIN_TONE, fill_opacity=1,
                  stroke_color="#7A4A28", stroke_width=1.2)
    body = RoundedRectangle(width=0.50, height=0.75, corner_radius=0.10,
                            fill_color=color, fill_opacity=1,
                            stroke_color="#1F3E70", stroke_width=1.2
                            ).shift(DOWN*0.62)
    if arms_up:
        arm_l = RoundedRectangle(width=0.14, height=0.55, corner_radius=0.06,
                                 fill_color=color, fill_opacity=1,
                                 stroke_color="#1F3E70", stroke_width=1.0)
        arm_l.shift(LEFT*0.30 + DOWN*0.30).rotate(-0.5, about_point=arm_l.get_top()+LEFT*0.30+DOWN*0.30)
        arm_r = arm_l.copy().flip().shift(RIGHT*0.60)
    else:
        arm_l = RoundedRectangle(width=0.14, height=0.55, corner_radius=0.06,
                                 fill_color=color, fill_opacity=1,
                                 stroke_color="#1F3E70", stroke_width=1.0
                                 ).shift(LEFT*0.32 + DOWN*0.62)
        arm_r = arm_l.copy().shift(RIGHT*0.64)
    leg_l = RoundedRectangle(width=0.18, height=0.65, corner_radius=0.06,
                             fill_color=PERSON_PANTS, fill_opacity=1,
                             stroke_width=0).shift(LEFT*0.12 + DOWN*1.32)
    leg_r = leg_l.copy().shift(RIGHT*0.24)
    foot_l = RoundedRectangle(width=0.28, height=0.10, corner_radius=0.04,
                              fill_color="#1F1A14", fill_opacity=1,
                              stroke_width=0).shift(LEFT*0.12 + DOWN*1.70)
    foot_r = foot_l.copy().shift(RIGHT*0.24)
    return VGroup(leg_l, leg_r, foot_l, foot_r, body, arm_l, arm_r, head
                  ).scale(scale).move_to(center)


def make_ground_line(y=-2.4, width=14.0):
    line = Line([-width/2, y, 0], [width/2, y, 0],
                stroke_color="#5A5C62", stroke_width=3)
    return line


# -----------------------------------------------------------------------------
# Energy bar
# -----------------------------------------------------------------------------

def make_energy_bar(base=np.array([0,0,0]), height=2.0, fill_frac=0.5,
                    color=BAR_RED, label=None):
    back = Rectangle(width=0.42, height=height, fill_color=BAR_BG,
                     fill_opacity=1, stroke_color="#444751",
                     stroke_width=1.2).move_to(base + UP*height/2)
    fh = max(0.04, height * fill_frac)
    fill = Rectangle(width=0.36, height=fh, fill_color=color,
                     fill_opacity=1, stroke_width=0)
    fill.move_to(back.get_bottom() + UP*fh/2 + UP*0.03)
    g = VGroup(back, fill)
    if label:
        lbl = Text(label, font="sans", font_size=18,
                   color="#9CA0A8").move_to(back.get_top() + UP*0.20)
        g.add(lbl)
    return g


# -----------------------------------------------------------------------------
# Crash barrier
# -----------------------------------------------------------------------------

def make_barrier(center=np.array([0,0,0]), height=1.6, width=0.40):
    body = Rectangle(width=width, height=height, fill_color=BARRIER_GREY,
                     fill_opacity=1, stroke_color="#3A3D44",
                     stroke_width=1.6).move_to(center)
    # red/white stripes
    stripes = VGroup()
    n = max(3, int(height / 0.25))
    for i in range(n):
        col = "#D03A1B" if i % 2 == 0 else "#EAE4D5"
        s = Rectangle(width=width-0.04, height=height/n,
                      fill_color=col, fill_opacity=1, stroke_width=0
                      ).move_to(center + UP*(height/2 - (i+0.5)*height/n))
        stripes.add(s)
    return VGroup(body, stripes)


# -----------------------------------------------------------------------------
# Impact rings
# -----------------------------------------------------------------------------

def impact_rings(center=np.array([0,0,0]), n=3, base_r=0.30, color=IMPACT_RED):
    """Concentric outward-radiating arcs/circles at an impact point."""
    g = VGroup()
    for i in range(n):
        r = base_r + 0.20 * i
        ring = Circle(radius=r, color=color, stroke_width=3,
                      fill_opacity=0).move_to(center).set_opacity(0.55 - 0.13*i)
        g.add(ring)
    return g


# -----------------------------------------------------------------------------
# Steering wheel + pedal (b28 — first-person dashboard)
# -----------------------------------------------------------------------------

def make_dashboard():
    """Stylized cockpit POV: steering wheel, a slice of speedometer, pedal hint."""
    # Dashboard surface
    dash = Polygon(
        [-7, -4, 0], [7, -4, 0], [6, -1.0, 0], [-6, -1.0, 0],
        fill_color="#22262E", fill_opacity=1, stroke_color="#3A3D44",
        stroke_width=1.6,
    )
    # Steering wheel
    wheel_outer = Circle(radius=1.6, fill_color="#1A1F26", fill_opacity=1,
                         stroke_color="#5A5C62", stroke_width=3.0
                         ).move_to([0, -2.8, 0])
    wheel_inner = Circle(radius=0.55, fill_color="#22262E", fill_opacity=1,
                         stroke_color="#5A5C62", stroke_width=2.0
                         ).move_to([0, -2.8, 0])
    spoke_v = Rectangle(width=0.16, height=1.0, fill_color="#5A5C62",
                        fill_opacity=1, stroke_width=0
                        ).move_to([0, -2.8, 0])
    spoke_h = Rectangle(width=1.0, height=0.16, fill_color="#5A5C62",
                        fill_opacity=1, stroke_width=0
                        ).move_to([0, -2.8, 0])
    return VGroup(dash, wheel_outer, spoke_h, spoke_v, wheel_inner)


def make_hand_on_wheel(center=np.array([-0.8, -1.9, 0])):
    """Hand wrapping over the top of the steering wheel."""
    palm = RoundedRectangle(width=0.60, height=0.34, corner_radius=0.10,
                            fill_color=SKIN_TONE, fill_opacity=1,
                            stroke_color="#7A4A28", stroke_width=1.0)
    f1 = RoundedRectangle(width=0.10, height=0.25, corner_radius=0.04,
                          fill_color=SKIN_TONE, fill_opacity=1,
                          stroke_color="#7A4A28", stroke_width=0.8
                          ).shift(DOWN*0.22 + LEFT*0.20)
    f2 = f1.copy().shift(RIGHT*0.15)
    f3 = f1.copy().shift(RIGHT*0.30)
    f4 = f1.copy().shift(RIGHT*0.45)
    return VGroup(palm, f1, f2, f3, f4).move_to(center)


def small_label(text, pos, color=WHITE, size=24, opacity=0.95, weight=NORMAL):
    return Text(text, font="sans", font_size=size, color=color, weight=weight
                ).move_to(pos).set_opacity(opacity)
