"""Helpers for the Power (power) scene.

Power = the rate of doing work. Primitives:
- a stick figure (standing / climbing / collapsed)
- a stairwell (flights of stairs) + a carried box
- a wall clock with a movable hand
- "work done" bars (equal height) and time bars (variable width)
- a power bar that grows/shrinks
- two simple cars on a track with a finish line
- a pulley lifting a piano
- text label helpers (watt, energy vs power)

Pure #000000 void, font="sans".
"""

from manim import *
import numpy as np

VOID = "#000000"

WORK_COL  = "#7FB8E8"   # work / energy — calm blue
TIME_COL  = "#C9A24B"   # time — warm amber
POWER_COL = "#E8956F"   # power — energetic orange
FIG_COL   = "#EAE4D5"   # figure / line art — bone
BOX_COL   = "#B89A6A"   # the carried box
STAIR_COL = "#6E7681"   # stairs / structure grey
INK       = "#EAE4D5"   # default text


def stick_figure(pose="stand", color=FIG_COL, scale=1.0):
    """A simple stick figure. pose in {stand, climb, collapse}."""
    g = VGroup()
    head = Circle(radius=0.16, color=color, stroke_width=4)
    if pose == "collapse":
        # slumped, sitting on the ground
        head.move_to([0.0, 0.30, 0])
        torso = Line([0.0, 0.16, 0], [0.30, -0.30, 0], color=color, stroke_width=4)
        armL = Line([0.10, 0.02, 0], [-0.18, -0.28, 0], color=color, stroke_width=4)
        armR = Line([0.10, 0.02, 0], [0.40, -0.10, 0], color=color, stroke_width=4)
        legL = Line([0.30, -0.30, 0], [0.62, -0.34, 0], color=color, stroke_width=4)
        legR = Line([0.30, -0.30, 0], [0.55, -0.10, 0], color=color, stroke_width=4)
    elif pose == "climb":
        head.move_to([0.0, 0.70, 0])
        torso = Line([0.0, 0.54, 0], [0.0, 0.02, 0], color=color, stroke_width=4)
        armL = Line([0.0, 0.42, 0], [-0.26, 0.16, 0], color=color, stroke_width=4)
        armR = Line([0.0, 0.42, 0], [0.24, 0.58, 0], color=color, stroke_width=4)
        legL = Line([0.0, 0.02, 0], [-0.22, -0.42, 0], color=color, stroke_width=4)
        legR = Line([0.0, 0.02, 0], [0.26, -0.20, 0], color=color, stroke_width=4)
    else:  # stand
        head.move_to([0.0, 0.70, 0])
        torso = Line([0.0, 0.54, 0], [0.0, 0.0, 0], color=color, stroke_width=4)
        armL = Line([0.0, 0.42, 0], [-0.22, 0.10, 0], color=color, stroke_width=4)
        armR = Line([0.0, 0.42, 0], [0.22, 0.10, 0], color=color, stroke_width=4)
        legL = Line([0.0, 0.0, 0], [-0.18, -0.46, 0], color=color, stroke_width=4)
        legR = Line([0.0, 0.0, 0], [0.18, -0.46, 0], color=color, stroke_width=4)
    g.add(head, torso, armL, armR, legL, legR)
    return g.scale(scale)


def carried_box(size=0.34, color=BOX_COL):
    """A small box, meant to be placed above a figure's head."""
    b = Square(side_length=size, fill_color=color, fill_opacity=1,
               stroke_color="#E8DCC0", stroke_width=2)
    return b


def stairwell(n=4, step_w=0.62, step_h=0.46, color=STAIR_COL, origin=None):
    """A flight of `n` stairs rising to the right. Returns a VGroup;
    .corners holds the top-of-step landing points (np arrays)."""
    if origin is None:
        origin = np.array([-3.0, -2.3, 0.0])
    origin = np.array(origin, dtype=float)
    g = VGroup()
    corners = []
    x, y = origin[0], origin[1]
    for i in range(n):
        # vertical riser
        riser = Line([x, y, 0], [x, y + step_h, 0], color=color, stroke_width=5)
        # horizontal tread
        tread = Line([x, y + step_h, 0], [x + step_w, y + step_h, 0],
                     color=color, stroke_width=5)
        g.add(riser, tread)
        y += step_h
        corners.append(np.array([x + step_w * 0.5, y, 0]))
        x += step_w
    base = Line([origin[0], origin[1], 0], origin + np.array([-0.5, 0, 0]),
                color=color, stroke_width=5)
    g.add(base)
    g.corners = corners
    g.top = np.array([x, y, 0])
    return g


def wall_clock(pos, radius=0.85, color=FIG_COL):
    """A round clock face. Returns VGroup with .hand (the minute hand line)
    pivoting about clock center; rotate .hand about `pos`."""
    pos = np.array(pos, dtype=float)
    face = Circle(radius=radius, color=color, stroke_width=4)
    ticks = VGroup()
    for k in range(12):
        a = TAU * k / 12 + PI / 2
        outer = np.array([np.cos(a), np.sin(a), 0]) * radius
        inner = np.array([np.cos(a), np.sin(a), 0]) * (radius - 0.12)
        ticks.add(Line(inner, outer, color=color, stroke_width=2.5))
    hand = Line([0, 0, 0], [0, radius - 0.22, 0], color=POWER_COL,
                stroke_width=5)
    hub = Dot(point=[0, 0, 0], radius=0.05, color=color)
    g = VGroup(face, ticks, hand, hub).move_to(pos)
    g.hand = hand
    g.center_pt = pos
    return g


