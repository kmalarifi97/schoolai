"""Helpers for the Spring-Drop Machine (springdrop) project-story.

A narrative: Yousef and a spring launcher that must tap a bell at an
exact height. Over- and undershoots; he rebuilds it in PhET Masses and
Springs and predicts-then-releases. The ending calls back to four
earlier concept videos: a drawn bow / loaded spring (elastic PE), a
book on a high shelf (gravitational PE), a rolling cart (kinetic
energy), and a swinging pendulum (conservation of mechanical energy).

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Warm, low-key palette — workbench, chalk, faint glows. No hype colors.
METAL    = "#9FB2C2"   # spring coil metal
METAL_DK = "#5E707E"   # spring shadow
BALL     = "#D8B48C"   # the launched ball
BALL_HVY = "#B98A5A"   # heavier-ball variant
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary
GUIDE    = "#5A5446"   # faint guide lines
TARGET   = "#7FB8E8"   # dotted target line (cool, calm)
BELL     = "#E8C46B"   # the bell (warm brass)
SHORT_C  = "#C98A6B"   # an undershoot arc (warm)
OVER_C   = "#9BD6B0"   # an overshoot arc
SPRING_E = "#7FB8E8"   # elastic / spring-stored (cool blue)
SPEED_E  = "#E8C46B"   # kinetic / speed (warm gold)
HEIGHT_E = "#9BD6B0"   # gravitational / height (green)
TOTAL    = "#EAE4D5"   # total energy (chalk)
SKIN     = "#D8B48C"
SHIRT    = "#6E8C9B"


# ----------------------------------------------------------------------
# Yousef — a minimal figure (head + torso + simple limbs). Low detail on
# purpose: he is a presence in the story, not a character study.
# ----------------------------------------------------------------------
def make_yousef(pos=ORIGIN, scale=1.0, facing=1):
    head = Circle(radius=0.16, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0)
    head.move_to(UP * 0.62)
    torso = Line(UP * 0.46, DOWN * 0.10, color=SHIRT, stroke_width=8)
    arm = Line(UP * 0.34, RIGHT * facing * 0.26 + DOWN * 0.02,
               color=SHIRT, stroke_width=6)
    leg1 = Line(DOWN * 0.10, DOWN * 0.62 + LEFT * 0.12,
                color=METAL_DK, stroke_width=6)
    leg2 = Line(DOWN * 0.10, DOWN * 0.62 + RIGHT * 0.12,
                color=METAL_DK, stroke_width=6)
    g = VGroup(head, torso, arm, leg1, leg2)
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# A vertical, compressible coil spring standing on a base plate.
# `compress` in [0,1] = how far it's pressed down (0 = relaxed).
# `height` = relaxed coil height. Returns a dict so beats can reach the
# top of the coil (where the ball sits) precisely.
# ----------------------------------------------------------------------
def make_spring(pos=ORIGIN, height=1.6, compress=0.0, coils=7,
                width=0.7):
    compress = float(np.clip(compress, 0.0, 0.85))
    base_y = pos[1]
    coil_h = height * (1.0 - compress)
    plate = Line([pos[0] - 0.55, base_y, 0],
                 [pos[0] + 0.55, base_y, 0],
                 color=METAL_DK, stroke_width=6)
    pts = []
    n = coils * 12
    for i in range(n + 1):
        t = i / n
        y = base_y + t * coil_h
        x = pos[0] + (width / 2) * np.sin(t * coils * 2 * np.pi)
        pts.append([x, y, 0])
    coil = VMobject()
    coil.set_points_as_corners(pts)
    coil.set_stroke(METAL, width=3)
    top = np.array([pos[0], base_y + coil_h, 0])
    grp = VGroup(plate, coil)
    info = {"group": grp, "top": top, "base_y": base_y,
            "coil": coil, "plate": plate, "compress": compress,
            "coil_h": coil_h, "x": pos[0]}
    return info


def make_ball(pos=ORIGIN, r=0.22, heavy=False):
    c = BALL_HVY if heavy else BALL
    ball = Circle(radius=r, fill_color=c, fill_opacity=1,
                  stroke_color=CHALK, stroke_width=1.5)
    ball.move_to(pos)
    if heavy:
        # a denser glint to read as "heavier"
        ball.set_stroke(CHALK, width=2.5)
    return ball


# ----------------------------------------------------------------------
# The bell, hung at a fixed height above the launcher.
# ----------------------------------------------------------------------
def make_bell(pos=ORIGIN, scale=1.0):
    body = ArcPolygon(
        [-0.30, 0.0, 0], [-0.22, 0.34, 0], [0.0, 0.46, 0],
        [0.22, 0.34, 0], [0.30, 0.0, 0],
        arc_config=[{"angle": -0.5}, {"angle": -0.4},
                    {"angle": -0.4}, {"angle": -0.5},
                    {"angle": 0.0}],
        fill_color=BELL, fill_opacity=1,
        stroke_color=CHALK, stroke_width=2)
    rim = Line([-0.32, 0.0, 0], [0.32, 0.0, 0], color=CHALK,
               stroke_width=3)
    clapper = Dot([0, -0.06, 0], radius=0.05, color=CHALK)
    mount = Line([0, 0.46, 0], [0, 0.72, 0], color=DIM,
                 stroke_width=3)
    g = VGroup(mount, body, rim, clapper).scale(scale).move_to(pos)
    return g


def target_line(y, x0=-5.5, x1=5.5, color=TARGET):
    """The dotted target line at the bell's height."""
    ln = DashedLine([x0, y, 0], [x1, y, 0], color=color,
                    stroke_width=2.5, dash_length=0.18)
    ln.set_opacity(0.7)
    return ln


