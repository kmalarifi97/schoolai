"""Helpers for the Latent Heat (latentheat) scene.

Primitives the 12 beats need:
  - glass of ice water sitting on a flame, with a thermometer
  - steady energy arrows pouring in
  - a flat / rising temperature line and a full heating curve
  - a rigid ice lattice with bonds that snap into liquid disorder
  - steam vs. boiling water energy-bar comparison
  - sweat droplets evaporating off skin

Pure #000000 void. font="sans" for all text.
"""

from manim import *
import numpy as np

VOID        = "#000000"
GLASS_COL   = "#9FC6E0"
WATER_COL   = "#5E86A8"
ICE_COL     = "#CFE6F2"
ICE_EDGE    = "#8FB9D2"
FLAME_OUT   = "#E08A3C"
FLAME_IN    = "#F2C14E"
ENERGY_COL  = "#F2A24E"
TEMP_COL    = "#E8615A"
CURVE_COL   = "#E8C15A"
BOND_COL    = "#8FB9D2"
PART_COL    = "#CFE6F2"
STEAM_COL   = "#C8D6E0"
SKIN_COL    = "#D9A57A"
LABEL_COL   = "#EAE4D5"
FAINT_LBL   = "#8C98A6"


def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


# ---------------------------------------------------------------------------
# Glass of ice water
# ---------------------------------------------------------------------------
def make_glass(pos=(0, 0, 0), scale=1.0, ice_frac=1.0):
    """A tumbler glass with water and `ice_frac` worth of ice cubes (0..1).

    Returns VGroup(glass_outline, water, *ice_cubes). Empty-friendly when
    ice_frac == 0 (no cubes added).
    """
    pos = np.array(pos, dtype=float)
    w, h = 1.7 * scale, 2.3 * scale
    # slightly tapered tumbler
    tl = [-w / 2, h / 2, 0]
    tr = [w / 2, h / 2, 0]
    br = [w * 0.40, -h / 2, 0]
    bl = [-w * 0.40, -h / 2, 0]
    glass = VMobject(stroke_color=GLASS_COL, stroke_width=4)
    glass.set_points_as_corners([tl, bl, br, tr])
    glass.set_fill(opacity=0)

    water_top = h / 2 - 0.30 * scale
    wtl = [-w / 2 * 0.97, water_top, 0]
    wtr = [w / 2 * 0.97, water_top, 0]
    wbr = [w * 0.40 * 0.97, -h / 2 * 0.97, 0]
    wbl = [-w * 0.40 * 0.97, -h / 2 * 0.97, 0]
    water = Polygon(wtl, wbl, wbr, wtr, color=WATER_COL,
                    fill_color=WATER_COL, fill_opacity=0.55,
                    stroke_width=0)

    grp = VGroup(glass, water)

    if ice_frac > 0:
        n = max(1, int(round(4 * ice_frac)))
        spots = [(-0.32, 0.55), (0.34, 0.62), (0.02, 0.18),
                 (-0.20, -0.05)]
        for k in range(min(n, len(spots))):
            cx, cy = spots[k]
            cube = RoundedCorners_square(0.42 * scale)
            cube.move_to([cx * w, cy * h * 0.5, 0])
            cube.rotate(0.18 * (k - 1))
            grp.add(cube)

    return grp.move_to(pos)


def RoundedCorners_square(side):
    sq = RoundedRectangle(width=side, height=side, corner_radius=0.06,
                          fill_color=ICE_COL, fill_opacity=0.85,
                          stroke_color=ICE_EDGE, stroke_width=2)
    return sq


def make_flame(pos=(0, 0, 0), scale=1.0):
    """A small two-tone flame, base at `pos` pointing up."""
    pos = np.array(pos, dtype=float)
    outer = VMobject(stroke_width=0, fill_color=FLAME_OUT, fill_opacity=0.9)
    outer.set_points_as_corners([
        [-0.45 * scale, 0, 0], [-0.20 * scale, 0.55 * scale, 0],
        [0.0, 0.30 * scale, 0], [0.20 * scale, 0.80 * scale, 0],
        [0.10 * scale, 1.20 * scale, 0], [0.0, 1.45 * scale, 0],
        [-0.12 * scale, 1.10 * scale, 0], [-0.22 * scale, 0.70 * scale, 0],
        [-0.45 * scale, 0, 0],
    ])
    inner = VMobject(stroke_width=0, fill_color=FLAME_IN, fill_opacity=0.95)
    inner.set_points_as_corners([
        [-0.22 * scale, 0.05 * scale, 0], [-0.05 * scale, 0.45 * scale, 0],
        [0.10 * scale, 0.70 * scale, 0], [0.02 * scale, 0.95 * scale, 0],
        [-0.04 * scale, 0.55 * scale, 0], [-0.22 * scale, 0.05 * scale, 0],
    ])
    return VGroup(outer, inner).move_to(pos + np.array([0, 0.7 * scale, 0]))


