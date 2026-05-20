"""Helpers for the Collision Forensics (collisionlab) project-story.

A narrative: Noura, two toy carts, a dent, an argument with her little
brother — "who was really going faster?". She rebuilds the crash in PhET
Collision Lab, predicts-then-runs, then the ending calls back to three
earlier concept videos (cars at a wall, frozen-lake bag throw, steel vs
clay).

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Warm, low-key palette — table wood, chalk, faint glows. No hype colors.
WOOD     = "#C9A66B"   # table / cart body warm
WOOD_DK  = "#8A6E40"   # edge / shadow
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary
GAP_LINE = "#5A5446"
COOL     = "#7FB8E8"   # conserved / steady (cool blue)
GOLD     = "#E8C46B"   # speed / motion energy (warm gold)
GREEN    = "#9BD6B0"   # "after" / good
WARM     = "#C98A6B"   # dent / damage warm
HEAT     = "#D98C5F"   # thermal / heat
TOTAL    = "#EAE4D5"   # total (chalk)
SKIN     = "#D8B48C"
SHIRT_N  = "#6E8C9B"   # Noura's shirt (cool)
SHIRT_B  = "#B07A55"   # brother's shirt (warm)
STEEL    = "#AEB6BD"   # steel sphere
CLAY     = "#B07A55"   # clay
ICE      = "#9FB9C9"   # frozen lake


# ----------------------------------------------------------------------
# Noura — a minimal figure (head + torso + simple limbs). Low detail on
# purpose: she is a presence in the story, not a character study.
# `facing` = +1 looks/points right, -1 left.
# ----------------------------------------------------------------------
def make_noura(pos=ORIGIN, scale=1.0, facing=1):
    head = Circle(radius=0.17, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0).move_to(UP * 0.64)
    torso = Line(UP * 0.47, DOWN * 0.10, color=SHIRT_N, stroke_width=8)
    arm = Line(UP * 0.34, RIGHT * facing * 0.30 + DOWN * 0.04,
               color=SHIRT_N, stroke_width=6)
    leg1 = Line(DOWN * 0.10, DOWN * 0.64 + LEFT * 0.12,
                color=WOOD_DK, stroke_width=6)
    leg2 = Line(DOWN * 0.10, DOWN * 0.64 + RIGHT * 0.12,
                color=WOOD_DK, stroke_width=6)
    g = VGroup(head, torso, arm, leg1, leg2)
    g.scale(scale).move_to(pos)
    return g


# Little brother — smaller, warmer shirt.
def make_brother(pos=ORIGIN, scale=1.0, facing=-1):
    head = Circle(radius=0.14, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0).move_to(UP * 0.50)
    torso = Line(UP * 0.36, DOWN * 0.06, color=SHIRT_B, stroke_width=7)
    arm = Line(UP * 0.26, RIGHT * facing * 0.26 + UP * 0.04,
               color=SHIRT_B, stroke_width=5)
    leg1 = Line(DOWN * 0.06, DOWN * 0.50 + LEFT * 0.10,
                color=WOOD_DK, stroke_width=5)
    leg2 = Line(DOWN * 0.06, DOWN * 0.50 + RIGHT * 0.10,
                color=WOOD_DK, stroke_width=5)
    g = VGroup(head, torso, arm, leg1, leg2)
    g.scale(scale * 0.82).move_to(pos)
    return g


# ----------------------------------------------------------------------
# A toy cart: a rounded body + two wheels. `dented=True` puts a visible
# crumple notch in the front-right face. `color` lets the two carts read
# as distinct objects.
# ----------------------------------------------------------------------
def make_cart(pos=ORIGIN, scale=1.0, color=WOOD, dented=False,
              facing=1):
    body = RoundedRectangle(corner_radius=0.10, width=1.30, height=0.62,
                            fill_color=color, fill_opacity=1,
                            stroke_color=WOOD_DK, stroke_width=2)
    parts = VGroup(body)
    if dented:
        # a crushed notch on the leading (facing) edge
        ex = facing * 0.55
        dent = Polygon(
            [ex, 0.22, 0], [ex - facing * 0.26, 0.05, 0],
            [ex, -0.04, 0], [ex - facing * 0.22, -0.20, 0],
            [ex, -0.28, 0],
            fill_color=VOID, fill_opacity=1,
            stroke_color=WARM, stroke_width=2.5)
        parts.add(dent)
        crease = Line([ex - facing * 0.30, 0.18, 0],
                      [ex - facing * 0.10, -0.16, 0],
                      color=WARM, stroke_width=2).set_opacity(0.8)
        parts.add(crease)
    w1 = Circle(radius=0.15, fill_color=WOOD_DK, fill_opacity=1,
                stroke_color=CHALK, stroke_width=1.5)
    w2 = w1.copy()
    w1.move_to(body.get_corner(DL) + RIGHT * 0.30 + DOWN * 0.05)
    w2.move_to(body.get_corner(DR) + LEFT * 0.30 + DOWN * 0.05)
    parts.add(w1, w2)
    parts.scale(scale).move_to(pos)
    parts.body = body
    return parts


def table_line(y=-2.3, color=GAP_LINE, w=12.0):
    return Line([-w / 2, y, 0], [w / 2, y, 0],
                color=color, stroke_width=2).set_opacity(0.55)


# ----------------------------------------------------------------------
# Clue icons — each a small glyph + an optional ✗ to mark "lies alone".
#   dent  : a crumpled chevron
#   slide : a short skid trail with arrow
#   sound : concentric sound arcs
# ----------------------------------------------------------------------
def _x_mark(scale=1.0, color=WARM):
    a = Line([-0.16, 0.16, 0], [0.16, -0.16, 0],
             color=color, stroke_width=4)
    b = Line([-0.16, -0.16, 0], [0.16, 0.16, 0],
             color=color, stroke_width=4)
    return VGroup(a, b).scale(scale)


def clue_dent(pos=ORIGIN, scale=1.0, crossed=False):
    chev = VMobject().set_points_as_corners([
        [-0.28, 0.22, 0], [-0.02, -0.05, 0], [-0.20, -0.05, 0],
        [0.10, -0.30, 0]]).set_stroke(WARM, width=4)
    g = VGroup(chev)
    if crossed:
        x = _x_mark(0.9).move_to([0.05, 0.30, 0])
        g.add(x)
    g.scale(scale).move_to(pos)
    return g


def clue_slide(pos=ORIGIN, scale=1.0, crossed=False):
    trail = DashedLine([-0.36, -0.16, 0], [0.18, -0.16, 0],
                       color=DIM, stroke_width=3, dash_length=0.07)
    arr = Arrow([0.10, -0.16, 0], [0.40, -0.16, 0], color=CHALK,
                stroke_width=4, buff=0,
                max_tip_length_to_length_ratio=0.5)
    g = VGroup(trail, arr)
    if crossed:
        g.add(_x_mark(0.9).move_to([0.02, 0.18, 0]))
    g.scale(scale).move_to(pos)
    return g


def clue_sound(pos=ORIGIN, scale=1.0, crossed=False):
    g = VGroup()
    for k, rad in enumerate([0.14, 0.26, 0.38]):
        a = Arc(radius=rad, start_angle=-PI / 3, angle=2 * PI / 3,
                color=COOL, stroke_width=3).set_opacity(0.8 - k * 0.2)
        g.add(a)
    dot = Dot([-0.30, 0, 0], radius=0.05, color=CHALK)
    g.add(dot)
    if crossed:
        g.add(_x_mark(0.9).move_to([0.06, 0.34, 0]))
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# Fixed-length total-momentum bar: a single bar that stays the SAME
# length before and after the impact. Optionally split into two colored
# segments (cart A | cart B) whose split point shifts but total length is
# invariant.
# ----------------------------------------------------------------------
def momentum_bar(pos=ORIGIN, length=4.6, split=0.5, label=None,
                 colA=COOL, colB=GOLD, h=0.34):
    track = Rectangle(width=length, height=h, stroke_color=DIM,
                      stroke_width=1.5, fill_opacity=0).set_opacity(0.5)
    split = float(np.clip(split, 0.05, 0.95))
    la = length * split
    lb = length - la
    segA = Rectangle(width=max(0.01, la), height=h, stroke_width=0,
                     fill_color=colA, fill_opacity=1)
    segB = Rectangle(width=max(0.01, lb), height=h, stroke_width=0,
                     fill_color=colB, fill_opacity=1)
    segA.move_to(track.get_left() + RIGHT * la / 2)
    segB.move_to(track.get_right() + LEFT * lb / 2)
    grp = VGroup(track, segA, segB)
    out = VGroup(grp)
    if label:
        lbl = Text(label, font="sans", font_size=20, color=DIM)
        lbl.next_to(grp, DOWN, buff=0.18)
        out.add(lbl)
    out.move_to(pos)
    out.seg_a = segA
    out.seg_b = segB
    out.track = track
    return out


# ----------------------------------------------------------------------
# Motion-energy bar — a vertical bar that can SHRINK at impact. The lost
# part can be shown as a faint dent+sound+heat shimmer.
# ----------------------------------------------------------------------
def energy_bar(label, frac, pos, color=GOLD, max_h=2.6, w=0.62,
               show_label=True):
    frac = float(np.clip(frac, 0.0, 1.0))
    track = Rectangle(width=w, height=max_h, stroke_color=DIM,
                      stroke_width=1.5, fill_opacity=0).set_opacity(0.5)
    fill_h = max(0.001, frac * max_h)
    fill = Rectangle(width=w, height=fill_h, stroke_width=0,
                     fill_color=color, fill_opacity=1)
    fill.move_to(track.get_bottom() + UP * fill_h / 2)
    grp = VGroup(track, fill).move_to(pos)
    out = VGroup(grp)
    if show_label:
        lbl = Text(label, font="sans", font_size=20, color=DIM)
        lbl.next_to(grp, DOWN, buff=0.18)
        out.add(lbl)
    out.bar_fill = fill
    out.bar_track = track
    return out


def loss_shimmer(pos=ORIGIN, scale=1.0):
    """The lost motion energy: dent + sound + heat shimmer."""
    d = clue_dent([-0.55, 0, 0], scale=0.7)
    s = clue_sound([0.05, 0, 0], scale=0.6)
    waves = VGroup()
    for k in range(3):
        ln = Line([0.45, -0.18 + k * 0.16, 0],
                  [0.95, -0.10 + k * 0.16, 0],
                  color=HEAT, stroke_width=3).set_opacity(0.7)
        waves.add(ln)
    g = VGroup(d, s, waves).scale(scale).move_to(pos)
    g.set_opacity(0.8)
    return g


# ----------------------------------------------------------------------
# Collision Lab layout: two pucks on a track + momentum vector arrows +
# a KE readout box.
# ----------------------------------------------------------------------
def cl_track(pos=ORIGIN, w=8.0):
    rail = Line([-w / 2, 0, 0], [w / 2, 0, 0], color=DIM,
                stroke_width=3).set_opacity(0.55)
    ticks = VGroup()
    for x in np.linspace(-w / 2, w / 2, 9):
        ticks.add(Line([x, -0.08, 0], [x, 0.08, 0], color=DIM,
                        stroke_width=2).set_opacity(0.4))
    g = VGroup(rail, ticks).move_to(pos)
    g.rail = rail
    return g


def cl_puck(pos=ORIGIN, r=0.34, color=COOL, mass="m"):
    disc = Circle(radius=r, fill_color=color, fill_opacity=1,
                  stroke_color=CHALK, stroke_width=2)
    lbl = Text(mass, font="sans", font_size=20, color=VOID)
    lbl.move_to(disc.get_center())
    g = VGroup(disc, lbl).move_to(pos)
    g.disc = disc
    return g


def momentum_arrow(start, dx, color=GOLD, width=5):
    start = np.array(start, dtype=float)
    end = start + np.array([dx, 0, 0])
    return Arrow(start, end, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.28)


def ke_readout(pos=ORIGIN, value="KE = 1.00 J", scale=1.0):
    box = Rectangle(width=2.7, height=0.74, stroke_color=DIM,
                    stroke_width=1.5, fill_opacity=0).set_opacity(0.5)
    txt = Text(value, font="sans", font_size=22, color=CHALK)
    txt.move_to(box.get_center())
    g = VGroup(box, txt).scale(scale).move_to(pos)
    g.value_text = txt
    g.box = box
    return g


def play_button(pos=ORIGIN, r=0.42, color=CHALK):
    circ = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    tri.scale(r * 0.55).rotate(-PI / 2)
    tri.move_to(circ.get_center() + RIGHT * r * 0.08)
    return VGroup(circ, tri).move_to(pos)


def mass_slider(pos=ORIGIN, frac=0.5, w=2.8, label="mass"):
    rail = Line(LEFT * w / 2, RIGHT * w / 2, color=DIM, stroke_width=3
                ).set_opacity(0.6)
    knob = Circle(radius=0.12, fill_color=CHALK, fill_opacity=1,
                  stroke_width=0)
    knob.move_to(LEFT * w / 2 + RIGHT * w * float(np.clip(frac, 0, 1)))
    grp = VGroup(rail, knob)
    lbl = Text(label, font="sans", font_size=20, color=DIM)
    lbl.next_to(grp, DOWN, buff=0.16)
    out = VGroup(grp, lbl).move_to(pos)
    out.knob = knob
    out.rail = rail
    return out


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


def predict_vs_result(pos=ORIGIN, pred=0.4, res=0.7):
    """Two short bars: prediction vs the sim's result."""
    base = Line(LEFT * 1.6, RIGHT * 1.6, color=DIM, stroke_width=2
                ).set_opacity(0.4)
    pbar = Rectangle(width=0.5, height=max(0.05, pred * 2.2),
                     fill_color=COOL, fill_opacity=1, stroke_width=0)
    rbar = Rectangle(width=0.5, height=max(0.05, res * 2.2),
                     fill_color=GREEN, fill_opacity=1, stroke_width=0)
    pbar.move_to(base.get_left() + RIGHT * 0.9 + UP * pbar.height / 2)
    rbar.move_to(base.get_right() + LEFT * 0.9 + UP * rbar.height / 2)
    pl = Text("predicted", font="sans", font_size=18, color=DIM
              ).next_to(pbar, DOWN, buff=0.14)
    rl = Text("result", font="sans", font_size=18, color=DIM
              ).next_to(rbar, DOWN, buff=0.14)
    return VGroup(base, pbar, rbar, pl, rl).move_to(pos)


