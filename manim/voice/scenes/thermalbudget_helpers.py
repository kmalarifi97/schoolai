"""Helpers for the Thermal Budget (thermalbudget) project-story.

A narrative: Maha must melt a block of ice to water exactly when a timer
ends. The thermometer stalls at 0deg, then overshoots. She rebuilds it in
PhET Energy Forms and Changes, predicts-then-runs, then the ending calls
back to four earlier concept videos:
  - temperature-vs-thermal (match vs steaming tub)
  - specific heat (water vs oil, diverging thermometers)
  - heat transfer (conduction/convection/radiation triptych)
  - latent heat (the thermometer stuck at 0deg while ice drinks energy)

Pure #000000 void. font="sans" for any Text. Calm, kitchen-table palette.
"""

from manim import *
import numpy as np

VOID = "#000000"

# Warm, low-key palette — ice, water, heat glow, chalk. No hype colors.
ICE      = "#BFE3F2"   # ice block (pale cyan)
ICE_EDGE = "#8FC4DC"   # ice outline
WATER    = "#5A9BD4"   # liquid water (cool blue)
METAL    = "#B9BFC6"   # metal cup / good conductor
METAL_DK = "#7C828A"
HEAT     = "#D98C5F"   # thermal / heat glow
HEAT_BR  = "#E8A06B"   # brighter heat
CHALK    = "#EAE4D5"   # chalk-white lines / labels
DIM      = "#8C8576"   # dim secondary
LEDGER   = "#5A5446"   # faint ledger rules
OIL      = "#C7A24B"   # oil (warm yellow)
SUN_C    = "#E8C46B"   # the Sun (radiation callback)
SKIN     = "#D8B48C"
SHIRT    = "#6E8C9B"
PLATEAU  = "#9BD6B0"   # the flat melting plateau highlight


# ----------------------------------------------------------------------
# Maha — a minimal figure (head + torso + simple limbs). A presence in
# the story, not a character study.
# ----------------------------------------------------------------------
def make_maha(pos=ORIGIN, scale=1.0, facing=1):
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
# The heater: a small slab with coil arcs on top and an optional glow.
# `heat` 0..1 controls coil brightness / glow opacity.
# ----------------------------------------------------------------------
def make_heater(pos=ORIGIN, scale=1.0, heat=0.4):
    heat = float(np.clip(heat, 0.0, 1.0))
    body = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.5,
                            fill_color=METAL_DK, fill_opacity=1,
                            stroke_color=DIM, stroke_width=2)
    coils = VGroup()
    coil_col = interpolate_color(
        ManimColor(DIM), ManimColor(HEAT_BR), heat)
    for k in range(4):
        cx = -0.75 + k * 0.5
        arc = Arc(radius=0.16, start_angle=PI, angle=-PI,
                  arc_center=[cx, 0.30, 0])
        arc.set_stroke(coil_col, width=4)
        coils.add(arc)
    grp = VGroup(body, coils)
    glow = None
    if heat > 0.02:
        glow = Ellipse(width=2.4, height=0.9, stroke_width=0,
                       fill_color=HEAT, fill_opacity=0.0)
        glow.set_fill(HEAT, opacity=0.10 + 0.35 * heat)
        glow.move_to(body.get_top() + UP * 0.22)
        grp = VGroup(glow, body, coils)
    out = grp
    out.scale(scale).move_to(pos)
    out.coils = coils
    out.body = body
    out.glow = glow
    return out


