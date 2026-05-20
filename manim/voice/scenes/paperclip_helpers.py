"""Helpers for the E = mc² / paperclip scene."""

from manim import *
import numpy as np


VOID = "#000000"

# Palette
SKIN_TONE   = "#D5A887"
SKIN_SHADE  = "#9C7A5A"
WIRE_SILVER = "#C5C8CE"
WIRE_HILITE = "#E8EAEE"
WATER_BLUE  = "#5AA8D4"
ICE_BLUE    = "#C9E8F2"
GLASS_LINE  = "#EAE4D5"
SOFA_COLOR  = "#624B36"
SOFA_DARK   = "#3A2A1C"
CUSHION_HI  = "#8C6B4F"
BADGE_BG    = "#1E2A40"
BADGE_GLOW  = "#7FB7FF"
PADLOCK_BODY= "#3A3D44"
PADLOCK_HI  = "#7E8290"
SHACKLE     = "#5A5C62"
FIRE_RED    = "#E64A1A"
FIRE_YEL    = "#FFE08A"
GAS_BLUE    = "#7FB7FF"
EXPL_ORANGE = "#FF8A4A"
MUSH_GREY   = "#5A5C62"
MUSH_BRT    = "#9CA0A8"
CITY_DARK   = "#22272E"
GLOW_AMBER  = "#FFC36E"
PHONE_DARK  = "#1A1A22"
COFFEE_CUP  = "#D4B999"
COFFEE_BR   = "#3A2010"


# -----------------------------------------------------------------------------
# Hand (palm up, viewed from above)
# -----------------------------------------------------------------------------

def make_palm(center=np.array([0, -0.8, 0]), scale=1.0):
    """Palm-up hand, viewed from slightly above."""
    palm = RoundedRectangle(width=3.2, height=1.5, corner_radius=0.45,
                            fill_color=SKIN_TONE, fill_opacity=1,
                            stroke_color=SKIN_SHADE, stroke_width=1.6)
    # subtle palm crease lines
    crease1 = ArcBetweenPoints([-1.1, 0.15, 0], [0.8, 0.10, 0], angle=-0.4
                               ).set_stroke(SKIN_SHADE, 1).set_opacity(0.5)
    crease2 = ArcBetweenPoints([-1.0, -0.15, 0], [0.6, -0.20, 0], angle=-0.3
                               ).set_stroke(SKIN_SHADE, 1).set_opacity(0.5)
    # fingertips peeking at top of frame
    fingers = VGroup()
    finger_xs = [-0.95, -0.30, 0.30, 0.95]
    for x in finger_xs:
        f = RoundedRectangle(width=0.42, height=0.42, corner_radius=0.16,
                             fill_color=SKIN_TONE, fill_opacity=1,
                             stroke_color=SKIN_SHADE, stroke_width=1.4
                             ).move_to([x, 0.85, 0])
        fingers.add(f)
    thumb = RoundedRectangle(width=0.55, height=0.36, corner_radius=0.15,
                             fill_color=SKIN_TONE, fill_opacity=1,
                             stroke_color=SKIN_SHADE, stroke_width=1.4
                             ).move_to([-1.85, -0.10, 0]).rotate(0.40)
    g = VGroup(palm, crease1, crease2, fingers, thumb)
    g.scale(scale).move_to(center)
    return g


# -----------------------------------------------------------------------------
# Paperclip
# -----------------------------------------------------------------------------

def make_paperclip(center=np.array([0, 0, 0]), scale=1.0,
                   color=WIRE_SILVER):
    """
    Classic gem-style paperclip — three nested oval loops, drawn as
    stroke-only rounded rectangles (no fill) so it reads as a bent wire.
    """
    outer = RoundedRectangle(width=1.50, height=0.55, corner_radius=0.27,
                             stroke_color=color, stroke_width=5,
                             fill_opacity=0)
    middle = RoundedRectangle(width=1.20, height=0.40, corner_radius=0.20,
                              stroke_color=color, stroke_width=5,
                              fill_opacity=0).shift(RIGHT*0.10)
    inner = RoundedRectangle(width=0.90, height=0.25, corner_radius=0.12,
                             stroke_color=color, stroke_width=5,
                             fill_opacity=0).shift(RIGHT*0.20)
    hl = Line([-0.50, 0.27, 0], [0.40, 0.27, 0],
              stroke_color=WIRE_HILITE, stroke_width=2).set_opacity(0.70)
    return VGroup(outer, middle, inner, hl).scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Sofa with cushions
