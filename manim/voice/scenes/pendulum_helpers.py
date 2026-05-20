"""
Shared helpers for the pendulum / conservation-of-energy scene.

Same conventions as grav_helpers / rocket_helpers:
- VOID #000000 background
- Text uses font="sans"
- All shapes from primitive Mobjects; no SVGs
"""

from manim import *
import numpy as np


VOID = "#000000"

# Palette
STRING_COLOR  = "#B0B5BE"
BOB_COLOR     = "#C7402D"          # warm red bob — easy to track
BOB_HI        = "#FFB69E"
PIVOT_COLOR   = "#888B92"
WALLET_BROWN  = "#7B4A22"
WALLET_DARK   = "#3D2510"
BILL_GREEN    = "#3F8B5E"
BILL_LINE     = "#1F4E33"
BILL_TEXT     = "#F4F8F1"
RECEIPT_WHITE = "#EAE4D5"
RECEIPT_LINE  = "#9C937A"
TABLE_WOOD    = "#5C3A1F"
COFFEE_BROWN  = "#3A2010"
COFFEE_CUP    = "#D4B999"
PARK_BLUE     = "#2F62A8"
PARK_WHITE    = "#F0F2F5"
BAG_BROWN     = "#C8A375"
BAG_HANDLE    = "#8C6738"
MOLECULE      = "#7BC9FF"
MOLECULE_HOT  = "#FF8A4A"
HEAT_GLOW     = "#FFB55C"
THERM_GLASS   = "#D5D8DE"
THERM_RED     = "#D03A1B"
BRAKE_GLOW    = "#FF5A1A"
PHONE_BLACK   = "#1A1A22"
PHONE_GLASS   = "#2C3340"
SOUND_WAVE    = "#F0F4FA"
BALL_BLUE     = "#3B6AB0"
FLOOR_GREY    = "#3A3D44"


# -----------------------------------------------------------------------------
# Pendulum
# -----------------------------------------------------------------------------

def make_pendulum(pivot=np.array([0, 3.0, 0]), length=4.0, bob_r=0.42,
                  angle=0.0):
    """
    Pendulum hanging from `pivot`, with a given rod length and bob radius.
    `angle` is in radians, measured from straight down (negative = swing left).
    Returns VGroup(pivot_dot, string, bob, bob_highlight).
    """
    pivot_dot = Circle(radius=0.10, fill_color=PIVOT_COLOR, fill_opacity=1,
                       stroke_color="#5A5C62", stroke_width=1.2
                       ).move_to(pivot)
    bob_pos = pivot + length * np.array([np.sin(angle), -np.cos(angle), 0])
    string = Line(pivot, bob_pos, stroke_color=STRING_COLOR, stroke_width=2.5)
    bob = Circle(radius=bob_r, fill_color=BOB_COLOR, fill_opacity=1,
                 stroke_color="#8A2A1C", stroke_width=2.0).move_to(bob_pos)
    hl = Ellipse(width=bob_r*0.6, height=bob_r*0.3, fill_color=BOB_HI,
                 fill_opacity=0.65, stroke_width=0
                 ).move_to(bob_pos + LEFT*bob_r*0.20 + UP*bob_r*0.30)
    return VGroup(pivot_dot, string, bob, hl)


def pendulum_at_angle(pivot, length, angle, bob_r=0.42):
    """Convenience — returns just the bob/string/highlight positions for an angle."""
    bob_pos = pivot + length * np.array([np.sin(angle), -np.cos(angle), 0])
    return bob_pos


# -----------------------------------------------------------------------------
# Wallet & money
# -----------------------------------------------------------------------------

def make_table(y=-2.6, width=14.0):
    """Wooden table strip across frame bottom."""
    strip = Rectangle(width=width, height=0.50,
                      fill_color=TABLE_WOOD, fill_opacity=1,
                      stroke_color="#3A2410", stroke_width=1.2
                      ).move_to([0, y, 0])
    # grain lines
    grain = VGroup()
    for x in np.linspace(-width/2 + 1.0, width/2 - 1.0, 6):
        ln = Line([x, y+0.10, 0], [x+0.4, y-0.10, 0],
                  stroke_color="#3A2410", stroke_width=1).set_opacity(0.40)
        grain.add(ln)
    return VGroup(strip, grain)