# ----------------------------------------------------------------------
# A projectile arc for the ball: straight up from `start` to an apex
# `apex_y`, then back down. Stroke-only open path.
# ----------------------------------------------------------------------
def rise_path(start, apex_y, color=SHORT_C, width=4, n=60,
              fall=True):
    start = np.array(start, dtype=float)
    x = start[0]
    pts = []
    span = apex_y - start[1]
    up_n = n // 2
    for i in range(up_n + 1):
        t = i / up_n
        y = start[1] + span * (1 - (1 - t) ** 2)
        pts.append([x, y, 0])
    if fall:
        for i in range(1, up_n + 1):
            t = i / up_n
            y = apex_y - span * (t ** 2)
            pts.append([x, y, 0])
    path = VMobject()
    path.set_points_as_corners(pts)
    path.set_stroke(color, width=width)
    return path


# ----------------------------------------------------------------------
# Energy-chain bars: spring-stored -> speed -> height, with constant
# total. `stage` in 0..1 sweeps the energy along the chain. Returns a
# VGroup of three labelled bars.
# ----------------------------------------------------------------------
def energy_bar(label, frac, pos, color=SPRING_E, max_h=2.6, w=0.62,
               show_label=True):
    frac = float(np.clip(frac, 0.0, 1.0))
    track = Rectangle(width=w, height=max_h, stroke_color=DIM,
                      stroke_width=1.5, fill_opacity=0).set_opacity(0.5)
    fill_h = max(0.001, frac * max_h)
    fill = Rectangle(width=w, height=fill_h, stroke_width=0,
                     fill_color=color, fill_opacity=1)
    fill.move_to(track.get_bottom() + UP * fill_h / 2)
    grp = VGroup(track, fill)
    grp.move_to(pos)
    out = VGroup(grp)
    if show_label:
        lbl = Text(label, font="sans", font_size=20, color=DIM)
        lbl.next_to(grp, DOWN, buff=0.18)
        out.add(lbl)
    out.bar_fill = fill
    out.bar_track = track
    return out