# -----------------------------------------------------------------------------

def make_sofa(center=np.array([0, -1.3, 0]), scale=1.0):
    """Simple side-on sofa with two cushion bumps."""
    base = RoundedRectangle(width=5.5, height=0.9, corner_radius=0.20,
                            fill_color=SOFA_COLOR, fill_opacity=1,
                            stroke_color=SOFA_DARK, stroke_width=1.6
                            ).move_to([0, -0.4, 0])
    backrest = RoundedRectangle(width=5.5, height=1.4, corner_radius=0.25,
                                fill_color=SOFA_COLOR, fill_opacity=1,
                                stroke_color=SOFA_DARK, stroke_width=1.6
                                ).move_to([0, 0.7, 0])
    # cushions (two bumps)
    c1 = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.20,
                          fill_color=CUSHION_HI, fill_opacity=1,
                          stroke_color=SOFA_DARK, stroke_width=1.4
                          ).move_to([-1.35, 0.1, 0])
    c2 = c1.copy().move_to([1.35, 0.1, 0])
    # armrests
    arm_l = RoundedRectangle(width=0.55, height=1.7, corner_radius=0.15,
                             fill_color=SOFA_DARK, fill_opacity=1,
                             stroke_width=0).move_to([-2.85, 0.4, 0])
    arm_r = arm_l.copy().shift(RIGHT*5.7)
    legs = VGroup(
        Rectangle(width=0.20, height=0.30, fill_color=SOFA_DARK,
                  fill_opacity=1, stroke_width=0).move_to([-2.5, -0.95, 0]),
        Rectangle(width=0.20, height=0.30, fill_color=SOFA_DARK,
                  fill_opacity=1, stroke_width=0).move_to([2.5, -0.95, 0]),
    )
    g = VGroup(legs, base, backrest, c1, c2, arm_l, arm_r)
    g.scale(scale).move_to(center)
    return g


# -----------------------------------------------------------------------------
# Glass of water (with phase transitions)
# -----------------------------------------------------------------------------

def make_glass(center=np.array([0, 0, 0]), scale=1.0, contents="water"):
    """
    A simple cylinder-style glass. contents ∈ {'water', 'ice', 'empty'}.
    """
    # glass outline — slightly trapezoid-ish (narrower at bottom)
    outline = Polygon(
        [-0.65, 1.0, 0], [0.65, 1.0, 0],
        [0.55, -1.0, 0], [-0.55, -1.0, 0],
        fill_color=GLASS_LINE, fill_opacity=0.10,
        stroke_color=GLASS_LINE, stroke_width=2.0,
    )
    g = VGroup(outline)
    if contents == "water":
        water = Polygon(
            [-0.62, 0.40, 0], [0.62, 0.40, 0],
            [0.55, -0.96, 0], [-0.55, -0.96, 0],
            fill_color=WATER_BLUE, fill_opacity=0.85,
            stroke_color="#3A85B0", stroke_width=1.2,
        )
        surface = Line([-0.62, 0.40, 0], [0.62, 0.40, 0],
                       stroke_color="#A8D8F0", stroke_width=2)
        g.add(water, surface)
    elif contents == "ice":
        # Glass interior fill so the ice has something to contrast against
        interior = Polygon(
            [-0.62, 0.96, 0], [0.62, 0.96, 0],
            [0.53, -0.96, 0], [-0.53, -0.96, 0],
            fill_color="#3A4860", fill_opacity=0.55, stroke_width=0,
        )
        cube = RoundedRectangle(width=1.00, height=1.00, corner_radius=0.10,
                                fill_color=ICE_BLUE, fill_opacity=1.0,
                                stroke_color="#FFFFFF", stroke_width=2.0
                                ).move_to([0, -0.10, 0])
        glint = Line([-0.30, 0.20, 0], [-0.05, -0.05, 0],
                     stroke_color=WHITE, stroke_width=3).set_opacity(0.95)
        g.add(interior, cube, glint)
    return g.scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Badge — circular emblem for "matter ↔ energy"