def make_thermometer(pos=(0, 0, 0), scale=1.0, level=0.0):
    """Vertical thermometer. `level` 0..1 maps bulb-empty to full column.

    Returns VGroup(tube, bulb, mercury, *ticks). Bulb at the bottom.
    """
    pos = np.array(pos, dtype=float)
    tube_h = 3.0 * scale
    tube_w = 0.30 * scale
    tube = RoundedRectangle(width=tube_w, height=tube_h,
                            corner_radius=tube_w / 2,
                            stroke_color=LABEL_COL, stroke_width=2.5,
                            fill_opacity=0)
    bulb = Circle(radius=0.30 * scale, stroke_color=LABEL_COL,
                  stroke_width=2.5, fill_color=TEMP_COL, fill_opacity=1)
    bulb.next_to(tube, DOWN, buff=-0.12 * scale)

    col_bottom = bulb.get_center()[1] + 0.10 * scale
    col_top_max = tube.get_top()[1] - 0.12 * scale
    col_h = (col_top_max - col_bottom) * float(np.clip(level, 0, 1))
    col_h = max(col_h, 0.02 * scale)
    mercury = Rectangle(width=tube_w * 0.45, height=col_h,
                        fill_color=TEMP_COL, fill_opacity=1,
                        stroke_width=0)
    mercury.move_to([tube.get_center()[0],
                     col_bottom + col_h / 2, 0])

    grp = VGroup(tube, bulb, mercury)
    for f in (0.0, 0.5, 1.0):
        ty = col_bottom + (col_top_max - col_bottom) * f
        tk = Line([tube.get_center()[0] + tube_w / 2, ty, 0],
                  [tube.get_center()[0] + tube_w / 2 + 0.14 * scale, ty, 0],
                  color=FAINT_LBL, stroke_width=2)
        grp.add(tk)
    return grp.move_to(pos)


def energy_arrows(center, n=5, length=0.9, color=ENERGY_COL,
                  spread=1.8, y=-1.6, up=True):
    """A row of `n` short arrows pointing UP (energy pouring into the
    base of the glass). Centered horizontally on `center`."""
    center = np.array(center, dtype=float)
    g = VGroup()
    xs = np.linspace(-spread, spread, n)
    for x in xs:
        base = center + np.array([x, y, 0])
        tip = base + np.array([0, length if up else -length, 0])
        a = Arrow(base, tip, color=color, stroke_width=5, buff=0,
                  max_tip_length_to_length_ratio=0.32, tip_length=0.18)
        g.add(a)
    return g


# ---------------------------------------------------------------------------
# Heating curve (temperature vs energy)
# ---------------------------------------------------------------------------
def heating_curve(origin=(-5.2, -2.4, 0), w=10.4, h=4.4,
                  show_plateaus=True, color=CURVE_COL):
    """Temperature-vs-energy curve: rise, flat (melt), rise, flat (boil),
    rise. Returns VGroup(axes_v, axes_h, curve, melt_seg, boil_seg).

    melt_seg / boil_seg are the two flat plateau sub-paths, returned
    separately so a beat can highlight them.
    """
    o = np.array(origin, dtype=float)
    ax_v = Arrow(o, o + np.array([0, h, 0]), color=FAINT_LBL,
                 stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.05)
    ax_h = Arrow(o, o + np.array([w, 0, 0]), color=FAINT_LBL,
                 stroke_width=3, buff=0, max_tip_length_to_length_ratio=0.05)

    # x fractions for the 5 segments
    p = [0.0, 0.16, 0.40, 0.58, 0.82, 1.0]
    # y levels (temperature)
    y0, y_melt, y_boil, y_top = 0.10, 0.34, 0.74, 0.96

    def P(fx, fy):
        return o + np.array([fx * w, fy * h, 0])

    pts = [
        P(p[0], y0),
        P(p[1], y_melt),   # rise to melting
        P(p[2], y_melt),   # FLAT: melting plateau
        P(p[3], y_boil),   # rise to boiling
        P(p[4], y_boil),   # FLAT: boiling plateau
        P(p[5], y_top),    # rise as steam
    ]
    curve = VMobject(stroke_color=color, stroke_width=6)
    curve.set_points_as_corners(pts)

    melt_seg = Line(pts[1], pts[2], color=color, stroke_width=8)
    boil_seg = Line(pts[3], pts[4], color=color, stroke_width=8)

    return VGroup(ax_v, ax_h, curve, melt_seg, boil_seg)