def make_wallet(center=np.array([0, -1.4, 0]), scale=1.0, open_=False):
    """A wallet, closed or open."""
    if open_:
        # open: two flaps side by side
        left = RoundedRectangle(width=1.6, height=1.0, corner_radius=0.10,
                                fill_color=WALLET_BROWN, fill_opacity=1,
                                stroke_color=WALLET_DARK, stroke_width=1.6
                                ).shift(LEFT*0.85)
        right = left.copy().shift(RIGHT*1.70)
        stitch_l = DashedVMobject(
            RoundedRectangle(width=1.42, height=0.82, corner_radius=0.06)
            .shift(LEFT*0.85).set_stroke(WALLET_DARK, 1), num_dashes=24
        )
        stitch_r = DashedVMobject(
            RoundedRectangle(width=1.42, height=0.82, corner_radius=0.06)
            .shift(RIGHT*0.85).set_stroke(WALLET_DARK, 1), num_dashes=24
        )
        g = VGroup(left, right, stitch_l, stitch_r)
    else:
        body = RoundedRectangle(width=2.2, height=1.30, corner_radius=0.12,
                                fill_color=WALLET_BROWN, fill_opacity=1,
                                stroke_color=WALLET_DARK, stroke_width=1.6)
        seam = Line(LEFT*1.0, RIGHT*1.0,
                    stroke_color=WALLET_DARK, stroke_width=1.4).set_opacity(0.7)
        stitch = DashedVMobject(
            RoundedRectangle(width=1.96, height=1.06, corner_radius=0.06)
            .set_stroke(WALLET_DARK, 1), num_dashes=32
        )
        g = VGroup(body, seam, stitch)
    return g.scale(scale).move_to(center)


def make_bill(value="50", center=np.array([0, 0, 0]), scale=1.0):
    """A single banknote, with denomination text in the middle."""
    body = RoundedRectangle(width=1.4, height=0.70, corner_radius=0.04,
                            fill_color=BILL_GREEN, fill_opacity=1,
                            stroke_color=BILL_LINE, stroke_width=1.2)
    inner = RoundedRectangle(width=1.24, height=0.54, corner_radius=0.03,
                             fill_color=BILL_GREEN, fill_opacity=1,
                             stroke_color=BILL_LINE, stroke_width=1.0
                             ).set_opacity(0.95)
    num = Text(value, font="sans", font_size=26, color=BILL_TEXT,
               weight=BOLD).move_to(ORIGIN)
    return VGroup(body, inner, num).scale(scale).move_to(center)


def make_bill_stack(value="50", count=3, center=np.array([0, 0, 0]), scale=1.0):
    """A small fanned stack of bills."""
    g = VGroup()
    for i in range(count):
        b = make_bill(value=value, center=ORIGIN, scale=scale)
        b.shift(RIGHT*(0.06*i) + UP*(0.04*i))
        b.set_opacity(0.96 if i < count - 1 else 1.0)
        g.add(b)
    g.move_to(center)
    return g


def make_receipt(center=np.array([0, 0, 0]), scale=1.0, icon=None,
                 label=None):
    """
    A small paper receipt. Optional small icon at top, optional label text below.
    icon: one of None, 'coffee', 'parking', 'bag'
    """
    paper = Polygon(
        [-0.40, 0.55, 0], [0.40, 0.55, 0],
        [0.40, -0.40, 0], [0.32, -0.50, 0],
        [0.20, -0.40, 0], [0.08, -0.50, 0],
        [-0.04, -0.40, 0], [-0.16, -0.50, 0],
        [-0.28, -0.40, 0], [-0.40, -0.50, 0],
        fill_color=RECEIPT_WHITE, fill_opacity=1,
        stroke_color="#666158", stroke_width=1.0,
    )
    lines = VGroup()
    for y in [0.32, 0.16, 0.0, -0.16]:
        ln = Line([-0.30, y, 0], [0.30, y, 0],
                  stroke_color=RECEIPT_LINE, stroke_width=1.2).set_opacity(0.65)
        lines.add(ln)

    g = VGroup(paper, lines)

    if icon == "coffee":
        ic = _icon_coffee()
    elif icon == "parking":
        ic = _icon_parking()
    elif icon == "bag":
        ic = _icon_bag()
    else:
        ic = None
    if ic is not None:
        ic.scale(0.50).move_to([0, 0.34, 0])
        g.add(ic)

    if label:
        lbl = Text(label, font="sans", font_size=14,
                   color="#444039").move_to([0, -0.70, 0])
        g.add(lbl)

    return g.scale(scale).move_to(center)