# -----------------------------------------------------------------------------

def make_badge(center=np.array([0, 0, 0]), radius=2.0):
    outer = Circle(radius=radius, fill_color=BADGE_BG, fill_opacity=1,
                   stroke_color=BADGE_GLOW, stroke_width=3.0)
    inner = Circle(radius=radius * 0.88, fill_color=BADGE_BG, fill_opacity=1,
                   stroke_color="#3A4860", stroke_width=1.2)
    return VGroup(outer, inner).move_to(center)


# -----------------------------------------------------------------------------
# City silhouette + mushroom cloud
# -----------------------------------------------------------------------------

def make_city(center=np.array([0, 0, 0]), width=4.0):
    """Boxy skyline."""
    base_y = -0.6
    g = VGroup()
    # ground line
    ground = Line([-width/2, base_y, 0], [width/2, base_y, 0],
                  stroke_color=CITY_DARK, stroke_width=2)
    g.add(ground)
    # buildings (random-ish heights)
    rng = np.random.default_rng(11)
    x = -width/2
    while x < width/2:
        bw = rng.uniform(0.30, 0.55)
        bh = rng.uniform(0.40, 1.20)
        b = Rectangle(width=bw, height=bh,
                      fill_color=CITY_DARK, fill_opacity=1,
                      stroke_color="#0E1014", stroke_width=1
                      ).move_to([x + bw/2, base_y + bh/2, 0])
        # window dots
        wins = VGroup()
        for wy in np.arange(base_y + 0.15, base_y + bh - 0.1, 0.20):
            for wx in np.arange(x + 0.08, x + bw - 0.05, 0.18):
                if rng.random() < 0.35:
                    w = Dot(point=[wx + 0.04, wy, 0], radius=0.025,
                            color="#FFE08A").set_opacity(0.7)
                    wins.add(w)
        g.add(b, wins)
        x += bw + rng.uniform(0.04, 0.10)
    return g.move_to(center)


def make_mushroom(center=np.array([0, 0.5, 0]), scale=1.0):
    """Mushroom cloud silhouette."""
    cap = Ellipse(width=2.2, height=1.1, fill_color=MUSH_BRT, fill_opacity=0.92,
                  stroke_color=MUSH_GREY, stroke_width=1.4
                  ).move_to([0, 0.7, 0])
    cap_top = Ellipse(width=1.6, height=0.7, fill_color="#C5C8CE",
                      fill_opacity=0.95, stroke_width=0
                      ).move_to([0, 1.05, 0])
    stem = Polygon(
        [-0.40, 0.5, 0], [-0.55, -0.30, 0],
        [-0.30, -1.30, 0], [ 0.30, -1.30, 0],
        [ 0.55, -0.30, 0], [ 0.40, 0.5, 0],
        fill_color=MUSH_GREY, fill_opacity=0.85, stroke_width=0,
    )
    # debris puffs
    puff1 = Circle(radius=0.30, fill_color=MUSH_GREY, fill_opacity=0.65,
                   stroke_width=0).move_to([-0.85, 0.30, 0])
    puff2 = Circle(radius=0.24, fill_color=MUSH_GREY, fill_opacity=0.55,
                   stroke_width=0).move_to([0.85, 0.30, 0])
    return VGroup(stem, puff1, puff2, cap, cap_top).scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Padlock
# -----------------------------------------------------------------------------

