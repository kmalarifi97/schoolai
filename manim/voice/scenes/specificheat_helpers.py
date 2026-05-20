"""Helpers for the Specific Heat (specificheat) scene.

Pure #000000 void, font="sans". Primitives:
- pot on a flame (water / oil)
- thermometer with a settable level
- horizontal "energy in" bar and a labelled value bar
- a sponge-like absorbing block
- a small gram cube
- a simple bar chart
- a coastline (sea + sand) cell
- a small engine block / hot-water bottle / standing figure
- a labelled dial
- small text label
"""

from manim import *
import numpy as np

VOID = "#000000"

WATER_COL  = "#5BA3D9"
WATER_DARK = "#2E6E9E"
OIL_COL    = "#E0B23A"
OIL_DARK   = "#9C7A18"
METAL_COL  = "#B9BFC6"
METAL_DARK = "#71777E"
SAND_COL   = "#D9B26A"
FLAME_OUT  = "#F0902A"
FLAME_IN   = "#F6D341"
POT_COL    = "#8A8F96"
POT_DARK   = "#52565C"
ENERGY_COL = "#F0902A"
HOT_COL    = "#E2533B"
COOL_COL   = "#5BA3D9"
COLD_COL   = "#7C8AA0"  # sand-at-night: clearly distinct from the sea blue
INK        = "#EAE4D5"
DIM        = "#9AA0A6"


def label(text, pos, color=INK, size=28, opacity=1.0, slant=NORMAL):
    return Text(text, font="sans", font_size=size, color=color,
                slant=slant).move_to(pos).set_opacity(opacity)


def flame(pos, scale=1.0, color_out=FLAME_OUT, color_in=FLAME_IN):
    """A small stylised flame, centred at `pos`, tip pointing up."""
    outer = VMobject(stroke_width=0, fill_color=color_out, fill_opacity=0.95)
    outer.set_points_as_corners([
        [-0.34, -0.30, 0], [-0.20, 0.05, 0], [-0.07, -0.10, 0],
        [0.0, 0.55, 0], [0.10, -0.08, 0], [0.22, 0.08, 0],
        [0.34, -0.30, 0], [-0.34, -0.30, 0],
    ])
    inner = VMobject(stroke_width=0, fill_color=color_in, fill_opacity=0.95)
    inner.set_points_as_corners([
        [-0.15, -0.25, 0], [-0.06, 0.02, 0], [0.0, 0.28, 0],
        [0.07, 0.0, 0], [0.15, -0.25, 0], [-0.15, -0.25, 0],
    ])
    g = VGroup(outer, inner).scale(scale).move_to(pos)
    return g


def burner(pos, width=2.0, n_flames=3, scale=1.0):
    """A horizontal burner line with several flames on it."""
    base = Line([-width / 2, 0, 0], [width / 2, 0, 0],
                color=POT_DARK, stroke_width=5)
    fl = VGroup()
    xs = np.linspace(-width / 2 + 0.3, width / 2 - 0.3, n_flames)
    for x in xs:
        fl.add(flame([x, 0.30 * scale, 0], scale=0.7 * scale))
    return VGroup(base, fl).move_to(pos)


def pot(pos, liquid="water", width=2.0, height=1.3, fill_frac=0.62):
    """A pot with a handle and a coloured liquid inside."""
    if liquid == "water":
        lc, ld = WATER_COL, WATER_DARK
    elif liquid == "oil":
        lc, ld = OIL_COL, OIL_DARK
    else:
        lc, ld = METAL_COL, METAL_DARK
    body = RoundedCornerRectangle if False else Rectangle
    shell = Rectangle(width=width, height=height, color=POT_COL,
                      stroke_width=5, fill_color="#3A3D42", fill_opacity=1.0)
    inner_h = height * fill_frac
    liquid_rect = Rectangle(width=width - 0.16, height=inner_h,
                            stroke_width=0, fill_color=lc, fill_opacity=1.0)
    liquid_rect.move_to(shell.get_bottom() + UP * (inner_h / 2 + 0.07))
    surf = Line(liquid_rect.get_corner(UL), liquid_rect.get_corner(UR),
                color=ld, stroke_width=4)
    handle = Arc(radius=0.26, start_angle=-PI / 2, angle=PI,
                 color=POT_COL, stroke_width=5)
    handle.move_to(shell.get_right() + RIGHT * 0.22)
    g = VGroup(shell, liquid_rect, surf, handle).move_to(pos)
    g.shell, g.liquid = shell, liquid_rect
    return g