def _icon_coffee():
    cup = Polygon([-0.30, 0.30, 0], [0.28, 0.30, 0],
                  [0.22, -0.30, 0], [-0.24, -0.30, 0],
                  fill_color=COFFEE_CUP, fill_opacity=1,
                  stroke_color="#5A3A20", stroke_width=1.5)
    coffee = Rectangle(width=0.48, height=0.10, fill_color=COFFEE_BROWN,
                       fill_opacity=1, stroke_width=0).shift(UP*0.22)
    handle = ArcBetweenPoints([0.28, 0.18, 0], [0.28, -0.18, 0], angle=-PI*0.9
                              ).set_stroke("#5A3A20", 2.5)
    steam = VMobject(stroke_color="#CCCCCC", stroke_width=1.8)
    pts = [[-0.05, 0.45, 0], [0.05, 0.55, 0], [-0.05, 0.65, 0], [0.05, 0.75, 0]]
    steam.set_points_smoothly(pts).set_stroke(opacity=0.7)
    return VGroup(cup, coffee, handle, steam)


def _icon_parking():
    box = RoundedRectangle(width=0.60, height=0.60, corner_radius=0.08,
                           fill_color=PARK_BLUE, fill_opacity=1,
                           stroke_color="#1A3D70", stroke_width=1.5)
    p = Text("P", font="sans", font_size=42, weight=BOLD, color=PARK_WHITE)
    return VGroup(box, p)


def _icon_bag():
    body = Polygon([-0.30, -0.35, 0], [0.30, -0.35, 0],
                   [0.34, 0.30, 0], [-0.34, 0.30, 0],
                   fill_color=BAG_BROWN, fill_opacity=1,
                   stroke_color="#5A3A20", stroke_width=1.4)
    handle_l = ArcBetweenPoints([-0.20, 0.30, 0], [-0.05, 0.30, 0], angle=-PI*0.95
                                ).set_stroke(BAG_HANDLE, 2.2)
    handle_r = ArcBetweenPoints([0.05, 0.30, 0], [0.20, 0.30, 0], angle=-PI*0.95
                                ).set_stroke(BAG_HANDLE, 2.2)
    return VGroup(body, handle_l, handle_r)


# -----------------------------------------------------------------------------
# Air molecules
# -----------------------------------------------------------------------------