def value_bar(height, width=0.9, color=WORK_COL, anchor=None, label=None,
              label_color=INK):
    """A vertical bar of given height, bottom-anchored at `anchor`.
    Optional text label below it. Returns VGroup; .bar is the rectangle."""
    if anchor is None:
        anchor = np.array([0, -2.4, 0])
    anchor = np.array(anchor, dtype=float)
    bar = Rectangle(width=width, height=max(height, 0.001),
                    fill_color=color, fill_opacity=0.92,
                    stroke_color=color, stroke_width=2)
    bar.move_to(anchor + np.array([0, max(height, 0.001) / 2.0, 0]))
    g = VGroup(bar)
    g.bar = bar
    g.anchor = anchor
    if label is not None:
        t = Text(label, font="sans", font_size=26, color=label_color)
        t.next_to(bar, DOWN, buff=0.22)
        g.add(t)
        g.label = t
    return g


def time_bar(width, height=0.42, color=TIME_COL, anchor=None, label=None,
             label_color=INK):
    """A horizontal time bar, left-anchored at `anchor`."""
    if anchor is None:
        anchor = np.array([-2.0, -2.6, 0])
    anchor = np.array(anchor, dtype=float)
    bar = Rectangle(width=max(width, 0.001), height=height,
                    fill_color=color, fill_opacity=0.9,
                    stroke_color=color, stroke_width=2)
    bar.move_to(anchor + np.array([max(width, 0.001) / 2.0, 0, 0]))
    g = VGroup(bar)
    g.bar = bar
    g.anchor = anchor
    if label is not None:
        t = Text(label, font="sans", font_size=24, color=label_color)
        t.next_to(bar, DOWN, buff=0.18)
        g.add(t)
        g.label = t
    return g


def simple_car(pos, color=FIG_COL, scale=1.0):
    """A minimal side-view car."""
    body = RoundedRectangle(width=0.95, height=0.32, corner_radius=0.08,
                            fill_color=color, fill_opacity=0.18,
                            stroke_color=color, stroke_width=3)
    cab = Polygon([-0.22, 0.16, 0], [0.20, 0.16, 0], [0.10, 0.42, 0],
                  [-0.12, 0.42, 0], color=color, stroke_width=3,
                  fill_opacity=0.10)
    w1 = Circle(radius=0.13, color=color, stroke_width=3,
                fill_color=VOID, fill_opacity=1).move_to([-0.30, -0.18, 0])
    w2 = Circle(radius=0.13, color=color, stroke_width=3,
                fill_color=VOID, fill_opacity=1).move_to([0.30, -0.18, 0])
    g = VGroup(body, cab, w1, w2).scale(scale).move_to(pos)
    return g


def piano(pos, color=FIG_COL, scale=1.0):
    """A tiny upright-piano silhouette to be lifted by a pulley."""
    body = Rectangle(width=0.66, height=0.52, fill_color=color,
                     fill_opacity=0.16, stroke_color=color, stroke_width=3)
    lid = Line([-0.33, 0.26, 0], [0.33, 0.26, 0], color=color, stroke_width=3)
    keys = VGroup()
    for k in range(7):
        x = -0.28 + k * 0.095
        keys.add(Line([x, -0.26, 0], [x, -0.12, 0], color=color,
                      stroke_width=2))
    kb = Line([-0.30, -0.12, 0], [0.30, -0.12, 0], color=color,
              stroke_width=2)
    g = VGroup(body, lid, keys, kb).scale(scale).move_to(pos)
    return g


def pulley(center, radius=0.30, color=STAIR_COL):
    """A pulley wheel mounted on a beam at `center` (the wheel hub)."""
    center = np.array(center, dtype=float)
    wheel = Circle(radius=radius, color=color, stroke_width=4).move_to(center)
    hub = Dot(point=center, radius=0.05, color=color)
    beam = Line(center + np.array([-0.9, radius + 0.05, 0]),
                center + np.array([0.9, radius + 0.05, 0]),
                color=color, stroke_width=5)
    return VGroup(beam, wheel, hub)


def big_label(text, pos, size=46, color=INK, slant=NORMAL):
    return Text(text, font="sans", font_size=size, color=color,
                slant=slant).move_to(pos)


def small_label(text, pos, color=INK, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def horse_motif(pos, color=STAIR_COL, scale=1.0):
    """A very faint stylized horse silhouette (b10 background motif)."""
    body = Ellipse(width=0.9, height=0.42, color=color, stroke_width=3,
                   fill_opacity=0.0)
    neck = Line([0.34, 0.10, 0], [0.56, 0.40, 0], color=color, stroke_width=3)
    head = Line([0.56, 0.40, 0], [0.70, 0.30, 0], color=color, stroke_width=3)
    l1 = Line([-0.28, -0.20, 0], [-0.30, -0.55, 0], color=color, stroke_width=3)
    l2 = Line([0.28, -0.20, 0], [0.30, -0.55, 0], color=color, stroke_width=3)
    tail = Line([-0.44, 0.06, 0], [-0.62, -0.20, 0], color=color, stroke_width=3)
    g = VGroup(body, neck, head, l1, l2, tail).scale(scale).move_to(pos)
    g.set_opacity(0.30)
    return g