# ----------------------------------------------------------------------
# The three faint callback icons — must echo the concept-video imagery.
#   cars_wall : two cars at a wall, one crumpling slowly, one rigid
#   lake_throw: a figure on a frozen lake who threw a bag and slid back
#   steel_clay: steel spheres rebounding vs clay fusing
# Faint by default: they flicker in the void as memories.
# ----------------------------------------------------------------------
def callback_cars_wall(pos=ORIGIN, scale=1.0, opacity=0.85):
    wall = Line([0, -0.6, 0], [0, 0.6, 0], color=DIM, stroke_width=5)
    # rigid car (top): square nose, no crumple
    rigid = RoundedRectangle(corner_radius=0.05, width=0.8, height=0.34,
                             fill_color=STEEL, fill_opacity=1,
                             stroke_color=CHALK, stroke_width=1.5)
    rigid.move_to([-0.55, 0.32, 0])
    rw1 = Circle(radius=0.07, fill_color=WOOD_DK, fill_opacity=1,
                 stroke_width=0).move_to(rigid.get_corner(DL) + RIGHT * 0.16)
    rw2 = rw1.copy().move_to(rigid.get_corner(DR) + LEFT * 0.16)
    # crumpled car (bottom): a notched nose near the wall
    crum = Polygon([-0.95, -0.14, 0], [-0.95, -0.50, 0],
                   [-0.20, -0.50, 0], [-0.34, -0.32, 0],
                   [-0.20, -0.14, 0],
                   fill_color=CLAY, fill_opacity=1,
                   stroke_color=WARM, stroke_width=1.5)
    cw1 = Circle(radius=0.07, fill_color=WOOD_DK, fill_opacity=1,
                 stroke_width=0).move_to([-0.78, -0.54, 0])
    cw2 = cw1.copy().move_to([-0.40, -0.54, 0])
    g = VGroup(wall, rigid, rw1, rw2, crum, cw1, cw2)
    g.scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_lake_throw(pos=ORIGIN, scale=1.0, opacity=0.85):
    ice = Line([-1.0, -0.5, 0], [1.0, -0.5, 0], color=ICE,
               stroke_width=4).set_opacity(0.7)
    # figure leaning back
    head = Circle(radius=0.10, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0).move_to([-0.45, 0.30, 0])
    body = Line([-0.45, 0.20, 0], [-0.55, -0.45, 0], color=SHIRT_N,
                stroke_width=6)
    arm = Line([-0.48, 0.05, 0], [-0.15, 0.18, 0], color=SHIRT_N,
               stroke_width=5)
    # thrown bag + its arrow (forward), figure's recoil arrow (back)
    bag = RoundedRectangle(corner_radius=0.04, width=0.26, height=0.22,
                           fill_color=WOOD, fill_opacity=1,
                           stroke_color=CHALK, stroke_width=1.5)
    bag.move_to([0.30, 0.20, 0])
    fwd = Arrow([0.45, 0.20, 0], [0.85, 0.20, 0], color=GOLD,
                stroke_width=4, buff=0,
                max_tip_length_to_length_ratio=0.5)
    back = Arrow([-0.60, -0.20, 0], [-0.95, -0.20, 0], color=COOL,
                 stroke_width=4, buff=0,
                 max_tip_length_to_length_ratio=0.5)
    g = VGroup(ice, head, body, arm, bag, fwd, back)
    g.scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_steel_clay(pos=ORIGIN, scale=1.0, opacity=0.85):
    # top: two steel spheres rebounding (apart, with arrows)
    s1 = Circle(radius=0.16, fill_color=STEEL, fill_opacity=1,
                stroke_color=CHALK, stroke_width=1.5).move_to(
        [-0.40, 0.34, 0])
    s2 = s1.copy().move_to([0.40, 0.34, 0])
    a1 = Arrow([-0.55, 0.34, 0], [-0.90, 0.34, 0], color=GREEN,
               stroke_width=3, buff=0,
               max_tip_length_to_length_ratio=0.6)
    a2 = Arrow([0.55, 0.34, 0], [0.90, 0.34, 0], color=GREEN,
               stroke_width=3, buff=0,
               max_tip_length_to_length_ratio=0.6)
    # bottom: two clay blobs fused into one, stopped
    fused = VGroup(
        Circle(radius=0.17, fill_color=CLAY, fill_opacity=1,
               stroke_color=WARM, stroke_width=1.5).move_to(
            [-0.10, -0.34, 0]),
        Circle(radius=0.17, fill_color=CLAY, fill_opacity=1,
               stroke_color=WARM, stroke_width=1.5).move_to(
            [0.12, -0.34, 0]))
    stop = Line([0.34, -0.50, 0], [0.34, -0.18, 0], color=DIM,
                stroke_width=3).set_opacity(0.7)
    g = VGroup(s1, s2, a1, a2, fused, stop)
    g.scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def small_label(text, pos, color=CHALK, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=48, color=DIM, opacity=0.6):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