def make_padlock(center=np.array([0, 0, 0]), scale=1.0, cracked=False):
    body = RoundedRectangle(width=1.4, height=1.5, corner_radius=0.18,
                            fill_color=PADLOCK_BODY, fill_opacity=1,
                            stroke_color="#1F2128", stroke_width=2.0)
    hl = Rectangle(width=1.20, height=0.10, fill_color=PADLOCK_HI,
                   fill_opacity=0.55, stroke_width=0
                   ).shift(UP*0.45)
    shackle = ArcBetweenPoints([-0.50, 0.75, 0], [0.50, 0.75, 0], angle=-PI*0.95
                               ).set_stroke(SHACKLE, 12)
    keyhole = Circle(radius=0.10, fill_color="#0E1014", fill_opacity=1,
                     stroke_width=0).shift(DOWN*0.05)
    key_slot = Rectangle(width=0.10, height=0.25, fill_color="#0E1014",
                         fill_opacity=1, stroke_width=0).shift(DOWN*0.25)
    g = VGroup(shackle, body, hl, keyhole, key_slot)
    if cracked:
        # crack lines across body
        c1 = Line([-0.30, 0.35, 0], [0.10, 0.05, 0], stroke_color="#FFE08A", stroke_width=2.4)
        c2 = Line([0.10, 0.05, 0], [-0.05, -0.30, 0], stroke_color="#FFE08A", stroke_width=2.4)
        c3 = Line([0.10, 0.05, 0], [0.40, -0.25, 0], stroke_color="#FFE08A", stroke_width=2.4)
        g.add(c1, c2, c3)
    return g.scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Small icon helpers
# -----------------------------------------------------------------------------

def icon_campfire(center=np.array([0,0,0]), scale=1.0):
    log1 = Rectangle(width=0.7, height=0.10, fill_color="#5A3A20",
                     fill_opacity=1, stroke_width=0
                     ).rotate(0.35).move_to(DOWN*0.30)
    log2 = log1.copy().rotate(-0.70).move_to(DOWN*0.30 + RIGHT*0.05)
    flame_outer = Polygon([-0.25, -0.10, 0], [-0.18, 0.20, 0],
                          [0.0, 0.50, 0], [0.18, 0.20, 0], [0.25, -0.10, 0],
                          fill_color=FIRE_RED, fill_opacity=0.9, stroke_width=0)
    flame_inner = Polygon([-0.13, -0.05, 0], [-0.08, 0.10, 0],
                          [0.0, 0.30, 0], [0.08, 0.10, 0], [0.13, -0.05, 0],
                          fill_color=FIRE_YEL, fill_opacity=1, stroke_width=0)
    return VGroup(log1, log2, flame_outer, flame_inner).scale(scale).move_to(center)


def icon_gasoline(center=np.array([0,0,0]), scale=1.0):
    can = RoundedRectangle(width=0.55, height=0.55, corner_radius=0.06,
                           fill_color="#D03A1B", fill_opacity=1,
                           stroke_color="#7A1A10", stroke_width=1.4
                           ).move_to(DOWN*0.20)
    spout = Polygon([-0.05, 0.10, 0], [0.05, 0.10, 0],
                    [0.12, 0.30, 0], [-0.12, 0.30, 0],
                    fill_color="#D03A1B", fill_opacity=1,
                    stroke_color="#7A1A10", stroke_width=1.2)
    flame = Polygon([-0.10, 0.30, 0], [0.0, 0.65, 0], [0.10, 0.30, 0],
                    fill_color=GAS_BLUE, fill_opacity=0.95, stroke_width=0)
    flame_in = Polygon([-0.05, 0.32, 0], [0.0, 0.55, 0], [0.05, 0.32, 0],
                       fill_color=FIRE_YEL, fill_opacity=1, stroke_width=0)
    return VGroup(can, spout, flame, flame_in).scale(scale).move_to(center)