def energy_chain(pos=ORIGIN, stage=0.0, heavy=False, scale=1.0):
    """Three bars in a chain: spring -> motion -> height. The total is
    constant; `stage` 0->1 hands the energy along. `heavy` shrinks the
    height bar to show the same total buying less height."""
    stage = float(np.clip(stage, 0.0, 1.0))
    # spring full at stage 0, empties by stage 0.5
    spring = max(0.0, 1.0 - min(1.0, stage / 0.5))
    # speed peaks around stage 0.5
    speed = max(0.0, 1.0 - abs(stage - 0.5) / 0.5)
    # height fills from stage 0.5 -> 1.0
    raw_h = max(0.0, (stage - 0.5) / 0.5)
    height = raw_h * (0.6 if heavy else 1.0)
    xs = [-1.4, 0.0, 1.4]
    bars = VGroup(
        energy_bar("spring", spring, [xs[0], 0, 0], color=SPRING_E,
                   max_h=2.4, w=0.55),
        energy_bar("speed", speed, [xs[1], 0, 0], color=SPEED_E,
                   max_h=2.4, w=0.55),
        energy_bar("height", height, [xs[2], 0, 0], color=HEIGHT_E,
                   max_h=2.4, w=0.55),
    )
    # the arrows of the chain
    a1 = Arrow([xs[0] + 0.45, 0.1, 0], [xs[1] - 0.45, 0.1, 0],
               color=DIM, stroke_width=3, buff=0,
               max_tip_length_to_length_ratio=0.25).set_opacity(0.6)
    a2 = Arrow([xs[1] + 0.45, 0.1, 0], [xs[2] - 0.45, 0.1, 0],
               color=DIM, stroke_width=3, buff=0,
               max_tip_length_to_length_ratio=0.25).set_opacity(0.6)
    out = VGroup(bars, a1, a2).scale(scale).move_to(pos)
    out.bars = bars
    return out


# ----------------------------------------------------------------------
# A faint ledger — empty rows waiting to be filled (the missing account).
# ----------------------------------------------------------------------
def ledger(pos=ORIGIN, rows=4, w=3.4, scale=1.0):
    frame = Rectangle(width=w, height=rows * 0.5 + 0.4,
                      stroke_color=DIM, stroke_width=1.5,
                      fill_opacity=0).set_opacity(0.45)
    g = VGroup(frame)
    top = frame.get_top()[1]
    for k in range(rows):
        y = top - 0.45 - k * 0.5
        ln = Line([-w / 2 + 0.2, y, 0], [w / 2 - 0.2, y, 0],
                  color=GUIDE, stroke_width=2).set_opacity(0.5)
        g.add(ln)
    out = VGroup(g).scale(scale).move_to(pos)
    return out


# ----------------------------------------------------------------------
# PhET Masses-and-Springs layout: a spring + hanging mass + stiffness /
# mass controls + an elastic/kinetic/gravitational/total bar chart.
# ----------------------------------------------------------------------
def slider(pos=ORIGIN, frac=0.5, w=2.4, label="stiffness"):
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


def hanging_spring(pos=ORIGIN, stretch=0.6, coils=6, width=0.55):
    """A spring hanging from a top bracket with a mass on the end."""
    top_y = pos[1]
    bracket = Line([pos[0] - 0.6, top_y, 0],
                   [pos[0] + 0.6, top_y, 0],
                   color=METAL_DK, stroke_width=6)
    coil_h = 1.4 + stretch * 1.2
    pts = []
    n = coils * 12
    for i in range(n + 1):
        t = i / n
        y = top_y - t * coil_h
        x = pos[0] + (width / 2) * np.sin(t * coils * 2 * np.pi)
        pts.append([x, y, 0])
    coil = VMobject()
    coil.set_points_as_corners(pts)
    coil.set_stroke(METAL, width=3)
    mass = Square(side_length=0.5, fill_color=BALL, fill_opacity=1,
                  stroke_color=CHALK, stroke_width=1.5)
    mass.move_to([pos[0], top_y - coil_h - 0.25, 0])
    g = VGroup(bracket, coil, mass)
    info = {"group": g, "mass": mass, "coil": coil,
            "bottom_y": top_y - coil_h - 0.5}
    return info