def make_lattice(center=(0, 0, 0), rows=4, cols=4, gap=0.62,
                  part_r=0.16):
    """An ordered crystal: grid of particles + bonds between neighbours.

    Returns VGroup(bonds_group, parts_group) so a beat can snap bonds
    and scatter particles independently.
    """
    center = np.array(center, dtype=float)
    parts = VGroup()
    coords = {}
    x0 = -(cols - 1) * gap / 2
    y0 = -(rows - 1) * gap / 2
    for r in range(rows):
        for c in range(cols):
            p = center + np.array([x0 + c * gap, y0 + r * gap, 0])
            dot = Dot(p, radius=part_r, color=PART_COL)
            dot.set_fill(PART_COL, opacity=1)
            parts.add(dot)
            coords[(r, c)] = p

    bonds = VGroup()
    for r in range(rows):
        for c in range(cols):
            if c + 1 < cols:
                bonds.add(Line(coords[(r, c)], coords[(r, c + 1)],
                               color=BOND_COL, stroke_width=3))
            if r + 1 < rows:
                bonds.add(Line(coords[(r, c)], coords[(r + 1, c)],
                               color=BOND_COL, stroke_width=3))
    return VGroup(bonds, parts)


def energy_bar(pos, frac, label, max_h=2.6, w=0.8, color=ENERGY_COL,
               lbl_color=LABEL_COL):
    """A vertical filled bar of height frac*max_h with a caption below."""
    pos = np.array(pos, dtype=float)
    frame = Rectangle(width=w, height=max_h, stroke_color=FAINT_LBL,
                      stroke_width=2, fill_opacity=0).move_to(pos)
    fh = max(0.04, frac * max_h)
    fill = Rectangle(width=w * 0.86, height=fh, stroke_width=0,
                     fill_color=color, fill_opacity=0.9)
    fill.move_to([pos[0], frame.get_bottom()[1] + fh / 2, 0])
    cap = Text(label, font="sans", font_size=20, color=lbl_color
               ).next_to(frame, DOWN, buff=0.22)
    return VGroup(frame, fill, cap)


def make_skin(pos=(0, 0, 0), w=5.0, h=1.0):
    """A horizontal skin surface (gentle arc) for the sweat/steam beats."""
    pos = np.array(pos, dtype=float)
    arc = ArcBetweenPoints(pos + np.array([-w / 2, 0, 0]),
                           pos + np.array([w / 2, 0, 0]),
                           angle=-0.28)
    arc.set_stroke(SKIN_COL, width=5)
    band = Polygon(
        pos + np.array([-w / 2, 0, 0]),
        pos + np.array([-w / 2, -h, 0]),
        pos + np.array([w / 2, -h, 0]),
        pos + np.array([w / 2, 0, 0]),
        fill_color=SKIN_COL, fill_opacity=0.30, stroke_width=0)
    return VGroup(band, arc)


def droplet(pos, r=0.16, color=WATER_COL):
    """A small teardrop-ish water droplet."""
    pos = np.array(pos, dtype=float)
    d = Circle(radius=r, color=color, fill_color=color, fill_opacity=0.75,
               stroke_color=GLASS_COL, stroke_width=1.5)
    tip = Triangle(color=color, fill_color=color, fill_opacity=0.75,
                   stroke_width=0).scale(r * 0.9)
    tip.next_to(d, UP, buff=-r * 0.6)
    return VGroup(d, tip).move_to(pos)


def steam_curl(pos, scale=1.0, color=STEAM_COL):
    """A wispy rising steam curl."""
    pos = np.array(pos, dtype=float)
    pts = []
    for t in np.linspace(0, 1, 28):
        x = 0.32 * scale * np.sin(t * 3.4 * PI)
        y = t * 1.6 * scale
        pts.append([x, y, 0])
    c = VMobject(stroke_color=color, stroke_width=4)
    c.set_points_as_corners(pts)
    c.set_opacity(0.7)
    return c.move_to(pos + np.array([0, 0.8 * scale, 0]))
