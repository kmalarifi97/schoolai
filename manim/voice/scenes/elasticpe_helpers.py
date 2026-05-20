"""Helpers for the Elastic Potential Energy (elasticpe) scene.

Primitives for the 12 beats: a drawn bow + arrow, a work bar that pours
into arrow speed, stretched / compressed springs, a bent ruler, a
"wants to return" arrow, growing resist arrows, a stored-energy bar that
climbs in accelerating jumps, an everyday-elastic row (trampoline, vault
pole, clock spring, diving board), an overstretched spring, and a
load/release cycle.

Pure #000000 void. font="sans" for any text.
"""

from manim import *
import numpy as np

VOID = "#000000"

ELASTIC   = "#7FB8E8"   # primary elastic-energy blue
ELASTIC_F = "#4A6E8C"   # faint blue
ENERGY    = "#E8C46A"   # stored-energy gold
ARROWCOL  = "#EAE4D5"   # arrow / motion bone-white
RESIST    = "#E08A6A"   # resisting-force warm
WOOD      = "#C9A06A"   # bow / ruler / board wood
SPRINGCOL = "#9FB8C8"   # spring steel
DIM       = "#8C98A6"   # labels / dim


# ----------------------------------------------------------------------
#  text
# ----------------------------------------------------------------------
def small_label(text, pos, color=DIM, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


# ----------------------------------------------------------------------
#  spring  (zig-zag coil between two anchor points)
# ----------------------------------------------------------------------
def make_spring(start, end, coils=9, amp=0.30, color=SPRINGCOL, width=4):
    """A coil spring drawn as a zig-zag from start to end with short
    straight lead-ins at each end."""
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    axis = e - s
    L = np.linalg.norm(axis)
    if L < 1e-6:
        axis = np.array([1.0, 0, 0]); L = 1e-6
    u = axis / L
    perp = np.array([-u[1], u[0], 0.0])
    lead = min(0.18 * L, 0.30)
    p0 = s + u * lead
    p1 = e - u * lead
    span = p1 - p0
    pts = [s, p0]
    n = max(2, coils) * 2
    for k in range(1, n):
        frac = k / n
        sign = 1.0 if (k % 2 == 1) else -1.0
        pts.append(p0 + span * frac + perp * (amp * sign))
    pts.extend([p1, e])
    coil = VMobject(stroke_color=color, stroke_width=width)
    coil.set_points_as_corners([np.array(p) for p in pts])
    return coil


def wall_block(center, w=0.30, h=1.4, color=DIM):
    """A fixed anchor wall with hatching feel (just a filled bar)."""
    return Rectangle(width=w, height=h, fill_color=color,
                     fill_opacity=0.30, stroke_color=color,
                     stroke_width=2).move_to(center)


def spring_mass(center, r=0.34, color=ELASTIC):
    return Circle(radius=r, fill_color=color, fill_opacity=0.85,
                  stroke_color=WHITE, stroke_width=1.5).move_to(center)


# ----------------------------------------------------------------------
#  bow + arrow
# ----------------------------------------------------------------------
def make_bow(center=ORIGIN, draw=0.0, scale=1.0):
    """A bow drawn as an arc whose curvature deepens with `draw`
    (0 = relaxed, 1 = fully drawn), a string, and a nocked arrow.

    Returns a dict: {'group','arrow','string','limbs','nock'} so beats
    can animate the arrow separately.
    """
    c = np.array(center, dtype=float)
    span = 2.6 * scale          # tip-to-tip vertical span
    top = c + np.array([0, span / 2, 0])
    bot = c + np.array([0, -span / 2, 0])
    belly = 1.0 * scale         # how far the bow bulges left (toward archer pull is right)
    bow_x = -0.1 * scale

    # limbs: arc bulging LEFT, string pulled RIGHT by `draw`
    limb_ctrl = c + np.array([bow_x - belly, 0, 0])
    limbs = VMobject(stroke_color=WOOD, stroke_width=7 * scale)
    arc_pts = []
    for t in np.linspace(0, 1, 40):
        p = (1 - t) ** 2 * top + 2 * (1 - t) * t * limb_ctrl + t ** 2 * bot
        arc_pts.append(p)
    limbs.set_points_smoothly([np.array(p) for p in arc_pts])

    # string nock point: pulled right proportional to draw
    nock_pt = c + np.array([bow_x + 0.25 * scale + draw * 1.5 * scale, 0, 0])
    string = VMobject(stroke_color="#D8D2C2", stroke_width=2.5)
    string.set_points_as_corners([top, nock_pt, bot])

    # arrow: shaft from nock pointing LEFT (flight direction), tip at left
    shaft_len = 2.1 * scale
    arr_tail = nock_pt
    arr_head = nock_pt + np.array([-shaft_len, 0, 0])
    arrow = Arrow(arr_tail, arr_head, color=ARROWCOL, stroke_width=5,
                  buff=0, max_tip_length_to_length_ratio=0.16,
                  tip_length=0.26)

    nock = Dot(nock_pt, radius=0.05, color="#D8D2C2")

    group = VGroup(limbs, string, arrow, nock).move_to(center) \
        if False else VGroup(limbs, string, arrow, nock)
    return {"group": group, "arrow": arrow, "string": string,
            "limbs": limbs, "nock": nock, "nock_pt": nock_pt}


def flying_arrow(start, length=2.1, color=ARROWCOL):
    s = np.array(start, dtype=float)
    e = s + np.array([-length, 0, 0])
    return Arrow(s, e, color=color, stroke_width=5, buff=0,
                 max_tip_length_to_length_ratio=0.16, tip_length=0.26)


# ----------------------------------------------------------------------
#  bars  (work bar / stored-energy bar)
# ----------------------------------------------------------------------
def make_bar(center, max_h=2.6, w=0.62, frac=1.0, color=ENERGY,
             label=None, label_size=24):
    """A vertical fill bar inside a thin frame.  Returns a dict
    {'group','frame','fill','base','max_h','w','center'}."""
    c = np.array(center, dtype=float)
    frame = Rectangle(width=w, height=max_h, stroke_color=DIM,
                      stroke_width=2, fill_opacity=0).move_to(c)
    base_y = c[1] - max_h / 2
    h = max(1e-4, frac * max_h)
    fill = Rectangle(width=w - 0.06, height=h, fill_color=color,
                     fill_opacity=0.9, stroke_width=0)
    fill.move_to([c[0], base_y + h / 2, 0])
    grp = VGroup(frame, fill)
    if label is not None:
        lbl = small_label(label, [c[0], c[1] - max_h / 2 - 0.34, 0],
                          color=DIM, size=label_size)
        grp.add(lbl)
    return {"group": grp, "frame": frame, "fill": fill,
            "base_y": base_y, "max_h": max_h, "w": w, "center": c,
            "color": color}


def set_bar(bar, frac):
    """Return an updated fill Rectangle for `bar` at fraction `frac`
    (use with Transform / .become)."""
    frac = float(np.clip(frac, 0.0, 1.0))
    h = max(1e-4, frac * bar["max_h"])
    f = Rectangle(width=bar["w"] - 0.06, height=h,
                  fill_color=bar["color"], fill_opacity=0.9,
                  stroke_width=0)
    f.move_to([bar["center"][0], bar["base_y"] + h / 2, 0])
    return f


# ----------------------------------------------------------------------
#  bent ruler / diving board / vault pole  (a flexed beam)
# ----------------------------------------------------------------------
def bent_beam(start, end, bend=0.0, color=WOOD, width=6, samples=40):
    """A beam from start to end, bowed perpendicular by `bend`
    (parabolic deflection).  Positive bend bows toward +perp."""
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    axis = e - s
    L = np.linalg.norm(axis)
    u = axis / (L if L > 1e-6 else 1.0)
    perp = np.array([-u[1], u[0], 0.0])
    pts = []
    for t in np.linspace(0, 1, samples):
        defl = bend * 4 * t * (1 - t)        # 0 at ends, max mid
        pts.append(s + axis * t + perp * defl)
    beam = VMobject(stroke_color=color, stroke_width=width)
    beam.set_points_smoothly([np.array(p) for p in pts])
    return beam


def clock_spring(center, turns=3.4, r0=0.06, dr=0.085, color=SPRINGCOL,
                 width=3.5, n=240):
    """An Archimedean spiral — a coiled clock mainspring."""
    c = np.array(center, dtype=float)
    pts = []
    for i in range(n):
        a = i / (n - 1) * turns * TAU
        rad = r0 + dr * a / TAU
        pts.append(c + np.array([rad * np.cos(a), rad * np.sin(a), 0]))
    sp = VMobject(stroke_color=color, stroke_width=width)
    sp.set_points_smoothly([np.array(p) for p in pts])
    return sp


def trampoline(center, dip=0.0, w=2.0, color=SPRINGCOL):
    """A trampoline mat sagging downward by `dip`, on two legs."""
    c = np.array(center, dtype=float)
    left = c + np.array([-w / 2, 0, 0])
    right = c + np.array([w / 2, 0, 0])
    mat = VMobject(stroke_color=color, stroke_width=5)
    pts = []
    for t in np.linspace(0, 1, 30):
        sag = -dip * 4 * t * (1 - t)
        pts.append(left + (right - left) * t + np.array([0, sag, 0]))
    mat.set_points_smoothly([np.array(p) for p in pts])
    leg1 = Line(left, left + np.array([0, -0.7, 0]),
                color=DIM, stroke_width=4)
    leg2 = Line(right, right + np.array([0, -0.7, 0]),
                color=DIM, stroke_width=4)
    return VGroup(mat, leg1, leg2)


def wants_return_arrow(start, end, color=ELASTIC, width=5):
    """A curved arrow suggesting 'wants to spring back'."""
    s = np.array(start, dtype=float)
    e = np.array(end, dtype=float)
    return CurvedArrow(s, e, color=color, stroke_width=width,
                       angle=-TAU / 7, tip_length=0.22)


def resist_arrow(start, length, color=RESIST, width=5):
    """A straight resisting-force arrow of given length, pointing
    back toward the relaxed side (+x by default = leftward pull)."""
    s = np.array(start, dtype=float)
    e = s + np.array([-length, 0, 0])
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.30, tip_length=0.20)
