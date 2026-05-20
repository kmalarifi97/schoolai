"""Helpers for the Skatepark Energy Audit (skatepark) project-story.

A narrative: Faris and a plywood ramp that "keeps lying to him". He takes
it to PhET Energy Skate Park, predicts-then-runs, then the ending calls
back to three earlier concept videos (book on a shelf, rolling cart,
swinging pendulum).

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Warm, low-key palette — wood, chalk, faint glows. No hype colors.
PLY      = "#C9A66B"   # plywood face
PLY_DARK = "#8A6E40"   # plywood edge / shadow
PLY_FAINT= "#6E5A38"
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary
GAP_LINE = "#5A5446"
IDEAL    = "#7FB8E8"   # ideal dotted arc (cool, calm)
FAIL_ARC = "#C98A6B"   # an attempt arc (warm)
WAX_ARC  = "#9BD6B0"   # waxed run arc
HEAT     = "#D98C5F"   # thermal / heat
STORED   = "#7FB8E8"   # potential / stored (cool blue)
SPEED    = "#E8C46B"   # kinetic / speed (warm gold)
TOTAL    = "#EAE4D5"   # total energy (chalk)
SKIN     = "#D8B48C"
SHIRT    = "#6E8C9B"


# ----------------------------------------------------------------------
# Faris — a minimal figure (head + torso + simple limbs). Low detail on
# purpose: he is a presence in the story, not a character study.
# ----------------------------------------------------------------------
def make_faris(pos=ORIGIN, scale=1.0, facing=1):
    head = Circle(radius=0.16, fill_color=SKIN, fill_opacity=1,
                  stroke_width=0)
    head.move_to(UP * 0.62)
    torso = Line(UP * 0.46, DOWN * 0.10, color=SHIRT, stroke_width=8)
    arm = Line(UP * 0.34, RIGHT * facing * 0.26 + DOWN * 0.02,
               color=SHIRT, stroke_width=6)
    leg1 = Line(DOWN * 0.10, DOWN * 0.62 + LEFT * 0.12,
                color=PLY_DARK, stroke_width=6)
    leg2 = Line(DOWN * 0.10, DOWN * 0.62 + RIGHT * 0.12,
                color=PLY_DARK, stroke_width=6)
    g = VGroup(head, torso, arm, leg1, leg2)
    g.scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# The plywood ramp: a launch ramp (left), a gap, a lower landing ramp
# (right). `launch_h` controls the launch lip height (the trial knob).
# Returns a dict so beats can reach the launch lip / landing precisely.
# ----------------------------------------------------------------------
def make_ramp(launch_h=2.0, ground_y=-2.6, waxed=False):
    # launch ramp: a right triangle rising left->up to a lip
    lx0, lx1 = -5.4, -1.8           # base span of launch ramp
    lip = np.array([lx1, ground_y + launch_h, 0])
    base_l = np.array([lx0, ground_y, 0])
    foot_l = np.array([lx1, ground_y, 0])
    launch = Polygon(base_l, foot_l, lip,
                     fill_color=PLY, fill_opacity=1,
                     stroke_color=PLY_DARK, stroke_width=2)
    # waxed surface: a faint glint stripe along the ramp face
    face = Line(base_l, lip,
                color=(CHALK if waxed else PLY_DARK),
                stroke_width=(3 if waxed else 2))
    if waxed:
        face.set_opacity(0.85)

    # gap
    gap_x0, gap_x1 = lx1, 1.2
    gap_floor = Line([gap_x0, ground_y, 0], [gap_x1, ground_y, 0],
                     color=GAP_LINE, stroke_width=2).set_opacity(0.5)

    # landing ramp: a lower wedge on the right, sloping down to the right
    land_top = np.array([gap_x1, ground_y + launch_h * 0.42, 0])
    land_lo  = np.array([5.0, ground_y, 0])
    land_foot= np.array([gap_x1, ground_y, 0])
    landing = Polygon(land_foot, land_lo, land_top,
                      fill_color=PLY, fill_opacity=1,
                      stroke_color=PLY_DARK, stroke_width=2)

    grp = VGroup(launch, gap_floor, landing, face)
    info = {
        "group": grp, "lip": lip, "land_top": land_top,
        "land_lo": land_lo, "ground_y": ground_y,
        "gap_x0": gap_x0, "gap_x1": gap_x1, "launch_h": launch_h,
        "launch": launch, "landing": landing, "face": face,
    }
    return info


def board_dot(pos, color=CHALK, r=0.11):
    """The skateboard/rider as a single quiet dot."""
    return Dot(point=pos, radius=r, color=color)


# ----------------------------------------------------------------------
# A projectile / board arc between two points, with an apex offset.
# `peak` raises the arc; positive => higher. Returns a VMobject path.
# ----------------------------------------------------------------------
def arc_path(start, end, peak=1.4, dotted=False, color=FAIL_ARC,
             width=4, n=60):
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    pts = []
    for i in range(n + 1):
        t = i / n
        p = start + (end - start) * t
        p = p.copy()
        p[1] += peak * 4 * t * (1 - t)   # parabolic bump
        pts.append(p)
    path = VMobject()
    path.set_points_smoothly(pts)
    path.set_stroke(color, width=width)
    if dotted:
        return DashedVMobject(path, num_dashes=34, dashed_ratio=0.5
                              ).set_stroke(color, width=width)
    return path


def ideal_arc(start, end, peak=1.6):
    """The calm dotted ideal arc, launch lip -> landing."""
    return arc_path(start, end, peak=peak, dotted=True,
                    color=IDEAL, width=3)


# ----------------------------------------------------------------------
# Rough-vs-waxed surface texture swatch (close-up).
# ----------------------------------------------------------------------
def surface_swatch(pos=ORIGIN, waxed=False, w=3.6, h=0.7):
    base = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                            fill_color=PLY, fill_opacity=1,
                            stroke_color=PLY_DARK, stroke_width=2)
    base.move_to(pos)
    marks = VGroup()
    if not waxed:
        rng = np.random.default_rng(7)
        for k in range(26):
            x = -w / 2 + 0.12 + rng.random() * (w - 0.24)
            y0 = -h / 2 + 0.08 + rng.random() * (h - 0.16)
            ln = Line([x, y0, 0], [x + 0.05, y0 + 0.12, 0],
                      color=PLY_DARK, stroke_width=2).set_opacity(0.7)
            marks.add(ln)
    else:
        glint = Line([-w / 2 + 0.2, h * 0.18, 0],
                     [w / 2 - 0.2, h * 0.30, 0],
                     color=CHALK, stroke_width=4).set_opacity(0.8)
        glint2 = Line([-w / 2 + 0.5, -h * 0.05, 0],
                      [w / 2 - 0.5, h * 0.05, 0],
                      color=CHALK, stroke_width=2).set_opacity(0.45)
        marks.add(glint, glint2)
    marks.move_to(pos)
    return VGroup(base, marks)


# ----------------------------------------------------------------------
# A dwindling plywood stack (out of wood, out of patience).
# n = number of sheets remaining.
# ----------------------------------------------------------------------
def plywood_stack(pos=ORIGIN, n=6, w=1.7, sheet_h=0.16):
    g = VGroup()
    for k in range(n):
        r = Rectangle(width=w, height=sheet_h,
                       fill_color=PLY, fill_opacity=1,
                       stroke_color=PLY_DARK, stroke_width=1.5)
        r.move_to([0, k * (sheet_h + 0.04), 0])
        g.add(r)
    g.move_to(pos)
    return g


# ----------------------------------------------------------------------
# Energy bars — generic vertical bar with label. Used for stored / speed
# / heat in the story half, and for the PhET bar-chart panel.
# ----------------------------------------------------------------------
def energy_bar(label, frac, pos, color=STORED, max_h=2.6, w=0.62,
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


def bar_chart_panel(pos=ORIGIN, pe=0.85, ke=0.10, th=0.0, scale=1.0):
    """The PhET-style stacked energy bar chart: potential / kinetic /
    thermal / total. `total` = pe+ke+th (capped at 1)."""
    total = min(1.0, pe + ke + th)
    xs = [-1.05, -0.35, 0.35, 1.05]
    cols = [STORED, SPEED, HEAT, TOTAL]
    labs = ["PE", "KE", "th", "tot"]
    vals = [pe, ke, th, total]
    grp = VGroup()
    for x, c, lab, v in zip(xs, cols, labs, vals):
        b = energy_bar(lab, v, [x, 0, 0], color=c, max_h=2.4, w=0.5)
        grp.add(b)
    frame = Rectangle(width=3.2, height=3.3, stroke_color=DIM,
                      stroke_width=1.5, fill_opacity=0).set_opacity(0.4)
    frame.move_to(grp.get_center())
    panel = VGroup(frame, grp)
    panel.scale(scale).move_to(pos)
    panel.bars = grp
    return panel


def phet_track(pos=ORIGIN, launch_h=2.2, scale=1.0):
    """A smooth Energy-Skate-Park track shaped like Faris's ramp:
    a high left side, a dip, a lower right side."""
    g = -2.0
    pts = []
    xs = np.linspace(-3.0, 3.0, 60)
    for x in xs:
        # high-left, valley center, lower-right
        y = g + 0.55 * (x ** 2) * 0.20 + (launch_h * 0.0)
        y = g + launch_h * (0.5 * (np.cos((x + 3.0) / 6.0 * np.pi) + 1.0)) \
            * (1.0 if x < 0 else 0.62)
        pts.append([x, y, 0])
    track = VMobject().set_points_smoothly(pts)
    track.set_stroke(CHALK, width=4)
    out = VGroup(track)
    out.scale(scale).move_to(pos)
    out.track_pts = [out[0].point_from_proportion(t) for t in
                     np.linspace(0, 1, 40)]
    return out


def play_button(pos=ORIGIN, r=0.42, color=CHALK):
    circ = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    tri.scale(r * 0.55).rotate(-PI / 2)
    tri.move_to(circ.get_center() + RIGHT * r * 0.08)
    return VGroup(circ, tri).move_to(pos)


def friction_slider(pos=ORIGIN, frac=0.5, w=2.8, label="friction"):
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
    """Two short stacked bars: prediction vs the sim's result, with the
    difference marked."""
    base = Line(LEFT * 1.6, RIGHT * 1.6, color=DIM, stroke_width=2
                ).set_opacity(0.4)
    pbar = Rectangle(width=0.5, height=max(0.05, pred * 2.2),
                     fill_color=IDEAL, fill_opacity=1, stroke_width=0)
    rbar = Rectangle(width=0.5, height=max(0.05, res * 2.2),
                     fill_color=WAX_ARC, fill_opacity=1, stroke_width=0)
    pbar.move_to(base.get_left() + RIGHT * 0.9
                 + UP * pbar.height / 2)
    rbar.move_to(base.get_right() + LEFT * 0.9
                 + UP * rbar.height / 2)
    pl = Text("predicted", font="sans", font_size=18, color=DIM
              ).next_to(pbar, DOWN, buff=0.14)
    rl = Text("result", font="sans", font_size=18, color=DIM
              ).next_to(rbar, DOWN, buff=0.14)
    return VGroup(base, pbar, rbar, pl, rl).move_to(pos)


# ----------------------------------------------------------------------
# The three faint callback icons — must echo the concept-video imagery.
#   book : a book sitting on a shelf (gravitational PE)
#   cart : a small rolling cart (kinetic energy)
#   pend : a swinging pendulum (conservation of mechanical energy)
# Faint by default: they flicker in the void as memories.
# ----------------------------------------------------------------------
def callback_book(pos=ORIGIN, scale=1.0, opacity=0.85):
    shelf = Line(LEFT * 0.9, RIGHT * 0.9, color=PLY_DARK, stroke_width=4)
    book = VGroup()
    cover = Rectangle(width=0.34, height=0.62, fill_color=STORED,
                      fill_opacity=1, stroke_color=CHALK, stroke_width=1.5)
    spine = Line(cover.get_corner(UL), cover.get_corner(DL),
                 color=CHALK, stroke_width=2)
    book.add(cover, spine)
    book.next_to(shelf, UP, buff=0.0).shift(LEFT * 0.2)
    g = VGroup(shelf, book).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_cart(pos=ORIGIN, scale=1.0, opacity=0.85):
    body = RoundedRectangle(corner_radius=0.05, width=0.9, height=0.4,
                            fill_color=SPEED, fill_opacity=1,
                            stroke_color=CHALK, stroke_width=1.5)
    w1 = Circle(radius=0.13, fill_color=PLY_DARK, fill_opacity=1,
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
    bob = Circle(radius=0.15, fill_color=WAX_ARC, fill_opacity=1,
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
