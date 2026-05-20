"""Helpers for the Simple Machines & Mechanical Advantage (machines) scene.

Primitives the 12 beats need: a boulder, a lever bar over a triangular
fulcrum, a pushing hand, force arrows (small input / large output),
arc & rise traces, a force<->distance balance, a mechanical-advantage
ratio label, a ramp with a barrel, screw / wheel-axle / pulley icons,
a simple->compound bicycle, and ideal in==out work bars.

Pure #000000 void. font="sans" for every Text.
"""

from manim import *
import numpy as np

VOID = "#000000"

ROCK_BASE = "#6E6E6E"
ROCK_HI   = "#9A9A9A"
ROCK_DK   = "#4A4A4A"
BAR_COL   = "#C9A36B"          # wooden lever bar
FULCRUM   = "#8C98A6"
HAND_COL  = "#D9C2A3"
IN_COL    = "#7FB8E8"          # input / effort force (small, blue)
OUT_COL   = "#E8A86B"          # output / load force (large, amber)
DIST_COL  = "#A8C8A0"          # distance (green)
LABEL_COL = "#EAE4D5"
DIM_COL   = "#8C98A6"
METAL     = "#B8B8BE"
METAL_DK  = "#6E6E76"


# ---------------------------------------------------------------- boulder
def make_boulder(pos=ORIGIN, scale=1.0, seed=7):
    """A lumpy heavy rock. Deterministic per seed."""
    rng = np.random.default_rng(seed)
    n = 13
    base_r = 0.85 * scale
    pts = []
    for i in range(n):
        ang = TAU * i / n
        r = base_r * (1.0 + 0.22 * (rng.random() - 0.5) * 2)
        pts.append([r * np.cos(ang), r * np.sin(ang) * 0.78, 0])
    # smooth with rolling average (no np.convolve wrap — see CLAUDE.md)
    sm = []
    for i in range(n):
        a = np.array(pts[(i - 1) % n]); b = np.array(pts[i]); c = np.array(pts[(i + 1) % n])
        sm.append(((a + 2 * b + c) / 4.0).tolist())
    body = Polygon(*sm, color=ROCK_DK, stroke_width=2,
                   fill_color=ROCK_BASE, fill_opacity=1)
    body.set_sheen(0.25, UL)
    f1 = Polygon([-0.3 * scale, 0.15 * scale, 0], [0.1 * scale, 0.35 * scale, 0],
                 [0.25 * scale, 0.05 * scale, 0], color=ROCK_DK,
                 stroke_width=0, fill_color=ROCK_HI, fill_opacity=0.35)
    f2 = Line([-0.45 * scale, -0.2 * scale, 0], [0.2 * scale, -0.35 * scale, 0],
              color=ROCK_DK, stroke_width=1.5).set_opacity(0.5)
    return VGroup(body, f1, f2).move_to(pos)


# ---------------------------------------------------------------- fulcrum
def make_fulcrum(apex=ORIGIN, w=0.9, h=0.8, color=FULCRUM):
    """A triangular pivot. `apex` is the top point the bar balances on."""
    apex = np.array(apex, dtype=float)
    tri = Polygon(apex,
                  apex + np.array([-w / 2, -h, 0]),
                  apex + np.array([w / 2, -h, 0]),
                  color=color, stroke_width=2,
                  fill_color="#5A6470", fill_opacity=1)
    return tri


# ---------------------------------------------------------------- lever bar
def make_bar(pivot, angle=0.0, left_len=2.0, right_len=4.2,
             thickness=0.16, color=BAR_COL):
    """A straight lever bar pivoting on `pivot`, rotated by `angle` (rad).
    Returns the bar VGroup (already positioned). left_len = load arm,
    right_len = effort arm."""
    pivot = np.array(pivot, dtype=float)
    bar = RoundedRectangle(width=left_len + right_len, height=thickness,
                           corner_radius=thickness / 2,
                           color="#8A6F45", stroke_width=1.5,
                           fill_color=color, fill_opacity=1)
    # shift so the pivot sits at fraction left_len of the bar
    bar.move_to(pivot + np.array([(right_len - left_len) / 2, 0, 0]))
    bar.rotate(angle, about_point=pivot)
    return bar