# ----------------------------------------------------------------------
# Ice block sitting on a heater. `melt` 0..1 shrinks the ice and reveals
# a growing pool of water beneath it. Returns a group with handles.
# ----------------------------------------------------------------------
def ice_on_heater(pos=ORIGIN, scale=1.0, heat=0.6, melt=0.0):
    melt = float(np.clip(melt, 0.0, 1.0))
    heater = make_heater([0, -0.55, 0], scale=1.0, heat=heat)

    # water pool grows on the heater top as ice melts
    pool_w = 1.7
    pool_h = max(0.001, 0.06 + 0.34 * melt)
    pool = RoundedRectangle(corner_radius=0.05, width=pool_w,
                            height=pool_h, stroke_width=0,
                            fill_color=WATER, fill_opacity=0.9)
    pool.move_to([0, -0.30 + pool_h / 2 - 0.0, 0])

    # ice cube shrinks with melt
    side = 1.25 * (1.0 - 0.92 * melt)
    side = max(0.06, side)
    ice = RoundedRectangle(corner_radius=0.06, width=side, height=side,
                           fill_color=ICE, fill_opacity=0.92,
                           stroke_color=ICE_EDGE, stroke_width=2)
    ice.move_to([0, -0.30 + pool_h + side / 2 + 0.02, 0])
    # a couple of inner facets so it reads as a solid block
    facet = Line(ice.get_corner(UL) + [side * 0.18, -side * 0.12, 0],
                 ice.get_corner(UL) + [side * 0.42, -side * 0.42, 0],
                 color="#FFFFFF", stroke_width=2).set_opacity(0.5)

    grp = VGroup(heater, pool, ice, facet)
    grp.scale(scale).move_to(pos)
    grp.heater = heater
    grp.pool = pool
    grp.ice = ice
    return grp


# ----------------------------------------------------------------------
# Metal-cup variant: the ice sits in a metal cup on the heater (fast
# conduction). Same melt semantics.
# ----------------------------------------------------------------------
def metal_cup(pos=ORIGIN, scale=1.0, heat=0.6, fill=0.4):
    fill = float(np.clip(fill, 0.0, 1.0))
    heater = make_heater([0, -0.65, 0], scale=1.0, heat=heat)
    cup = VGroup(
        Line([-0.7, 0.55, 0], [-0.55, -0.35, 0], color=METAL,
             stroke_width=5),
        Line([-0.55, -0.35, 0], [0.55, -0.35, 0], color=METAL,
             stroke_width=5),
        Line([0.55, -0.35, 0], [0.7, 0.55, 0], color=METAL,
             stroke_width=5),
    )
    wh = max(0.02, 0.85 * fill)
    water = Polygon(
        [-0.55 - 0.16 * (wh / 0.85), -0.35 + 0.001, 0],
        [0.55 + 0.16 * (wh / 0.85), -0.35 + 0.001, 0],
        [0.55 + 0.16 * (wh / 0.85), -0.35 + wh, 0],
        [-0.55 - 0.16 * (wh / 0.85), -0.35 + wh, 0],
        stroke_width=0, fill_color=WATER, fill_opacity=0.85)
    grp = VGroup(heater, water, cup)
    grp.scale(scale).move_to(pos)
    grp.heater = heater
    grp.cup = cup
    grp.water = water
    return grp


# ----------------------------------------------------------------------
# Countdown timer: a ring with a sweep wedge + digits. `frac` 1->0 is
# time remaining. Returns group with .set_frac via rebuild in scene.
# ----------------------------------------------------------------------
def countdown_timer(pos=ORIGIN, scale=1.0, frac=1.0, label=None):
    frac = float(np.clip(frac, 0.0, 1.0))
    ring = Circle(radius=0.7, stroke_color=DIM, stroke_width=3,
                  fill_opacity=0)
    if frac > 0.001:
        sweep = Sector(radius=0.66, angle=-TAU * (1.0 - frac),
                       start_angle=PI / 2)
        sweep.set_fill(HEAT, opacity=0.22)
        sweep.set_stroke(width=0)
    else:
        sweep = VGroup()
    secs = int(round(frac * 30))
    txt = Text(f"{secs:02d}", font="sans", font_size=30, color=CHALK)
    txt.move_to(ring.get_center())
    grp = VGroup(ring, sweep, txt)
    if label:
        lbl = Text(label, font="sans", font_size=18, color=DIM)
        lbl.next_to(ring, DOWN, buff=0.16)
        grp.add(lbl)
    grp.scale(scale).move_to(pos)
    grp.ring = ring
    return grp