def clock(pos, scale=1.0, hand_angle=-PI / 3):
    """A simple round clock."""
    face = Circle(radius=0.5 * scale, color=INK, stroke_width=3,
                  fill_color="#1A1C1F", fill_opacity=1.0)
    ticks = VGroup()
    for k in range(12):
        a = TAU * k / 12 + PI / 2
        p1 = np.array([np.cos(a), np.sin(a), 0]) * 0.42 * scale
        p2 = np.array([np.cos(a), np.sin(a), 0]) * 0.5 * scale
        ticks.add(Line(p1, p2, color=DIM, stroke_width=2))
    hand = Line([0, 0, 0],
                np.array([np.cos(hand_angle), np.sin(hand_angle), 0]) * 0.36 * scale,
                color=HOT_COL, stroke_width=4)
    hand2 = Line([0, 0, 0],
                 np.array([np.cos(hand_angle + 1.7),
                           np.sin(hand_angle + 1.7), 0]) * 0.26 * scale,
                 color=INK, stroke_width=3)
    g = VGroup(face, ticks, hand, hand2).move_to(pos)
    return g


class Thermometer(VGroup):
    """A vertical thermometer. set_level(frac 0..1) updates the fill."""

    def __init__(self, pos, height=2.6, color=HOT_COL, level=0.15, **kw):
        super().__init__(**kw)
        self.h = height
        self.col = color
        bulb = Circle(radius=0.22, color=INK, stroke_width=3,
                      fill_color=color, fill_opacity=1.0)
        tube_out = RoundedRectangle(width=0.26, height=height,
                                    corner_radius=0.12, color=INK,
                                    stroke_width=3, fill_color="#16181B",
                                    fill_opacity=1.0)
        tube_out.next_to(bulb, UP, buff=-0.10)
        self.bulb, self.tube = bulb, tube_out
        self._base_y = tube_out.get_bottom()[1] + 0.06
        self._top_y = tube_out.get_top()[1] - 0.10
        self.fill = Rectangle(width=0.14, height=0.01, stroke_width=0,
                              fill_color=color, fill_opacity=1.0)
        self.add(tube_out, bulb, self.fill)
        self.move_to(pos)
        self._anchor = self.fill.get_center()  # placeholder
        self.set_level(level)

    def set_level(self, frac):
        frac = float(np.clip(frac, 0.02, 1.0))
        b = self.tube.get_bottom()[1] + 0.07
        t = self.tube.get_top()[1] - 0.12
        h = (t - b) * frac
        x = self.tube.get_center()[0]
        self.fill.become(Rectangle(width=0.14, height=max(h, 0.02),
                                   stroke_width=0, fill_color=self.col,
                                   fill_opacity=1.0))
        self.fill.move_to([x, b + h / 2, 0])
        return self


def energy_bar(pos, length=3.0, frac=1.0, color=ENERGY_COL, height=0.34,
               outline=True):
    """A horizontal bar representing 'energy in'. Returns VGroup with .fill."""
    frame = Rectangle(width=length, height=height, color=DIM,
                      stroke_width=2 if outline else 0, fill_opacity=0)
    fill = Rectangle(width=max(length * frac, 0.02), height=height - 0.06,
                     stroke_width=0, fill_color=color, fill_opacity=1.0)
    fill.move_to(frame.get_left() + RIGHT * (length * frac / 2))
    g = VGroup(frame, fill).move_to(pos)
    # re-anchor fill to left after move
    fill.move_to(frame.get_left() + RIGHT * (length * frac / 2))
    g.fill, g.frame = fill, frame
    g.length = length
    return g