def bar_end(pivot, angle, arm, side):
    """World point of a bar end. side=-1 left (load), +1 right (effort)."""
    pivot = np.array(pivot, dtype=float)
    d = np.array([np.cos(angle), np.sin(angle), 0]) * arm * side
    return pivot + d


# ---------------------------------------------------------------- hand
def make_hand(pos=ORIGIN, scale=1.0, color=HAND_COL):
    """A simple stylised pressing fist seen from the side."""
    palm = RoundedRectangle(width=0.62 * scale, height=0.5 * scale,
                            corner_radius=0.14 * scale, color="#B59A78",
                            stroke_width=1.5, fill_color=color, fill_opacity=1)
    wrist = RoundedRectangle(width=0.34 * scale, height=0.42 * scale,
                             corner_radius=0.1 * scale, color="#B59A78",
                             stroke_width=1.5, fill_color=color,
                             fill_opacity=1).next_to(palm, UR, buff=-0.12 * scale)
    knuck = VGroup(*[
        Circle(radius=0.075 * scale, color="#B59A78", stroke_width=1,
               fill_color=color, fill_opacity=1)
        .move_to(palm.get_bottom() + RIGHT * (i - 1.5) * 0.15 * scale + UP * 0.04)
        for i in range(4)])
    return VGroup(wrist, palm, knuck).move_to(pos)


# ---------------------------------------------------------------- arrows
def force_arrow(start, vec, color=IN_COL, width=6):
    s = np.array(start, dtype=float)
    e = s + np.array(vec, dtype=float)
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.32, tip_length=0.26)


# ---------------------------------------------------------------- traces
def arc_trace(center, radius, a0, a1, color=IN_COL, width=4, dashed=True):
    """A dashed arc showing the path swept by a bar end."""
    arc = Arc(radius=radius, start_angle=a0, angle=a1 - a0,
              arc_center=np.array(center, dtype=float),
              color=color, stroke_width=width)
    if dashed:
        return DashedVMobject(arc, num_dashes=22).set_color(color)
    return arc


def rise_trace(p_lo, p_hi, color=OUT_COL, width=4):
    """A short dashed vertical bracket showing the small rise."""
    p_lo = np.array(p_lo, dtype=float); p_hi = np.array(p_hi, dtype=float)
    seg = DashedLine(p_lo, p_hi, color=color, stroke_width=width,
                     dash_length=0.08)
    cap_lo = Line(p_lo + LEFT * 0.12, p_lo + RIGHT * 0.12,
                  color=color, stroke_width=width)
    cap_hi = Line(p_hi + LEFT * 0.12, p_hi + RIGHT * 0.12,
                  color=color, stroke_width=width)
    return VGroup(seg, cap_lo, cap_hi)


# ---------------------------------------------------------- balance scale
def make_balance(center=ORIGIN, scale=1.0, tilt=0.0):
    """A see-saw balance: force pan one side, distance pan the other.
    `tilt` rad rotates the beam (kept ~0 since the product is unchanged)."""
    center = np.array(center, dtype=float)
    post = Line(center + DOWN * 1.1 * scale, center + UP * 0.15 * scale,
                color=DIM_COL, stroke_width=5)
    base = Line(center + DOWN * 1.1 * scale + LEFT * 0.6 * scale,
                center + DOWN * 1.1 * scale + RIGHT * 0.6 * scale,
                color=DIM_COL, stroke_width=5)
    beam = Line(center + LEFT * 1.9 * scale, center + RIGHT * 1.9 * scale,
                color=METAL, stroke_width=6)
    beam.rotate(tilt, about_point=center)
    piv = Triangle(color=DIM_COL, fill_color="#5A6470", fill_opacity=1,
                   stroke_width=1).scale(0.18 * scale).move_to(center + UP * 0.02)
    g = VGroup(base, post, piv, beam)
    return g, beam