# ----------------------------------------------------------------------
# Thermometer: a bulb + stem with a settable level. `level` is in
# degrees on a 0..110 scale (so it can stall at 0 and overshoot to boil).
# A 0deg tick and a 100deg (boil) tick are marked.
# ----------------------------------------------------------------------
def thermometer(pos=ORIGIN, scale=1.0, level=0.0):
    level = float(np.clip(level, -8.0, 112.0))
    stem_h = 3.0
    stem = RoundedRectangle(corner_radius=0.12, width=0.34,
                            height=stem_h, stroke_color=DIM,
                            stroke_width=2, fill_color=VOID,
                            fill_opacity=1)
    bulb = Circle(radius=0.30, fill_color=HEAT, fill_opacity=1,
                  stroke_color=DIM, stroke_width=2)
    bulb.move_to(stem.get_bottom() + DOWN * 0.10)

    y0 = stem.get_bottom()[1] + 0.05
    y1 = stem.get_top()[1] - 0.10
    yfill = y0 + (y1 - y0) * float(np.clip(level / 110.0, 0.0, 1.0))
    col = interpolate_color(ManimColor(WATER), ManimColor(HEAT),
                            float(np.clip(level / 110.0, 0, 1)))
    column = Line([0, y0, 0], [0, yfill, 0], color=col,
                  stroke_width=10)

    # ticks: 0deg and 100deg (boil)
    def tick(temp, lab):
        ty = y0 + (y1 - y0) * (temp / 110.0)
        t = Line([0.20, ty, 0], [0.42, ty, 0], color=DIM,
                 stroke_width=2)
        tl = Text(lab, font="sans", font_size=16, color=DIM)
        tl.next_to(t, RIGHT, buff=0.08)
        return VGroup(t, tl)

    t0 = tick(0, "0")
    t100 = tick(100, "100")

    grp = VGroup(stem, bulb, column, t0, t100)
    grp.scale(scale).move_to(pos)
    grp.stem = stem
    grp.bulb = bulb
    grp.column = column
    return grp


# ----------------------------------------------------------------------
# Energy ledger: stacked line-items with a label + a sized bar. Used for
# raise-temperature / hidden-melt / delivery-rate. Pass a list of
# (name, frac, color) tuples.
# ----------------------------------------------------------------------
def energy_ledger(items, pos=ORIGIN, scale=1.0, w=4.6, title=None):
    rows = VGroup()
    row_h = 0.62
    for idx, (name, frac, color) in enumerate(items):
        frac = float(np.clip(frac, 0.0, 1.0))
        y = -idx * row_h
        rule = Line([-w / 2, y - row_h / 2, 0],
                    [w / 2, y - row_h / 2, 0],
                    color=LEDGER, stroke_width=1.5).set_opacity(0.7)
        nm = Text(name, font="sans", font_size=20, color=CHALK)
        nm.move_to([-w / 2 + 0.1, y, 0]).align_to(
            [-w / 2 + 0.1, 0, 0], LEFT)
        bar_max = w * 0.42
        bar = Rectangle(width=max(0.02, frac * bar_max), height=0.20,
                        stroke_width=0, fill_color=color,
                        fill_opacity=1)
        bar.move_to([w / 2 - bar_max / 2, y, 0]).align_to(
            [w / 2 - 0.05, 0, 0], RIGHT)
        rows.add(VGroup(nm, bar, rule))
    grp = VGroup(rows)
    if title:
        tl = Text(title, font="sans", font_size=22, color=DIM)
        tl.next_to(rows, UP, buff=0.30)
        grp.add(tl)
    grp.scale(scale).move_to(pos)
    grp.rows = rows
    return grp