def sponge(pos, w=1.9, h=1.5, color=WATER_COL):
    """A rounded block riddled with holes — the 'soaks it up' metaphor."""
    body = RoundedRectangle(width=w, height=h, corner_radius=0.18,
                            color=WATER_DARK, stroke_width=3,
                            fill_color=color, fill_opacity=1.0)
    holes = VGroup()
    rng = np.random.RandomState(7)
    for _ in range(11):
        hx = rng.uniform(-w / 2 + 0.28, w / 2 - 0.28)
        hy = rng.uniform(-h / 2 + 0.28, h / 2 - 0.28)
        r = rng.uniform(0.07, 0.15)
        holes.add(Circle(radius=r, stroke_width=0,
                         fill_color=WATER_DARK, fill_opacity=0.65)
                  .move_to([hx, hy, 0]))
    return VGroup(body, holes).move_to(pos)


def gram_cube(pos, side=0.7, color=WATER_COL, glow=0.0):
    """A tiny cube with a faint isometric top/side — '1 g'."""
    front = Square(side, color=WATER_DARK, stroke_width=3,
                   fill_color=color, fill_opacity=1.0)
    o = side * 0.34
    top = Polygon(front.get_corner(UL), front.get_corner(UL) + [o, o, 0],
                  front.get_corner(UR) + [o, o, 0], front.get_corner(UR),
                  stroke_width=2, color=WATER_DARK,
                  fill_color=color, fill_opacity=0.8)
    side_f = Polygon(front.get_corner(UR), front.get_corner(UR) + [o, o, 0],
                     front.get_corner(DR) + [o, o, 0], front.get_corner(DR),
                     stroke_width=2, color=WATER_DARK,
                     fill_color=color, fill_opacity=0.6)
    g = VGroup(side_f, top, front).move_to(pos)
    if glow > 0:
        halo = Square(side * 1.5, stroke_width=0,
                      fill_color=HOT_COL, fill_opacity=glow * 0.4)
        halo.move_to(g.get_center())
        g.add_to_back(halo)
    return g


def bar_chart(pos, items, max_h=3.2, bar_w=0.7, gap=0.55):
    """items: list of (name, value, color). Returns VGroup with .bars."""
    vmax = max(v for _, v, _ in items)
    n = len(items)
    total_w = n * bar_w + (n - 1) * gap
    g = VGroup()
    bars = []
    for k, (name, val, col) in enumerate(items):
        bh = max_h * (val / vmax)
        x = -total_w / 2 + bar_w / 2 + k * (bar_w + gap)
        bar = Rectangle(width=bar_w, height=max(bh, 0.04), stroke_width=0,
                        fill_color=col, fill_opacity=1.0)
        bar.move_to([x, bh / 2, 0])
        nm = label(name, [x, -0.30, 0], size=20, color=DIM)
        g.add(bar, nm)
        bars.append(bar)
    baseline = Line([-total_w / 2 - 0.3, 0, 0], [total_w / 2 + 0.3, 0, 0],
                    color=DIM, stroke_width=2)
    g.add(baseline)
    g.move_to(pos)
    g.bars = bars
    return g


def coast_cell(pos, w=5.4, h=3.0):
    """Left half = sea (steady), right half = sand (swinging). Returns
    VGroup with .sea, .sand, .sun for animating a day cycle."""
    frame = Rectangle(width=w, height=h, color=DIM, stroke_width=2,
                      fill_opacity=0)
    sea = Rectangle(width=w / 2, height=h, stroke_width=0,
                    fill_color=WATER_COL, fill_opacity=1.0)
    sea.move_to(frame.get_left() + RIGHT * w / 4)
    sand = Rectangle(width=w / 2, height=h, stroke_width=0,
                     fill_color=SAND_COL, fill_opacity=1.0)
    sand.move_to(frame.get_right() + LEFT * w / 4)
    waves = VGroup()
    for k in range(3):
        y = h / 2 - 0.5 - k * 0.45
        waves.add(FunctionGraph(lambda x: 0.06 * np.sin(6 * x),
                                x_range=[-w / 2 + 0.2, 0 - 0.2],
                                color=WATER_DARK, stroke_width=2)
                  .shift(UP * y))
    sun = Circle(radius=0.26, stroke_width=0, fill_color=FLAME_IN,
                 fill_opacity=1.0)
    sun.move_to(frame.get_top() + DOWN * 0.5 + LEFT * 0.2)
    divider = Line(frame.get_top(), frame.get_bottom(),
                   color="#1A1C1F", stroke_width=5)
    g = VGroup(frame, sea, sand, waves, divider, sun).move_to(pos)
    g.sea, g.sand, g.sun, g.frame = sea, sand, sun, frame
    return g