# ------------------------------------------------ mechanical advantage ratio
def ma_ratio(pos=ORIGIN, scale=1.0):
    """The ratio output-force / input-force as a labelled fraction."""
    fout = Text("output force", font="sans", font_size=26, color=OUT_COL)
    bar = Line(LEFT * 1.05, RIGHT * 1.05, color=LABEL_COL, stroke_width=3)
    fin = Text("input force", font="sans", font_size=26, color=IN_COL)
    frac = VGroup(fout, bar, fin).arrange(DOWN, buff=0.16)
    return frac.scale(scale).move_to(pos)


# ---------------------------------------------------------------- ramp
def make_ramp(base_left, base_len=5.0, height=2.2, color=DIM_COL):
    """A right-triangle incline. Returns (triangle, top_point, slope_unit)."""
    bl = np.array(base_left, dtype=float)
    br = bl + np.array([base_len, 0, 0])
    top = bl + np.array([0, height, 0])
    tri = Polygon(bl, br, top, color=color, stroke_width=2.5,
                  fill_color="#3A4048", fill_opacity=1)
    slope_vec = br - top
    slope_unit = slope_vec / np.linalg.norm(slope_vec)
    return tri, top, br, -slope_unit  # unit points up the slope (toward top)


def make_barrel(pos=ORIGIN, scale=1.0):
    body = RoundedRectangle(width=0.7 * scale, height=0.92 * scale,
                            corner_radius=0.1 * scale, color="#7A5A33",
                            stroke_width=2, fill_color="#A9762F",
                            fill_opacity=1)
    h1 = Line(body.get_left() + UP * 0.22 * scale,
              body.get_right() + UP * 0.22 * scale,
              color="#7A5A33", stroke_width=3)
    h2 = Line(body.get_left() + DOWN * 0.22 * scale,
              body.get_right() + DOWN * 0.22 * scale,
              color="#7A5A33", stroke_width=3)
    return VGroup(body, h1, h2).move_to(pos)


# ------------------------------------------------ simple-machine icons
def icon_screw(pos=ORIGIN, scale=1.0):
    shaft = Rectangle(width=0.34 * scale, height=1.1 * scale,
                      color=METAL_DK, stroke_width=1.5, fill_color=METAL,
                      fill_opacity=1)
    threads = VGroup(*[
        Line([-0.17 * scale, y, 0], [0.17 * scale, y - 0.12 * scale, 0],
             color=METAL_DK, stroke_width=2)
        for y in np.linspace(0.45 * scale, -0.45 * scale, 7)])
    head = Polygon([-0.28 * scale, 0.55 * scale, 0],
                   [0.28 * scale, 0.55 * scale, 0],
                   [0.16 * scale, 0.78 * scale, 0],
                   [-0.16 * scale, 0.78 * scale, 0],
                   color=METAL_DK, stroke_width=1.5, fill_color=METAL,
                   fill_opacity=1)
    return VGroup(shaft, threads, head).move_to(pos)


def icon_wheel_axle(pos=ORIGIN, scale=1.0):
    wheel = Circle(radius=0.55 * scale, color=METAL_DK, stroke_width=3,
                   fill_color="#4A4A52", fill_opacity=1)
    axle = Circle(radius=0.16 * scale, color=METAL_DK, stroke_width=2,
                  fill_color=METAL, fill_opacity=1)
    spokes = VGroup(*[
        Line(ORIGIN, 0.52 * scale * np.array([np.cos(a), np.sin(a), 0]),
             color=METAL_DK, stroke_width=2)
        for a in np.linspace(0, TAU, 6, endpoint=False)])
    return VGroup(wheel, spokes, axle).move_to(pos)


def icon_pulley(pos=ORIGIN, scale=1.0):
    wheel = Circle(radius=0.5 * scale, color=METAL_DK, stroke_width=3,
                   fill_color="#4A4A52", fill_opacity=1)
    hub = Circle(radius=0.1 * scale, color=METAL_DK, stroke_width=2,
                 fill_color=METAL, fill_opacity=1)
    left = Line([-0.5 * scale, 0.5 * scale, 0], [-0.5 * scale, -0.9 * scale, 0],
                color="#D9C2A3", stroke_width=3)
    right = Line([0.5 * scale, 0.5 * scale, 0], [0.5 * scale, -0.9 * scale, 0],
                 color="#D9C2A3", stroke_width=3)
    over = Arc(radius=0.5 * scale, start_angle=0, angle=PI,
               color="#D9C2A3", stroke_width=3)
    return VGroup(over, left, right, wheel, hub).move_to(pos)


