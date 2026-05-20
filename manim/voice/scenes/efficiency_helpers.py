"""Helpers for the Efficiency (efficiency) scene.

Primitives: work bars (input/output), a simple machine block, a winch
with a load and heat shimmer at the gears, ideal-vs-real bar pairs, an
efficiency percent dial that can rest below 100, stepped-loss stages,
and a conserved bar that splits into useful + heat.

Pure #000000 void, font="sans" for all text.
"""

from manim import *
import numpy as np

VOID = "#000000"

WORK_COLOR   = "#7FB8E8"   # input / useful work — calm blue
USEFUL_COLOR = "#7FCF9A"   # the part that did the job — green
HEAT_COLOR   = "#E08A5A"   # lost to friction — warm orange
TRACK_COLOR  = "#3A3A40"   # empty bar track
MACHINE_COL  = "#9AA0A8"   # machine body grey
MACHINE_DARK = "#5A5E66"
LABEL_COL    = "#EAE4D5"   # warm off-white text
FAINT_LABEL  = "#8C98A6"


def label(text, pos, color=LABEL_COL, size=26, opacity=0.95, slant=NORMAL):
    return Text(text, font="sans", font_size=size, color=color,
                slant=slant).move_to(pos).set_opacity(opacity)


def work_bar(length, pos, color=WORK_COLOR, height=0.62, max_length=4.0,
             track=True):
    """A horizontal work bar of given `length`, left-anchored at `pos`.

    Returns a VGroup: (optional faint full-length track, filled bar).
    `pos` is the LEFT end midpoint of the bar.
    """
    pos = np.array(pos, dtype=float)
    grp = VGroup()
    if track:
        tr = Rectangle(width=max_length, height=height,
                        stroke_color=TRACK_COLOR, stroke_width=1.5,
                        fill_opacity=0)
        tr.move_to(pos + np.array([max_length / 2.0, 0, 0]))
        grp.add(tr)
    length = max(0.001, length)
    bar = Rectangle(width=length, height=height,
                    fill_color=color, fill_opacity=0.92,
                    stroke_color=color, stroke_width=1.5)
    bar.move_to(pos + np.array([length / 2.0, 0, 0]))
    grp.add(bar)
    return grp


def bar_only(length, pos, color=WORK_COLOR, height=0.62):
    """Just the filled bar, left-anchored at pos. No track."""
    pos = np.array(pos, dtype=float)
    length = max(0.001, length)
    bar = Rectangle(width=length, height=height,
                    fill_color=color, fill_opacity=0.92,
                    stroke_color=color, stroke_width=1.5)
    bar.move_to(pos + np.array([length / 2.0, 0, 0]))
    return bar


def machine_block(pos, w=1.7, h=2.0, teeth=True):
    """A simple machine: a rounded grey body with two gear-like circles."""
    pos = np.array(pos, dtype=float)
    body = RoundedRectangle(corner_radius=0.18, width=w, height=h,
                            fill_color=MACHINE_COL, fill_opacity=0.30,
                            stroke_color=MACHINE_COL, stroke_width=2.2)
    body.move_to(pos)
    g1 = _gear(pos + np.array([-0.32, 0.30, 0]), r=0.34)
    g2 = _gear(pos + np.array([0.34, -0.28, 0]), r=0.27)
    return VGroup(body, g1, g2)


def _gear(center, r=0.32, n_teeth=10, color=MACHINE_DARK):
    center = np.array(center, dtype=float)
    ring = Circle(radius=r, stroke_color=color, stroke_width=2.4,
                  fill_opacity=0).move_to(center)
    hub = Dot(point=center, radius=r * 0.22, color=color)
    teeth = VGroup()
    for k in range(n_teeth):
        a = TAU * k / n_teeth
        u = np.array([np.cos(a), np.sin(a), 0])
        seg = Line(center + u * r, center + u * (r + 0.10),
                   stroke_color=color, stroke_width=2.4)
        teeth.add(seg)
    return VGroup(ring, hub, teeth)


def winch(pos, scale=1.0):
    """A hand-crank winch: a frame, a drum with a crank handle, and a
    cable hanging down ready to take a load. Returns dict of parts."""
    pos = np.array(pos, dtype=float)
    s = scale
    post_l = Line(pos + np.array([-0.7, -1.1, 0]) * s,
                  pos + np.array([-0.7, 0.7, 0]) * s,
                  stroke_color=MACHINE_COL, stroke_width=3.5 * s)
    post_r = Line(pos + np.array([0.7, -1.1, 0]) * s,
                  pos + np.array([0.7, 0.7, 0]) * s,
                  stroke_color=MACHINE_COL, stroke_width=3.5 * s)
    drum = Circle(radius=0.42 * s, fill_color=MACHINE_DARK, fill_opacity=0.55,
                  stroke_color=MACHINE_COL, stroke_width=2.4).move_to(pos)
    axle = Dot(point=pos, radius=0.07 * s, color=MACHINE_COL)
    crank = Line(pos, pos + np.array([0.55, 0.30, 0]) * s,
                 stroke_color=MACHINE_COL, stroke_width=3.5 * s)
    handle = Dot(point=pos + np.array([0.55, 0.30, 0]) * s,
                 radius=0.09 * s, color=LABEL_COL)
    cable = Line(pos + np.array([0, -0.42, 0]) * s,
                 pos + np.array([0, -1.7, 0]) * s,
                 stroke_color=FAINT_LABEL, stroke_width=2.0)
    frame = VGroup(post_l, post_r)
    return {
        "group": VGroup(frame, drum, axle, crank, handle, cable),
        "frame": frame, "drum": drum, "axle": axle,
        "crank": crank, "handle": handle, "cable": cable,
        "drum_center": pos, "cable_end": pos + np.array([0, -1.7, 0]) * s,
    }