def masses_springs_panel(pos=ORIGIN, stiffness=0.5, mass=0.5,
                          elastic=0.7, kinetic=0.2, grav=0.1,
                          scale=1.0):
    """Full Masses-and-Springs layout: hanging spring+mass on the left,
    stiffness/mass sliders, and an elastic/kinetic/gravitational/total
    bar chart on the right."""
    hs = hanging_spring([-3.2, 1.9, 0], stretch=mass)
    spring_grp = hs["group"]
    s1 = slider([-3.2, -1.7, 0], frac=stiffness, w=2.2,
                label="stiffness")
    s2 = slider([-3.2, -2.6, 0], frac=mass, w=2.2, label="mass")

    total = min(1.0, elastic + kinetic + grav)
    xs = [-0.6, 0.4, 1.4, 2.4]
    cols = [SPRING_E, SPEED_E, HEIGHT_E, TOTAL]
    labs = ["elas", "kin", "grav", "tot"]
    vals = [elastic, kinetic, grav, total]
    bars = VGroup()
    for x, c, lab, v in zip(xs, cols, labs, vals):
        b = energy_bar(lab, v, [x, 0.2, 0], color=c, max_h=2.4, w=0.5)
        bars.add(b)
    frame = Rectangle(width=4.0, height=3.3, stroke_color=DIM,
                      stroke_width=1.5, fill_opacity=0).set_opacity(0.4)
    frame.move_to(bars.get_center())
    chart = VGroup(frame, bars)
    panel = VGroup(spring_grp, s1, s2, chart)
    panel.scale(scale).move_to(pos)
    panel.bars = bars
    panel.spring = spring_grp
    panel.hs = hs
    return panel


# ----------------------------------------------------------------------
# Hold/release hand — a simple hand shape holding (or releasing) the
# compressed spring.
# ----------------------------------------------------------------------
def hold_hand(pos=ORIGIN, scale=1.0, open_hand=False):
    palm = RoundedRectangle(corner_radius=0.08, width=0.7, height=0.34,
                            fill_color=SKIN, fill_opacity=1,
                            stroke_color=METAL_DK, stroke_width=1.5)
    g = VGroup(palm)
    if not open_hand:
        for k in range(3):
            f = RoundedRectangle(corner_radius=0.04, width=0.16,
                                 height=0.26, fill_color=SKIN,
                                 fill_opacity=1, stroke_width=0)
            f.next_to(palm, UP, buff=0.0).shift(RIGHT * (k - 1) * 0.2)
            g.add(f)
    wrist = Line(palm.get_bottom(), palm.get_bottom() + DOWN * 0.4,
                 color=SKIN, stroke_width=8)
    g.add(wrist)
    g.scale(scale).move_to(pos)
    return g


def compression_control(pos=ORIGIN, frac=0.5, w=2.6):
    """A labelled control for how far the spring is compressed."""
    return slider(pos=pos, frac=frac, w=w, label="compression")


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
    """Two short stacked bars: prediction vs the sim's result."""
    base = Line(LEFT * 1.6, RIGHT * 1.6, color=DIM, stroke_width=2
                ).set_opacity(0.4)
    pbar = Rectangle(width=0.5, height=max(0.05, pred * 2.2),
                     fill_color=TARGET, fill_opacity=1, stroke_width=0)
    rbar = Rectangle(width=0.5, height=max(0.05, res * 2.2),
                     fill_color=OVER_C, fill_opacity=1, stroke_width=0)
    pbar.move_to(base.get_left() + RIGHT * 0.9 + UP * pbar.height / 2)
    rbar.move_to(base.get_right() + LEFT * 0.9 + UP * rbar.height / 2)
    pl = Text("predicted", font="sans", font_size=18, color=DIM
              ).next_to(pbar, DOWN, buff=0.14)
    rl = Text("result", font="sans", font_size=18, color=DIM
              ).next_to(rbar, DOWN, buff=0.14)
    return VGroup(base, pbar, rbar, pl, rl).move_to(pos)