# ----------------------------------------------------------------------
# Temperature-vs-energy curve with a flat melting plateau.
# rise -> flat plateau (melt) -> rise -> flat plateau (boil cap).
# `progress` 0..1 reveals the curve up to that fraction; the plateau
# segment is highlighted in PLATEAU.
# ----------------------------------------------------------------------
def temp_energy_curve(pos=ORIGIN, scale=1.0, w=5.4, h=3.0,
                      progress=1.0, mark_plateau=True):
    progress = float(np.clip(progress, 0.0, 1.0))
    axes = VGroup(
        Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0], color=DIM,
             stroke_width=2),
        Line([-w / 2, -h / 2, 0], [-w / 2, h / 2, 0], color=DIM,
             stroke_width=2),
    )
    xlab = Text("energy in", font="sans", font_size=18, color=DIM)
    xlab.next_to(axes[0], DOWN, buff=0.14)
    ylab = Text("temp", font="sans", font_size=18, color=DIM)
    ylab.next_to(axes[1], LEFT, buff=0.14).rotate(PI / 2)

    # piecewise key points across the x-axis (fractions of width)
    x0, x1 = -w / 2, w / 2
    yb, yt = -h / 2, h / 2
    # segments: warm ice (0->0.12), MELT PLATEAU (0.12->0.55),
    # warm water (0.55->0.85), BOIL PLATEAU (0.85->1.0)
    keys = [
        (0.00, 0.10), (0.12, 0.22),   # ice warms to 0deg
        (0.55, 0.22),                  # MELT plateau (flat at 0deg)
        (0.85, 0.85),                  # water warms toward boil
        (1.00, 0.85),                  # BOIL plateau
    ]
    pts = []
    for fx, fy in keys:
        pts.append([x0 + (x1 - x0) * fx, yb + (yt - yb) * fy, 0])

    # Build as discrete Line segments (a VGroup) so a later
    # set_opacity() on a parent group never fills a closed region.
    curve = VGroup()
    for a, b in zip(pts[:-1], pts[1:]):
        curve.add(Line(a, b, color=CHALK, stroke_width=4))

    grp = VGroup(axes, xlab, ylab, curve)

    plateau_seg = None
    if mark_plateau:
        p_a = [x0 + (x1 - x0) * 0.12, yb + (yt - yb) * 0.22, 0]
        p_b = [x0 + (x1 - x0) * 0.55, yb + (yt - yb) * 0.22, 0]
        plateau_seg = Line(p_a, p_b, color=PLATEAU, stroke_width=6)
        plat_lbl = Text("melt — flat", font="sans", font_size=18,
                        color=PLATEAU)
        plat_lbl.next_to(plateau_seg, UP, buff=0.16)
        grp.add(plateau_seg, plat_lbl)

    grp.scale(scale).move_to(pos)
    grp.curve = curve
    grp.axes = axes
    grp.plateau_seg = plateau_seg
    return grp