def engine_block(pos, scale=1.0):
    """A blocky engine with two channels for coolant."""
    block = RoundedRectangle(width=2.0, height=1.6, corner_radius=0.12,
                             color=METAL_DARK, stroke_width=4,
                             fill_color="#3A3D42", fill_opacity=1.0)
    fins = VGroup(*[Line([-0.8, y, 0], [0.8, y, 0], color=METAL_COL,
                         stroke_width=3)
                    for y in np.linspace(-0.5, 0.5, 4)])
    g = VGroup(block, fins).scale(scale).move_to(pos)
    g.block = block
    return g


def water_bottle(pos, scale=1.0):
    """A hot-water bottle shape."""
    body = RoundedRectangle(width=1.4, height=2.0, corner_radius=0.45,
                            color=WATER_DARK, stroke_width=4,
                            fill_color=WATER_COL, fill_opacity=1.0)
    neck = Rectangle(width=0.42, height=0.4, color=WATER_DARK,
                     stroke_width=4, fill_color=WATER_COL, fill_opacity=1.0)
    neck.next_to(body, UP, buff=-0.06)
    cap = Rectangle(width=0.5, height=0.22, color=METAL_DARK,
                    stroke_width=3, fill_color=METAL_COL, fill_opacity=1.0)
    cap.next_to(neck, UP, buff=-0.02)
    ribs = VGroup(*[Line([-0.5, y, 0], [0.5, y, 0], color=WATER_DARK,
                        stroke_width=2)
                    for y in np.linspace(-0.6, 0.6, 4)])
    g = VGroup(body, neck, cap, ribs).scale(scale).move_to(pos)
    return g


def standing_figure(pos, scale=1.0, color=INK):
    """A simple human silhouette."""
    head = Circle(radius=0.22, color=color, stroke_width=0,
                  fill_color=color, fill_opacity=1.0)
    body = RoundedRectangle(width=0.5, height=0.9, corner_radius=0.18,
                            color=color, stroke_width=0,
                            fill_color=color, fill_opacity=1.0)
    body.next_to(head, DOWN, buff=0.04)
    legL = Line([-0.10, 0, 0], [-0.13, -0.7, 0], color=color, stroke_width=7)
    legR = Line([0.10, 0, 0], [0.13, -0.7, 0], color=color, stroke_width=7)
    legs = VGroup(legL, legR).next_to(body, DOWN, buff=0.0)
    g = VGroup(head, body, legs).scale(scale).move_to(pos)
    return g


def dial(pos, label_text, frac=0.55, scale=1.0, color=ENERGY_COL):
    """A semicircular gauge dial with a needle and a caption."""
    r = 0.7 * scale
    arc = Arc(radius=r, start_angle=PI, angle=-PI, color=DIM,
              stroke_width=4)
    ticks = VGroup()
    for k in range(6):
        a = PI - PI * k / 5
        p1 = np.array([np.cos(a), np.sin(a), 0]) * r
        p2 = np.array([np.cos(a), np.sin(a), 0]) * (r - 0.12)
        ticks.add(Line(p1, p2, color=DIM, stroke_width=2))
    na = PI - PI * float(np.clip(frac, 0, 1))
    needle = Line([0, 0, 0],
                  np.array([np.cos(na), np.sin(na), 0]) * (r - 0.10),
                  color=color, stroke_width=5)
    hub = Dot([0, 0, 0], radius=0.05, color=color)
    cap = label(label_text, [0, -0.42, 0], size=22, color=INK)
    g = VGroup(arc, ticks, needle, hub, cap).move_to(pos)
    g.needle, g.r = needle, r
    return g