# ----------------------------------------------------------------------
# The four faint callback icons — must echo the concept-video imagery.
#   bow  : a drawn bow / loaded spring (elastic PE)
#   book : a book sitting on a shelf  (gravitational PE)
#   cart : a small rolling cart       (kinetic energy)
#   pend : a swinging pendulum        (conservation of mech. energy)
# Faint by default: they flicker in the void as memories.
# ----------------------------------------------------------------------
def callback_bow(pos=ORIGIN, scale=1.0, opacity=0.85):
    # a drawn bow: a curved limb, a string pulled back, an arrow nocked
    bow = Arc(radius=0.8, start_angle=-PI / 2.4, angle=PI / 1.2,
              color=BALL_HVY, stroke_width=5)
    top = bow.get_start()
    bot = bow.get_end()
    nock = np.array([(top[0] + bot[0]) / 2 - 0.55,
                     (top[1] + bot[1]) / 2, 0])
    string = VMobject()
    string.set_points_as_corners([top, nock, bot])
    string.set_stroke(CHALK, width=2)
    arrow = Arrow(nock, nock + RIGHT * 1.0, color=CHALK,
                  stroke_width=4, buff=0,
                  max_tip_length_to_length_ratio=0.3)
    g = VGroup(bow, string, arrow).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_book(pos=ORIGIN, scale=1.0, opacity=0.85):
    shelf = Line(LEFT * 0.9, RIGHT * 0.9, color=METAL_DK,
                 stroke_width=4)
    cover = Rectangle(width=0.34, height=0.62, fill_color=SPRING_E,
                      fill_opacity=1, stroke_color=CHALK,
                      stroke_width=1.5)
    spine = Line(cover.get_corner(UL), cover.get_corner(DL),
                 color=CHALK, stroke_width=2)
    book = VGroup(cover, spine)
    book.next_to(shelf, UP, buff=0.0).shift(LEFT * 0.2)
    g = VGroup(shelf, book).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_cart(pos=ORIGIN, scale=1.0, opacity=0.85):
    body = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.4,
                            fill_color=SPEED_E, fill_opacity=1,
                            stroke_color=CHALK, stroke_width=1.5)
    w1 = Circle(radius=0.13, fill_color=METAL_DK, fill_opacity=1,
                stroke_color=CHALK, stroke_width=1.5)
    w2 = w1.copy()
    w1.move_to(body.get_corner(DL) + RIGHT * 0.22 + DOWN * 0.06)
    w2.move_to(body.get_corner(DR) + LEFT * 0.22 + DOWN * 0.06)
    arrow = Arrow(body.get_right() + RIGHT * 0.05,
                  body.get_right() + RIGHT * 0.6,
                  color=CHALK, stroke_width=4, buff=0,
                  max_tip_length_to_length_ratio=0.4)
    g = VGroup(body, w1, w2, arrow).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_pendulum(pos=ORIGIN, scale=1.0, opacity=0.85,
                       theta=0.5):
    pivot = Dot(radius=0.05, color=CHALK)
    L = 0.95
    bob_pos = np.array([L * np.sin(theta), -L * np.cos(theta), 0])
    rod = Line(ORIGIN, bob_pos, color=DIM, stroke_width=2)
    bob = Circle(radius=0.15, fill_color=HEIGHT_E, fill_opacity=1,
                 stroke_color=CHALK, stroke_width=1.5).move_to(bob_pos)
    arc = Arc(radius=L, start_angle=-PI / 2 - theta,
              angle=2 * theta, color=DIM, stroke_width=1.5
              ).set_opacity(0.4)
    g = VGroup(pivot, rod, bob, arc).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def small_label(text, pos, color=CHALK, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=48, color=DIM, opacity=0.6):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