# ------------------------------------------------ bicycle (compound)
def make_bicycle(pos=ORIGIN, scale=1.0, color=METAL):
    s = scale
    bw = Circle(radius=0.72 * s, color=METAL, stroke_width=4,
                fill_opacity=0)
    fw = bw.copy()
    bw.move_to(np.array([-1.35 * s, -0.55 * s, 0]))
    fw.move_to(np.array([1.55 * s, -0.55 * s, 0]))
    crank = Circle(radius=0.26 * s, color="#E8A86B", stroke_width=3,
                   fill_opacity=0).move_to([0.0, -0.55 * s, 0])
    cog = Circle(radius=0.16 * s, color="#E8A86B", stroke_width=3,
                 fill_opacity=0).move_to(bw.get_center())
    chain = VGroup(
        Line(crank.get_top(), cog.get_top(), color="#E8A86B", stroke_width=2),
        Line(crank.get_bottom(), cog.get_bottom(), color="#E8A86B",
             stroke_width=2))
    frame = VGroup(
        Line([-1.35 * s, -0.55 * s, 0], [0.0, 0.55 * s, 0]),
        Line([0.0, 0.55 * s, 0], [0.0, -0.55 * s, 0]),
        Line([0.0, -0.55 * s, 0], [-1.35 * s, -0.55 * s, 0]),
        Line([0.0, 0.55 * s, 0], [1.05 * s, 0.55 * s, 0]),
        Line([1.05 * s, 0.55 * s, 0], [1.55 * s, -0.55 * s, 0]),
        Line([0.0, -0.55 * s, 0], [1.55 * s, -0.55 * s, 0]),
    ).set_color(color).set_stroke(width=4)
    seat = Line([-0.2 * s, 0.6 * s, 0], [0.2 * s, 0.6 * s, 0],
                color=color, stroke_width=5)
    bars = Line([0.95 * s, 0.55 * s, 0], [1.25 * s, 0.75 * s, 0],
                color=color, stroke_width=5)
    return VGroup(bw, fw, frame, crank, cog, chain, seat, bars).move_to(pos)


# ------------------------------------------------ work bars (ideal in == out)
def work_bars(center=ORIGIN, scale=1.0, in_w=3.2, out_w=3.2, h=0.7):
    """Two horizontal bars: input work (blue) and output work (amber).
    Equal widths => ideal machine, work conserved."""
    center = np.array(center, dtype=float)
    in_bar = Rectangle(width=in_w * scale, height=h * scale, color=IN_COL,
                        fill_color=IN_COL, fill_opacity=0.85, stroke_width=2)
    out_bar = Rectangle(width=out_w * scale, height=h * scale, color=OUT_COL,
                        fill_color=OUT_COL, fill_opacity=0.85, stroke_width=2)
    in_bar.move_to(center + UP * 0.65 * scale).align_to(
        center + LEFT * 1.7 * scale + UP * 0.65 * scale, LEFT)
    out_bar.move_to(center + DOWN * 0.65 * scale).align_to(
        center + LEFT * 1.7 * scale + DOWN * 0.65 * scale, LEFT)
    in_lbl = Text("work in", font="sans", font_size=24, color=IN_COL
                  ).next_to(in_bar, LEFT, buff=0.3)
    out_lbl = Text("work out", font="sans", font_size=24, color=OUT_COL
                   ).next_to(out_bar, LEFT, buff=0.3)
    return VGroup(in_bar, out_bar, in_lbl, out_lbl)


# ---------------------------------------------------------------- labels
def small_label(text, pos, color=DIM_COL, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def title_label(text, pos, color=LABEL_COL, size=40):
    return Text(text, font="sans", font_size=size, color=color).move_to(pos)