def icon_explosion(center=np.array([0,0,0]), scale=1.0):
    pts = []
    for i in range(16):
        a = i * (TAU / 16)
        r = 0.45 if i % 2 == 0 else 0.22
        pts.append([r*np.cos(a), r*np.sin(a), 0])
    star = Polygon(*pts, fill_color=EXPL_ORANGE, fill_opacity=1,
                   stroke_color="#7A2A10", stroke_width=1.4)
    core = Circle(radius=0.18, fill_color=FIRE_YEL, fill_opacity=1,
                  stroke_width=0)
    return VGroup(star, core).scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Generic person silhouette (for "you" beat 24)
# -----------------------------------------------------------------------------

def make_silhouette(center=np.array([0, -0.5, 0]), scale=1.0):
    """Black silhouette of a standing person."""
    head = Circle(radius=0.32, fill_color="#0E1014", fill_opacity=1,
                  stroke_color="#1A1F26", stroke_width=1.2).shift(UP*1.6)
    neck = Rectangle(width=0.18, height=0.20, fill_color="#0E1014",
                     fill_opacity=1, stroke_width=0).shift(UP*1.18)
    body = Polygon(
        [-0.55, 1.0, 0], [0.55, 1.0, 0],
        [0.70, 0.0, 0], [0.55, -1.0, 0],
        [-0.55, -1.0, 0], [-0.70, 0.0, 0],
        fill_color="#0E1014", fill_opacity=1,
        stroke_color="#1A1F26", stroke_width=1.2,
    )
    # arms — at sides
    arm_l = RoundedRectangle(width=0.18, height=1.0, corner_radius=0.08,
                             fill_color="#0E1014", fill_opacity=1,
                             stroke_width=0).shift(LEFT*0.72 + DOWN*0.10)
    arm_r = arm_l.copy().shift(RIGHT*1.44)
    # legs
    leg_l = RoundedRectangle(width=0.26, height=1.20, corner_radius=0.08,
                             fill_color="#0E1014", fill_opacity=1,
                             stroke_width=0).shift(LEFT*0.20 + DOWN*1.60)
    leg_r = leg_l.copy().shift(RIGHT*0.40)
    g = VGroup(leg_l, leg_r, arm_l, arm_r, body, neck, head)
    return g.scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Phone (small, callback)
# -----------------------------------------------------------------------------

def make_phone_small(center=np.array([0,0,0]), scale=1.0):
    body = RoundedRectangle(width=0.80, height=1.50, corner_radius=0.14,
                            fill_color=PHONE_DARK, fill_opacity=1,
                            stroke_color="#3A3D44", stroke_width=1.2)
    screen = RoundedRectangle(width=0.66, height=1.28, corner_radius=0.08,
                              fill_color="#2C3340", fill_opacity=1,
                              stroke_width=0)
    return VGroup(body, screen).scale(scale).move_to(center)


def make_coffee_cup(center=np.array([0,0,0]), scale=1.0):
    cup = Polygon([-0.35, 0.40, 0], [0.32, 0.40, 0],
                  [0.25, -0.40, 0], [-0.28, -0.40, 0],
                  fill_color=COFFEE_CUP, fill_opacity=1,
                  stroke_color="#5A3A20", stroke_width=1.5)
    coffee = Rectangle(width=0.56, height=0.14, fill_color=COFFEE_BR,
                       fill_opacity=1, stroke_width=0).shift(UP*0.30)
    handle = ArcBetweenPoints([0.32, 0.25, 0], [0.32, -0.25, 0], angle=-PI*0.9
                              ).set_stroke("#5A3A20", 3)
    steam = VMobject(stroke_color="#CCCCCC", stroke_width=1.8)
    pts = [[-0.05, 0.55, 0], [0.05, 0.68, 0], [-0.05, 0.80, 0]]
    steam.set_points_smoothly(pts).set_stroke(opacity=0.6)
    return VGroup(cup, coffee, handle, steam).scale(scale).move_to(center)


# -----------------------------------------------------------------------------
# Small label helper
# -----------------------------------------------------------------------------

def small_label(text, pos, color=WHITE, size=24, opacity=0.95, weight=NORMAL):
    return Text(text, font="sans", font_size=size, color=color, weight=weight
                ).move_to(pos).set_opacity(opacity)