# ----------------------------------------------------------------------
# Energy Forms and Changes layout: a heater, a beaker with water/ice,
# rising energy chunks, and a thermometer beside it.
# ----------------------------------------------------------------------
def efc_layout(pos=ORIGIN, scale=1.0, heat=0.55, melt=0.3,
               chunks=True):
    heater = make_heater([-0.1, -1.7, 0], scale=1.0, heat=heat)

    # beaker
    beaker = VGroup(
        Line([-0.85, 1.0, 0], [-0.85, -1.25, 0], color=METAL,
             stroke_width=4),
        Line([-0.85, -1.25, 0], [0.85, -1.25, 0], color=METAL,
             stroke_width=4),
        Line([0.85, -1.25, 0], [0.85, 1.0, 0], color=METAL,
             stroke_width=4),
    )
    water = Polygon([-0.83, -1.23, 0], [0.83, -1.23, 0],
                    [0.83, 0.2, 0], [-0.83, 0.2, 0],
                    stroke_width=0, fill_color=WATER,
                    fill_opacity=0.8)
    side = 0.7 * (1.0 - 0.7 * float(np.clip(melt, 0, 1)))
    ice = RoundedRectangle(corner_radius=0.05, width=side,
                           height=side, fill_color=ICE,
                           fill_opacity=0.92, stroke_color=ICE_EDGE,
                           stroke_width=2)
    ice.move_to([0, 0.2 + side / 2, 0])

    chunk_grp = VGroup()
    if chunks:
        rng = np.random.default_rng(7)
        for k in range(7):
            cx = -0.55 + rng.random() * 1.1
            cy = -1.0 + rng.random() * 1.0
            c = Square(side_length=0.16, stroke_width=0,
                       fill_color=HEAT, fill_opacity=0.9)
            c.move_to([cx, cy, 0])
            chunk_grp.add(c)

    thermo = thermometer([2.3, -0.1, 0], scale=0.7, level=2.0)

    grp = VGroup(heater, beaker, water, ice, chunk_grp, thermo)
    grp.scale(scale).move_to(pos)
    grp.heater = heater
    grp.beaker = beaker
    grp.water = water
    grp.ice = ice
    grp.chunks = chunk_grp
    grp.thermo = thermo
    return grp


# ----------------------------------------------------------------------
# UI bits.
# ----------------------------------------------------------------------
def play_button(pos=ORIGIN, r=0.42, color=CHALK):
    circ = Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_opacity=0)
    tri = Triangle(fill_color=color, fill_opacity=1, stroke_width=0)
    tri.scale(r * 0.55).rotate(-PI / 2)
    tri.move_to(circ.get_center() + RIGHT * r * 0.08)
    return VGroup(circ, tri).move_to(pos)