def make_load(pos, size=0.55):
    """A blocky weight to be lifted."""
    pos = np.array(pos, dtype=float)
    box = Rectangle(width=size * 1.5, height=size,
                    fill_color=MACHINE_DARK, fill_opacity=0.8,
                    stroke_color=MACHINE_COL, stroke_width=2.0).move_to(pos)
    hook = Arc(radius=size * 0.22, start_angle=PI * 0.15,
               angle=PI * 1.4, stroke_color=MACHINE_COL,
               stroke_width=2.0).next_to(box, UP, buff=0.0)
    return VGroup(hook, box)


def heat_shimmer(center, n=5, spread=0.6, color=HEAT_COLOR, rise=0.7):
    """A cluster of wavy heat squiggles rising from `center`."""
    center = np.array(center, dtype=float)
    g = VGroup()
    for k in range(n):
        x0 = (k - (n - 1) / 2.0) * (spread / max(1, n - 1))
        pts = []
        steps = 16
        for i in range(steps + 1):
            t = i / steps
            y = -0.05 + t * rise
            x = x0 + 0.10 * np.sin(t * TAU * 1.6 + k)
            pts.append(center + np.array([x, y, 0]))
        wig = VMobject(stroke_color=color, stroke_width=2.4)
        wig.set_points_smoothly(pts)
        wig.set_opacity(0.55 + 0.10 * (k % 2))
        g.add(wig)
    return g


def stream(start, end, color=WORK_COLOR, width=6):
    """A directed flow arrow from start to end (used for input flow)."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    return Arrow(start, end, color=color, stroke_width=width,
                 buff=0.05, max_tip_length_to_length_ratio=0.18,
                 tip_length=0.22)


def percent_dial(pos, value, scale=1.0, color=USEFUL_COLOR, show_100=True):
    """A semicircular dial 0..100%. Needle rests at `value` (0-100).

    100% is marked but the needle stays below it for real machines.
    Returns dict with 'group' and 'needle'.
    """
    pos = np.array(pos, dtype=float)
    R = 1.6 * scale
    arc = Arc(radius=R, start_angle=PI, angle=-PI,
              stroke_color=MACHINE_COL, stroke_width=3.0).move_to(
                  pos + np.array([0, -0.0, 0]))
    arc.shift(pos - arc.get_arc_center())
    # tick at 0, 50, 100
    ticks = VGroup()
    for frac in (0.0, 0.5, 1.0):
        a = PI - PI * frac
        u = np.array([np.cos(a), np.sin(a), 0])
        ticks.add(Line(pos + u * (R - 0.16), pos + u * (R + 0.04),
                       stroke_color=MACHINE_COL, stroke_width=2.4))
    hub = Dot(point=pos, radius=0.08 * scale, color=LABEL_COL)
    frac = np.clip(value / 100.0, 0.0, 1.0)
    a = PI - PI * frac
    u = np.array([np.cos(a), np.sin(a), 0])
    needle = Line(pos, pos + u * (R - 0.22),
                  stroke_color=color, stroke_width=4.2)
    parts = VGroup(arc, ticks, hub, needle)
    if show_100:
        u100 = np.array([np.cos(0.0), np.sin(0.0), 0])
        cap = Text("100%", font="sans", font_size=22 * scale,
                   color=FAINT_LABEL).move_to(
                       pos + u100 * (R + 0.45) + np.array([0, 0.05, 0]))
        z = Text("0", font="sans", font_size=20 * scale,
                 color=FAINT_LABEL).move_to(
                     pos + np.array([-(R + 0.30), 0.05, 0]))
        parts.add(cap, z)
    vlabel = Text(f"{int(round(value))}%", font="sans",
                  font_size=34 * scale, color=color).move_to(
                      pos + np.array([0, -0.55 * scale, 0]))
    parts.add(vlabel)
    return {"group": parts, "needle": needle, "value_label": vlabel,
            "center": pos, "R": R}


def split_bar(total_len, pos, useful_frac, height=0.7,
               useful_color=USEFUL_COLOR, heat_color=HEAT_COLOR):
    """One conserved bar of `total_len`, left-anchored at pos, split into
    a useful segment (left) + heat segment (right). They sum to total."""
    pos = np.array(pos, dtype=float)
    useful_frac = float(np.clip(useful_frac, 0.0, 1.0))
    ul = total_len * useful_frac
    hl = total_len * (1.0 - useful_frac)
    useful = Rectangle(width=max(0.001, ul), height=height,
                       fill_color=useful_color, fill_opacity=0.92,
                       stroke_color=useful_color, stroke_width=1.5)
    useful.move_to(pos + np.array([ul / 2.0, 0, 0]))
    heat = Rectangle(width=max(0.001, hl), height=height,
                     fill_color=heat_color, fill_opacity=0.92,
                     stroke_color=heat_color, stroke_width=1.5)
    heat.move_to(pos + np.array([ul + hl / 2.0, 0, 0]))
    return VGroup(useful, heat)
