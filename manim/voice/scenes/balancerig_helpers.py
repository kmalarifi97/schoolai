"""Helpers for The Balancing Rig (balancerig) project-story.

A narrative: Lina hangs a mobile over her brother's bed; it keeps
tilting. She rebuilds it in PhET Balancing Act, predicts-then-releases,
then the ending calls back to two earlier concept videos:
  - torque (a wrench / lever arm on a stuck bolt)
  - center of mass (a tumbling wrench whose CoM traces a clean arc)

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Warm, low-key palette — wood, chalk, faint glows. No hype colors.
WOOD      = "#C9A66B"   # the bar / plank
WOOD_DARK = "#8A6E40"   # edge / shadow
CHALK     = "#EAE4D5"   # chalk-white lines / labels
DIM       = "#8C8576"   # dim secondary
STRING    = "#B8B0A0"   # the hanging string
LEFTC     = "#7FB8E8"   # left side / left twist (cool blue)
RIGHTC    = "#E8C46B"   # right side / right twist (warm gold)
HEAVY     = "#C98A6B"   # heavy shape
LIGHT     = "#9BD6B0"   # light shape
COM_C     = "#E0668C"   # center-of-mass marker (quiet rose)
LEVEL_C   = "#9BD6B0"   # level indicator OK
TILT_C    = "#C98A6B"   # tilt indicator warning
SKIN      = "#D8B48C"
SHIRT     = "#6E8C9B"


# ----------------------------------------------------------------------
# Lina — a minimal figure. A presence in the story, not a portrait.
# ----------------------------------------------------------------------
def make_lina(pos=ORIGIN, scale=1.0, facing=1):
    head = Circle(radius=0.16, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0)
    head.move_to(UP * 0.62)
    torso = Line(UP * 0.46, DOWN * 0.10, color=SHIRT, stroke_width=8)
    arm = Line(UP * 0.40, RIGHT * facing * 0.30 + UP * 0.30,
               color=SHIRT, stroke_width=6)   # reaching up to the mobile
    leg1 = Line(DOWN * 0.10, DOWN * 0.62 + LEFT * 0.12,
                color=WOOD_DARK, stroke_width=6)
    leg2 = Line(DOWN * 0.10, DOWN * 0.62 + RIGHT * 0.12,
                color=WOOD_DARK, stroke_width=6)
    g = VGroup(head, torso, arm, leg1, leg2)
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# The hanging mobile: a horizontal bar suspended from one central string,
# with dangling shapes. `shapes` = list of (x, weight, color) where x is
# the offset along the bar from center (m-ish), weight scales the shape.
# Returns a dict so beats can reach the pivot / bar / shapes precisely.
# ----------------------------------------------------------------------
def make_mobile(pos=ORIGIN, half_w=3.4, shapes=None, tilt=0.0,
                ceil_y=3.0):
    if shapes is None:
        shapes = [(-2.4, 1.0, HEAVY), (-0.9, 0.6, LIGHT),
                  (1.4, 0.8, RIGHT_C := RIGHTC), (2.6, 0.7, LIGHT)]
    pivot = np.array([0.0, 0.0, 0.0])

    # the ceiling anchor + the central string
    anchor = np.array([0.0, ceil_y - pos[1], 0.0])
    ceiling = Line([-1.4, anchor[1], 0], [1.4, anchor[1], 0],
                   color=DIM, stroke_width=3).set_opacity(0.5)
    string = Line(anchor, pivot, color=STRING, stroke_width=2)

    bar = Rectangle(width=2 * half_w, height=0.16,
                    fill_color=WOOD, fill_opacity=1,
                    stroke_color=WOOD_DARK, stroke_width=2)
    bar.move_to(pivot)

    shape_grp = VGroup()
    for (x, wt, col) in shapes:
        sz = 0.18 + 0.34 * wt
        thread = Line([x, -0.08, 0], [x, -0.08 - 0.34, 0],
                      color=STRING, stroke_width=1.5)
        body = Circle(radius=sz, fill_color=col, fill_opacity=1,
                      stroke_color=CHALK, stroke_width=1.5)
        body.move_to([x, -0.08 - 0.34 - sz, 0])
        shape_grp.add(VGroup(thread, body))

    # everything that rotates about the pivot when the bar tilts
    rig = VGroup(bar, shape_grp)
    if abs(tilt) > 1e-6:
        rig.rotate(tilt, about_point=pivot)

    grp = VGroup(ceiling, string, rig)
    grp.move_to(pos + np.array([0, 0, 0]))
    info = {
        "group": grp, "rig": rig, "bar": bar, "string": string,
        "ceiling": ceiling, "shapes": shape_grp, "pivot": pivot,
        "anchor": anchor, "half_w": half_w,
    }
    return info


def tilt_rig(rig_info, angle, run_time=1.4, scene=None,
             rate_func=rate_functions.ease_in_out_sine):
    """Animate the bar+shapes rotating about the central string pivot."""
    pv = rig_info["group"].get_center() + np.array([0, 0, 0])
    pv = rig_info["string"].get_end()
    anim = Rotate(rig_info["rig"], angle=angle, about_point=pv,
                  rate_func=rate_func)
    if scene is not None:
        scene.play(anim, run_time=run_time)
    return anim


# ----------------------------------------------------------------------
# A turning arrow whose size encodes weight x distance (torque). Drawn as
# a curved arrow about a pivot; CCW for left side, CW for right side.
# ----------------------------------------------------------------------
def twist_arrow(pivot, weight, distance, side="left", color=None,
                base=0.55, gain=0.30):
    mag = base + gain * weight * abs(distance)
    mag = float(np.clip(mag, 0.4, 2.1))
    if color is None:
        color = LEFTC if side == "left" else RIGHTC
    if side == "left":      # CCW
        arc = Arc(radius=mag, start_angle=-0.6, angle=2.0,
                  arc_center=pivot, color=color, stroke_width=5)
    else:                   # CW
        arc = Arc(radius=mag, start_angle=PI + 0.6, angle=-2.0,
                  arc_center=pivot, color=color, stroke_width=5)
    tip = ArrowTriangleFilledTip(color=color, length=0.22)
    arc.add_tip(tip)
    return arc


# ----------------------------------------------------------------------
# The combined center-of-mass point, drawn directly below the string.
# ----------------------------------------------------------------------
def com_marker(pos, scale=1.0, color=COM_C, label=True):
    rr = 0.16 * scale
    ring = Circle(radius=rr, color=color, stroke_width=3,
                  fill_opacity=0)
    q1 = Sector(radius=rr, start_angle=0, angle=PI / 2,
                color=color, fill_opacity=1, stroke_width=0)
    q2 = Sector(radius=rr, start_angle=PI, angle=PI / 2,
                color=color, fill_opacity=1, stroke_width=0)
    m = VGroup(ring, q1, q2).move_to(pos)
    if label:
        t = Text("center of mass", font="sans", font_size=18,
                 color=color).next_to(m, DOWN, buff=0.16)
        return VGroup(m, t)
    return m


# ----------------------------------------------------------------------
# Long-wrench / lever inset: a bolt with a wrench handle. `length`
# controls the handle reach; a push arrow shows the applied force.
# ----------------------------------------------------------------------
def wrench_lever(pos=ORIGIN, length=1.8, scale=1.0, color=CHALK,
                 push=True):
    bolt = VGroup(
        Circle(radius=0.16, fill_color=DIM, fill_opacity=1,
               stroke_color=CHALK, stroke_width=1.5),
        RegularPolygon(6, radius=0.16, color=CHALK, stroke_width=1.5),
    )
    handle = Rectangle(width=length, height=0.14, fill_color=color,
                       fill_opacity=1, stroke_color=WOOD_DARK,
                       stroke_width=1.5)
    handle.move_to(RIGHT * (length / 2.0))
    head = Circle(radius=0.20, color=color, stroke_width=4,
                  fill_opacity=0).move_to(ORIGIN)
    g = VGroup(bolt, handle, head)
    if push:
        a = Arrow([length, 0.45, 0], [length, 0.02, 0],
                  color=color, stroke_width=4, buff=0,
                  max_tip_length_to_length_ratio=0.5)
        g.add(a)
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# Balancing Act: a plank on a triangular fulcrum, mass bricks at marked
# distances, distance ticks, and a level indicator.
# `bricks` = list of (x_units, n_units) -> brick of n stacked units at
# x_units ticks from the fulcrum (negative = left).
# ----------------------------------------------------------------------
def balancing_act(pos=ORIGIN, half_w=3.6, bricks=None, tilt=0.0,
                  n_ticks=5, scale=1.0):
    if bricks is None:
        bricks = [(-3, 2), (2, 3)]
    plank = Rectangle(width=2 * half_w, height=0.20,
                      fill_color=WOOD, fill_opacity=1,
                      stroke_color=WOOD_DARK, stroke_width=2)
    plank.move_to(ORIGIN)

    # distance ticks along the plank
    ticks = VGroup()
    step = half_w / n_ticks
    for k in range(-n_ticks, n_ticks + 1):
        x = k * step
        tk = Line([x, -0.12, 0], [x, 0.12, 0],
                  color=(CHALK if k == 0 else DIM),
                  stroke_width=(3 if k == 0 else 1.5))
        ticks.add(tk)

    brick_grp = VGroup()
    for (xu, nu) in bricks:
        bx = xu * step
        col = LEFTC if xu < 0 else RIGHTC
        col = HEAVY if xu < 0 else RIGHTC
        stack = VGroup()
        for j in range(nu):
            r = Rectangle(width=0.46, height=0.28,
                          fill_color=col, fill_opacity=1,
                          stroke_color=CHALK, stroke_width=1.2)
            r.move_to([bx, 0.10 + 0.28 / 2 + j * 0.30, 0])
            stack.add(r)
        brick_grp.add(stack)

    beam = VGroup(plank, ticks, brick_grp)

    # the triangular fulcrum (does NOT rotate)
    ful = Polygon([-0.42, -0.10, 0], [0.42, -0.10, 0], [0.0, -1.05, 0],
                  fill_color=WOOD_DARK, fill_opacity=1,
                  stroke_color=CHALK, stroke_width=1.5)

    if abs(tilt) > 1e-6:
        beam.rotate(tilt, about_point=ORIGIN)

    grp = VGroup(ful, beam)
    grp.scale(scale).move_to(pos)
    info = {
        "group": grp, "beam": beam, "plank": plank, "fulcrum": ful,
        "ticks": ticks, "bricks": brick_grp, "step": step * scale,
        "half_w": half_w, "pivot": grp_pivot(grp, ORIGIN),
    }
    return info


def grp_pivot(grp, local):
    """Return world-space point for a local coordinate after transforms."""
    return grp.get_center()


def level_indicator(pos=ORIGIN, level=True, scale=1.0):
    """A small bubble-level style indicator: tube + bubble. Centered
    bubble = level; offset bubble = tilted."""
    tube = RoundedRectangle(corner_radius=0.12, width=1.5, height=0.34,
                            stroke_color=DIM, stroke_width=2,
                            fill_opacity=0)
    cx = 0.0 if level else 0.42
    bub = Circle(radius=0.12,
                 fill_color=(LEVEL_C if level else TILT_C),
                 fill_opacity=1, stroke_width=0)
    bub.move_to([cx, 0, 0])
    g1 = Line([-0.18, 0.20, 0], [-0.18, -0.20, 0],
              color=DIM, stroke_width=1.5)
    g2 = Line([0.18, 0.20, 0], [0.18, -0.20, 0],
              color=DIM, stroke_width=1.5)
    lbl = Text("level" if level else "tilted", font="sans",
               font_size=18, color=(LEVEL_C if level else TILT_C))
    g = VGroup(tube, g1, g2, bub)
    out = VGroup(g, lbl)
    lbl.next_to(g, DOWN, buff=0.14)
    out.scale(scale).move_to(pos)
    out.bubble = bub
    return out


def hand_hold(pos=ORIGIN, scale=1.0):
    """A simple hand deliberately holding the plank (not releasing)."""
    palm = RoundedRectangle(corner_radius=0.08, width=0.5, height=0.34,
                            fill_color=SKIN, fill_opacity=1,
                            stroke_color=WOOD_DARK, stroke_width=1.2)
    wrist = Line([0, -0.17, 0], [0, -0.55, 0], color=SKIN,
                 stroke_width=10)
    g = VGroup(wrist, palm).scale(scale).move_to(pos)
    return g


def play_button(pos=ORIGIN, r=0.40, color=CHALK, released=False):
    circ = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    if released:   # pause/hold glyph -> two bars
        b1 = Rectangle(width=r * 0.28, height=r * 0.9, color=color,
                       fill_opacity=1, stroke_width=0)
        b2 = b1.copy()
        b1.move_to(circ.get_center() + LEFT * r * 0.22)
        b2.move_to(circ.get_center() + RIGHT * r * 0.22)
        return VGroup(circ, b1, b2).move_to(pos)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    tri.scale(r * 0.55).rotate(-PI / 2)
    tri.move_to(circ.get_center() + RIGHT * r * 0.08)
    return VGroup(circ, tri).move_to(pos)


def run_counter(pos=ORIGIN, used=0, total=3):
    g = VGroup()
    for k in range(total):
        d = Circle(radius=0.12,
                   fill_color=(CHALK if k < used else VOID),
                   fill_opacity=(1 if k < used else 0),
                   stroke_color=DIM, stroke_width=2)
        d.move_to([k * 0.42, 0, 0])
        g.add(d)
    lbl = Text(f"{total} tries", font="sans", font_size=20, color=DIM)
    lbl.next_to(g, DOWN, buff=0.16)
    return VGroup(g, lbl).move_to(pos)


def predict_vs_result(pos=ORIGIN, pred=0.4, res=0.7):
    """Two short stacked bars: prediction vs the sim's result, with the
    difference marked."""
    base = Line(LEFT * 1.6, RIGHT * 1.6, color=DIM, stroke_width=2
                ).set_opacity(0.4)
    pbar = Rectangle(width=0.5, height=max(0.05, pred * 2.2),
                     fill_color=LEFTC, fill_opacity=1, stroke_width=0)
    rbar = Rectangle(width=0.5, height=max(0.05, res * 2.2),
                     fill_color=RIGHTC, fill_opacity=1, stroke_width=0)
    pbar.move_to(base.get_left() + RIGHT * 0.9 + UP * pbar.height / 2)
    rbar.move_to(base.get_right() + LEFT * 0.9 + UP * rbar.height / 2)
    pl = Text("predicted", font="sans", font_size=18, color=DIM
              ).next_to(pbar, DOWN, buff=0.14)
    rl = Text("result", font="sans", font_size=18, color=DIM
              ).next_to(rbar, DOWN, buff=0.14)
    return VGroup(base, pbar, rbar, pl, rl).move_to(pos)


# ----------------------------------------------------------------------
# The two faint callback icons — must echo the concept-video imagery.
#   wrench_bolt : a wrench on a bolt, short-vs-long handle (torque)
#   tumbling_wrench : a wrench tumbling, its CoM tracing a clean
#                     parabola (center of mass)
# Faint by default: they flicker in the void as memories.
# ----------------------------------------------------------------------
def callback_wrench_bolt(pos=ORIGIN, scale=1.0, opacity=0.85):
    short_w = wrench_lever([-1.5, 0.0, 0], length=1.0, scale=1.0,
                           color=HEAVY, push=True)
    long_w = wrench_lever([1.4, 0.0, 0], length=2.1, scale=1.0,
                          color=LIGHT, push=True)
    sl = Text("short", font="sans", font_size=16, color=DIM
              ).next_to(short_w, DOWN, buff=0.18)
    ll = Text("long", font="sans", font_size=16, color=DIM
              ).next_to(long_w, DOWN, buff=0.18)
    g = VGroup(short_w, long_w, sl, ll).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_tumbling_wrench(pos=ORIGIN, scale=1.0, opacity=0.85):
    # a smooth parabola the CoM follows
    pts = []
    for i in range(41):
        t = i / 40.0
        x = -2.2 + 4.4 * t
        y = 1.0 - 2.2 * (2 * t - 1) ** 2 + 0.4
        pts.append([x, y, 0])
    parab = VMobject()
    parab.set_points_as_corners(pts).make_smooth()
    parab.set_fill(opacity=0.0)
    parab.set_stroke(CHALK, width=2, opacity=0.55)

    # a simple wrench glyph tilted, mid-tumble
    handle = Rectangle(width=1.0, height=0.13, fill_color=DIM,
                       fill_opacity=1, stroke_color=CHALK,
                       stroke_width=1.2)
    jaw = RegularPolygon(6, radius=0.18, color=CHALK, stroke_width=1.5,
                         fill_opacity=0).move_to(LEFT * 0.5)
    wrench = VGroup(handle, jaw).rotate(0.5)
    wrench.move_to([0.0, 1.4, 0])

    com = Dot(point=[0.0, 1.4, 0], radius=0.07, color=COM_C)
    g = VGroup(parab, wrench, com).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    # re-assert: the parab is a stroke-only path (no dome fill), and the
    # wrench/com sit on the path's start after the group transform.
    parab.set_fill(opacity=0.0)
    parab.set_stroke(CHALK, width=2, opacity=0.55 * (opacity / 0.85
                                                     if opacity else 0))
    start_pt = parab.get_start()
    wrench.move_to(start_pt)
    com.move_to(start_pt)
    g.parab = parab
    g.wrench = wrench
    g.com = com
    return g


def small_label(text, pos, color=CHALK, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=48, color=DIM, opacity=0.6):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