def heat_rate_control(pos=ORIGIN, frac=0.5, w=2.8, label="heat rate"):
    rail = Line(LEFT * w / 2, RIGHT * w / 2, color=DIM, stroke_width=3
                ).set_opacity(0.6)
    knob = Circle(radius=0.12, fill_color=HEAT, fill_opacity=1,
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
    lbl = Text(f"{total} tries", font="sans", font_size=20, color=DIM)
    lbl.next_to(g, DOWN, buff=0.16)
    return VGroup(g, lbl).move_to(pos)


def predict_vs_result(pos=ORIGIN, pred=0.4, res=0.7):
    base = Line(LEFT * 1.6, RIGHT * 1.6, color=DIM, stroke_width=2
                ).set_opacity(0.4)
    pbar = Rectangle(width=0.5, height=max(0.05, pred * 2.2),
                     fill_color=WATER, fill_opacity=1, stroke_width=0)
    rbar = Rectangle(width=0.5, height=max(0.05, res * 2.2),
                     fill_color=PLATEAU, fill_opacity=1, stroke_width=0)
    pbar.move_to(base.get_left() + RIGHT * 0.9 + UP * pbar.height / 2)
    rbar.move_to(base.get_right() + LEFT * 0.9 + UP * rbar.height / 2)
    pl = Text("predicted", font="sans", font_size=18, color=DIM
              ).next_to(pbar, DOWN, buff=0.14)
    rl = Text("result", font="sans", font_size=18, color=DIM
              ).next_to(rbar, DOWN, buff=0.14)
    return VGroup(base, pbar, rbar, pl, rl).move_to(pos)


def target_dotted(pos=ORIGIN, scale=1.0):
    """A dotted target: 'timer at 0' aligned with 'fully water'."""
    box = DashedVMobject(
        RoundedRectangle(corner_radius=0.1, width=4.2, height=1.5,
                         stroke_color=PLATEAU, stroke_width=3,
                         fill_opacity=0), num_dashes=42)
    t1 = Text("timer = 0", font="sans", font_size=24, color=CHALK)
    t1.move_to([-1.0, 0, 0])
    eq = Text("=", font="sans", font_size=28, color=DIM)
    eq.move_to([0.05, 0, 0])
    t2 = Text("fully water", font="sans", font_size=24, color=WATER)
    t2.move_to([1.25, 0, 0])
    g = VGroup(box, t1, eq, t2).scale(scale).move_to(pos)
    return g


# ----------------------------------------------------------------------
# Callback icons — must echo the four concept-video images.
#   match vs tub  : a tiny match flame vs a big steaming tub
#                   (temperature-vs-thermal)
#   water vs oil  : two pots, diverging thermometers (specific heat)
#   transfer triptych: spoon (conduction) / churning pot (convection) /
#                   Sun across space (radiation)  (heat transfer)
#   stuck thermo  : thermometer frozen at 0deg while ice drinks energy
#                   (latent heat)
# Faint by default: memories flickering in the void.
# ----------------------------------------------------------------------
def callback_match_tub(pos=ORIGIN, scale=1.0, opacity=0.85):
    # tiny match
    stick = Line([-1.7, -0.35, 0], [-1.7, 0.15, 0], color=METAL_DK,
                 stroke_width=3)
    flame = Ellipse(width=0.16, height=0.30, stroke_width=0,
                    fill_color=HEAT_BR, fill_opacity=1)
    flame.move_to([-1.7, 0.30, 0])
    m_lbl = Text("hot", font="sans", font_size=16, color=DIM)
    m_lbl.move_to([-1.7, -0.7, 0])
    # big steaming tub
    tub = VGroup(
        Line([0.5, 0.0, 0], [0.6, -0.7, 0], color=METAL,
             stroke_width=4),
        Line([0.6, -0.7, 0], [1.9, -0.7, 0], color=METAL,
             stroke_width=4),
        Line([1.9, -0.7, 0], [2.0, 0.0, 0], color=METAL,
             stroke_width=4))
    tub_w = Polygon([0.58, -0.68, 0], [1.92, -0.68, 0],
                    [1.95, -0.05, 0], [0.55, -0.05, 0],
                    stroke_width=0, fill_color=WATER,
                    fill_opacity=0.7)
    steam = VGroup()
    for sx in (0.9, 1.25, 1.6):
        steam.add(ArcBetweenPoints([sx, 0.05, 0], [sx + 0.1, 0.55, 0],
                                   angle=1.6).set_stroke(DIM, width=2))
    t_lbl = Text("more heat", font="sans", font_size=16, color=DIM)
    t_lbl.move_to([1.25, -1.0, 0])
    g = VGroup(stick, flame, m_lbl, tub, tub_w, steam, t_lbl)
    g.scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_water_oil(pos=ORIGIN, scale=1.0, opacity=0.85):
    def pot(cx, liq_col, lab, therm_level):
        body = VGroup(
            Line([cx - 0.55, 0.35, 0], [cx - 0.45, -0.45, 0],
                 color=METAL, stroke_width=4),
            Line([cx - 0.45, -0.45, 0], [cx + 0.45, -0.45, 0],
                 color=METAL, stroke_width=4),
            Line([cx + 0.45, -0.45, 0], [cx + 0.55, 0.35, 0],
                 color=METAL, stroke_width=4))
        liq = Polygon([cx - 0.47, -0.43, 0], [cx + 0.47, -0.43, 0],
                      [cx + 0.50, 0.05, 0], [cx - 0.50, 0.05, 0],
                      stroke_width=0, fill_color=liq_col,
                      fill_opacity=0.8)
        # mini thermometer rising out of the pot
        stem = Line([cx, 0.1, 0], [cx, 0.1 + 0.9, 0], color=DIM,
                    stroke_width=3)
        col = Line([cx, 0.1, 0],
                   [cx, 0.1 + 0.9 * therm_level, 0],
                   color=HEAT, stroke_width=6)
        l = Text(lab, font="sans", font_size=16, color=DIM)
        l.move_to([cx, -0.75, 0])
        return VGroup(body, liq, stem, col, l)
    water_pot = pot(-1.1, WATER, "water", 0.30)
    oil_pot = pot(1.1, OIL, "oil", 0.92)
    g = VGroup(water_pot, oil_pot).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_transfer(pos=ORIGIN, scale=1.0, opacity=0.85):
    # conduction: a spoon in a pot, heat creeping up the handle
    spoon = VGroup(
        Line([-3.2, -0.5, 0], [-3.0, 0.45, 0], color=METAL,
             stroke_width=5),
        Arc(radius=0.14, start_angle=PI, angle=PI,
            arc_center=[-3.22, -0.55, 0]).set_stroke(METAL, width=5))
    cond_dots = VGroup(*[Dot([-3.13 + 0.04 * k, -0.2 + 0.18 * k, 0],
                             radius=0.05, color=HEAT)
                         for k in range(4)])
    c1 = Text("conduction", font="sans", font_size=15, color=DIM
              ).move_to([-3.1, -1.0, 0])

    # convection: a pot with a churning loop arrow
    pot = VGroup(
        Line([-0.7, 0.3, 0], [-0.6, -0.5, 0], color=METAL,
             stroke_width=4),
        Line([-0.6, -0.5, 0], [0.6, -0.5, 0], color=METAL,
             stroke_width=4),
        Line([0.6, -0.5, 0], [0.7, 0.3, 0], color=METAL,
             stroke_width=4))
    loop = VGroup(
        CurvedArrow([-0.3, -0.35, 0], [0.0, 0.15, 0], angle=-1.8,
                    color=HEAT, stroke_width=3, tip_length=0.14),
        CurvedArrow([0.3, 0.15, 0], [0.0, -0.35, 0], angle=-1.8,
                    color=HEAT, stroke_width=3, tip_length=0.14))
    c2 = Text("convection", font="sans", font_size=15, color=DIM
              ).move_to([0, -1.0, 0])

    # radiation: a Sun emitting rays across empty space
    sun = Circle(radius=0.26, fill_color=SUN_C, fill_opacity=1,
                 stroke_width=0).move_to([3.0, 0.15, 0])
    rays = VGroup()
    for a in np.linspace(0, TAU, 9)[:-1]:
        d = np.array([np.cos(a), np.sin(a), 0])
        rays.add(Line([3.0, 0.15, 0] + d * 0.34,
                      [3.0, 0.15, 0] + d * 0.58,
                      color=SUN_C, stroke_width=3))
    c3 = Text("radiation", font="sans", font_size=15, color=DIM
              ).move_to([3.0, -1.0, 0])

    g = VGroup(spoon, cond_dots, c1, pot, loop, c2, sun, rays, c3)
    g.scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def callback_stuck_thermo(pos=ORIGIN, scale=1.0, opacity=0.85):
    th = thermometer([0, 0, 0], scale=0.85, level=0.0)
    # an ice cube beside it "drinking" energy chunks
    ice = RoundedRectangle(corner_radius=0.05, width=0.6, height=0.6,
                           fill_color=ICE, fill_opacity=0.9,
                           stroke_color=ICE_EDGE, stroke_width=2)
    ice.move_to([1.5, -0.3, 0])
    chunks = VGroup()
    for k in range(3):
        c = Square(side_length=0.14, stroke_width=0,
                   fill_color=HEAT, fill_opacity=0.9)
        c.move_to([1.0 + k * 0.18, 0.3 - k * 0.1, 0])
        chunks.add(c)
    z = Text("0", font="sans", font_size=20, color=PLATEAU)
    z.next_to(th, RIGHT, buff=0.05).shift(DOWN * 0.9)
    g = VGroup(th, ice, chunks, z).scale(scale).move_to(pos)
    g.set_opacity(opacity)
    return g


def small_label(text, pos, color=CHALK, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def qmark(pos, size=48, color=DIM, opacity=0.6):
    return Text("?", font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