def make_molecule_field(n=80, seed=42, x_range=(-6.0, 6.0), y_range=(-3.0, 3.0),
                        radius=0.06, color=MOLECULE, opacity=0.55):
    """A field of small dots representing air molecules."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for _ in range(n):
        x = rng.uniform(*x_range)
        y = rng.uniform(*y_range)
        d = Dot(point=[x, y, 0], radius=radius, color=color).set_opacity(opacity)
        g.add(d)
    return g


def heat_overlay(width=14, height=8, opacity=0.0, color=HEAT_GLOW):
    """Full-frame warm tint overlay (animate opacity to suggest heating)."""
    return Rectangle(width=width, height=height,
                     fill_color=color, fill_opacity=opacity,
                     stroke_width=0)


# -----------------------------------------------------------------------------
# Thermometer
# -----------------------------------------------------------------------------

def make_thermometer(center=np.array([0,0,0]), height=2.2,
                     fill_frac=0.30, color=THERM_RED):
    """
    Simple thermometer: bulb + tube. `fill_frac` ∈ [0,1] sets red column height.
    """
    bulb = Circle(radius=0.30, fill_color=color, fill_opacity=1,
                  stroke_color="#444751", stroke_width=2.0
                  ).move_to(center + DOWN*(height/2 - 0.20))
    tube_h = height - 0.55
    tube_back = RoundedRectangle(width=0.30, height=tube_h, corner_radius=0.14,
                                 fill_color=THERM_GLASS, fill_opacity=1,
                                 stroke_color="#444751", stroke_width=1.6
                                 ).move_to(center + UP*0.10)
    fill_h = max(0.05, tube_h * fill_frac)
    tube_fill = Rectangle(width=0.16, height=fill_h, fill_color=color,
                          fill_opacity=1, stroke_width=0)
    tube_fill.move_to(tube_back.get_bottom() + UP*fill_h/2 + UP*0.06)
    return VGroup(bulb, tube_back, tube_fill)


# -----------------------------------------------------------------------------
# Brake disc (glowing)
# -----------------------------------------------------------------------------

def make_brake_disc(center=np.array([0,0,0]), radius=1.0, hot=False):
    base = Circle(radius=radius, fill_color="#3C4048", fill_opacity=1,
                  stroke_color="#1F2128", stroke_width=2.0)
    inner = Circle(radius=radius*0.35, fill_color="#1F2128", fill_opacity=1,
                   stroke_color="#0E1014", stroke_width=1.4)
    # ventilation slots
    slots = VGroup()
    for i in range(8):
        ang = i * (TAU / 8)
        slot = Rectangle(width=radius*0.10, height=radius*0.45,
                         fill_color="#1F2128", fill_opacity=1, stroke_width=0)
        slot.move_to([radius*0.62*np.cos(ang), radius*0.62*np.sin(ang), 0])
        slot.rotate(ang)
        slots.add(slot)
    g = VGroup(base, slots, inner).move_to(center)
    if hot:
        glow = Circle(radius=radius*1.05, fill_color=BRAKE_GLOW,
                      fill_opacity=0.55, stroke_width=0).move_to(center)
        inner_glow = Circle(radius=radius*0.80, fill_color="#FFB55C",
                            fill_opacity=0.40, stroke_width=0).move_to(center)
        return VGroup(glow, inner_glow, g)
    return g


# -----------------------------------------------------------------------------
# Bouncing ball
# -----------------------------------------------------------------------------

def make_ball(center=np.array([0,0,0]), radius=0.30, color=BALL_BLUE):
    body = Circle(radius=radius, fill_color=color, fill_opacity=1,
                  stroke_color="#1F3E70", stroke_width=1.6)
    hl = Ellipse(width=radius*0.6, height=radius*0.3, fill_color=WHITE,
                 fill_opacity=0.45, stroke_width=0
                 ).shift(LEFT*radius*0.20 + UP*radius*0.30)
    return VGroup(body, hl).move_to(center)


def make_floor(y=-2.0, width=14.0, color=FLOOR_GREY):
    line = Line([-width/2, y, 0], [width/2, y, 0],
                stroke_color=color, stroke_width=3)
    strip = Rectangle(width=width, height=0.18,
                      fill_color=color, fill_opacity=1,
                      stroke_width=0).move_to([0, y-0.10, 0])
    return VGroup(strip, line)


def sound_wave(center=np.array([0,0,0]), n=3, base_r=0.30, color=SOUND_WAVE):
    """Concentric arcs (sound wave fronts) emanating from a point."""
    g = VGroup()
    for i in range(n):
        r = base_r * (i + 1)
        arc = Arc(radius=r, angle=PI*0.6, start_angle=PI*0.2,
                  color=color, stroke_width=2.4).set_opacity(0.55 - 0.13*i)
        arc.move_arc_center_to(center)
        g.add(arc)
    return g


# -----------------------------------------------------------------------------
# Phone (with warm aura)
# -----------------------------------------------------------------------------

def make_phone(center=np.array([0,0,0]), scale=1.0, hot=False):
    body = RoundedRectangle(width=1.10, height=2.10, corner_radius=0.18,
                            fill_color=PHONE_BLACK, fill_opacity=1,
                            stroke_color="#3A3D44", stroke_width=1.6)
    screen = RoundedRectangle(width=0.92, height=1.78, corner_radius=0.10,
                              fill_color=PHONE_GLASS, fill_opacity=1,
                              stroke_width=0)
    notch = Rectangle(width=0.30, height=0.06, fill_color="#0E1014",
                      fill_opacity=1, stroke_width=0).shift(UP*0.82)
    g = VGroup(body, screen, notch)
    if hot:
        aura = Circle(radius=1.3, fill_color=HEAT_GLOW, fill_opacity=0.30,
                      stroke_width=0)
        g = VGroup(aura, g)
    return g.scale(scale).move_to(center)


def make_hand(center=np.array([0,0,0]), scale=1.0):
    """Simple cupped palm shape (under-phone)."""
    palm = RoundedRectangle(width=2.4, height=0.55, corner_radius=0.20,
                            fill_color="#D5A887", fill_opacity=1,
                            stroke_color="#7A4A28", stroke_width=1.2)
    # 4 stub fingers
    fingers = VGroup()
    for x in [-0.7, -0.25, 0.20, 0.65]:
        f = RoundedRectangle(width=0.30, height=0.25, corner_radius=0.10,
                             fill_color="#D5A887", fill_opacity=1,
                             stroke_color="#7A4A28", stroke_width=1.0
                             ).move_to([x, 0.35, 0])
        fingers.add(f)
    thumb = RoundedRectangle(width=0.36, height=0.20, corner_radius=0.08,
                             fill_color="#D5A887", fill_opacity=1,
                             stroke_color="#7A4A28", stroke_width=1.0
                             ).move_to([-1.20, 0.10, 0])
    return VGroup(palm, fingers, thumb).scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Small label helper
# -----------------------------------------------------------------------------

def small_label(text, pos, color=WHITE, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
