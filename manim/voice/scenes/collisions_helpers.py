"""Helpers for the Collisions (elastic & inelastic) scene.

Primitives the 12 beats need:
  - make_cart            : a rolling cart (two wheels + body)
  - steel_ball           : polished metal sphere with highlight
  - clay_blob            : matte lumpy clay blob (organic outline)
  - fused_blob           : a single bigger lump (two clays merged)
  - momentum_bar         : fixed-length labelled bar (does NOT change)
  - energy_bar           : a variable-fill "motion energy" bar
  - split_bar            : conserved total split into useful / lost
  - shimmer              : heat/sound/bending shimmer particles
  - checklist            : a small two-row tick/cross checklist
  - slider               : a track with a knob between two labelled ends
  - small_label / title  : sans-font text helpers

Pure #000000 void. font="sans" for all text.
"""

from manim import *
import numpy as np

VOID = "#000000"

STEEL_LIGHT = "#D8DEE6"
STEEL_MID   = "#8C95A1"
STEEL_DARK  = "#4A5059"
CLAY_COL    = "#B07A52"
CLAY_DARK   = "#6E4A30"
BAR_FRAME   = "#5A6470"
MOM_COL     = "#7FB8E8"
KE_COL      = "#E8C24A"
LOST_COL    = "#C8654A"
INK         = "#EAE4D5"
DIM         = "#8C98A6"
GOOD        = "#7FC27F"
BAD         = "#C8654A"


def title(text, pos, size=34, color=INK, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def small_label(text, pos, color=DIM, size=24, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def steel_ball(pos, r=0.42):
    """Polished steel sphere: graded body + bright highlight."""
    body = Circle(radius=r, fill_color=STEEL_MID, fill_opacity=1,
                  stroke_color=STEEL_DARK, stroke_width=2)
    inner = Circle(radius=r * 0.72, fill_color=STEEL_LIGHT, fill_opacity=0.45,
                   stroke_width=0).shift((LEFT + UP) * r * 0.18)
    hl = Ellipse(width=r * 0.55, height=r * 0.34, fill_color=WHITE,
                 fill_opacity=0.85, stroke_width=0
                 ).shift((LEFT + UP) * r * 0.42)
    return VGroup(body, inner, hl).move_to(pos)


def make_cart(pos, color=STEEL_MID, w=1.2, h=0.55):
    """A simple cart: rectangular body on two round wheels."""
    body = RoundedRectangle(width=w, height=h, corner_radius=0.10,
                            fill_color=color, fill_opacity=1,
                            stroke_color=STEEL_DARK, stroke_width=2)
    wr = h * 0.34
    wl = Circle(radius=wr, fill_color=STEEL_DARK, fill_opacity=1,
                stroke_color="#2A2E33", stroke_width=2)
    wl.move_to(body.get_corner(DL) + np.array([w * 0.22, -wr * 0.55, 0]))
    wrt = wl.copy().move_to(
        body.get_corner(DR) + np.array([-w * 0.22, -wr * 0.55, 0]))
    hub1 = Dot(wl.get_center(), radius=wr * 0.30, color="#9AA2AD")
    hub2 = Dot(wrt.get_center(), radius=wr * 0.30, color="#9AA2AD")
    return VGroup(body, wl, wrt, hub1, hub2).move_to(pos)


def _blob_points(r, seed, lumpiness=0.22, n=22):
    rng = np.random.default_rng(seed)
    pts = []
    for k in range(n):
        ang = TAU * k / n
        rad = r * (1.0 + lumpiness * (rng.random() - 0.5) * 2)
        pts.append([rad * np.cos(ang), rad * np.sin(ang), 0])
    return pts


def clay_blob(pos, r=0.45, seed=3, color=CLAY_COL):
    """A matte, slightly lumpy clay blob (closed smooth-ish polygon)."""
    pts = _blob_points(r, seed)
    blob = Polygon(*pts, fill_color=color, fill_opacity=1,
                   stroke_color=CLAY_DARK, stroke_width=2)
    blob.set_sheen(0.0)
    blob = blob.round_corners(radius=r * 0.30)
    spot = Circle(radius=r * 0.16, fill_color=CLAY_DARK, fill_opacity=0.30,
                  stroke_width=0).shift((RIGHT * 0.12 + DOWN * 0.10) * r)
    return VGroup(blob, spot).move_to(pos)


def fused_blob(pos, r=0.62, seed=9, color=CLAY_COL):
    """One bigger lump — the two clays merged into a single body."""
    pts = _blob_points(r, seed, lumpiness=0.28, n=26)
    blob = Polygon(*pts, fill_color=color, fill_opacity=1,
                   stroke_color=CLAY_DARK, stroke_width=2
                   ).round_corners(radius=r * 0.26)
    seam = Line([0, -r * 0.7, 0], [0, r * 0.7, 0],
                color=CLAY_DARK, stroke_width=2).set_opacity(0.45)
    s1 = Circle(radius=r * 0.14, fill_color=CLAY_DARK, fill_opacity=0.28,
                stroke_width=0).shift((LEFT * 0.30 + UP * 0.18) * r)
    s2 = Circle(radius=r * 0.12, fill_color=CLAY_DARK, fill_opacity=0.28,
                stroke_width=0).shift((RIGHT * 0.34 + DOWN * 0.20) * r)
    return VGroup(blob, seam, s1, s2).move_to(pos)


def momentum_bar(pos, width=4.2, height=0.42, frac=0.62,
                 color=MOM_COL, label="total momentum"):
    """A FIXED-length filled bar inside a frame. Use for momentum:
    the fill never changes through the collision."""
    frame = Rectangle(width=width, height=height, stroke_color=BAR_FRAME,
                      stroke_width=2, fill_opacity=0)
    fill = Rectangle(width=width * frac, height=height,
                     fill_color=color, fill_opacity=0.9, stroke_width=0)
    fill.move_to(frame.get_left() + RIGHT * (width * frac / 2))
    lbl = Text(label, font="sans", font_size=22, color=DIM
               ).next_to(frame, UP, buff=0.16)
    g = VGroup(frame, fill, lbl).move_to(pos)
    g.fill_rect = fill
    return g


def energy_bar(pos, width=1.0, max_h=2.6, frac=1.0,
               color=KE_COL, label="motion energy"):
    """A vertical 'motion energy' bar that grows from the bottom.
    Returns a VGroup; .set_fraction(f) rebuilds the fill height."""
    frame = Rectangle(width=width, height=max_h, stroke_color=BAR_FRAME,
                      stroke_width=2, fill_opacity=0)
    frac = float(np.clip(frac, 0.001, 1.0))
    fill = Rectangle(width=width, height=max_h * frac,
                     fill_color=color, fill_opacity=0.9, stroke_width=0)
    fill.align_to(frame, DOWN)
    lbl = Text(label, font="sans", font_size=20, color=DIM
               ).next_to(frame, DOWN, buff=0.18)
    g = VGroup(frame, fill, lbl).move_to(pos)
    return g


def make_energy_fill(bar_group, frac, color=KE_COL):
    """Build a replacement fill rect for an energy_bar at a new fraction,
    aligned to that bar's frame bottom. Returns a Rectangle mobject."""
    frame = bar_group[0]
    w = frame.width
    max_h = frame.height
    frac = float(np.clip(frac, 0.001, 1.0))
    fill = Rectangle(width=w, height=max_h * frac,
                     fill_color=color, fill_opacity=0.9, stroke_width=0)
    fill.move_to(frame.get_bottom() + UP * (max_h * frac / 2))
    return fill


def split_bar(pos, width=5.0, height=0.5, useful_frac=0.5):
    """One conserved total bar split into 'useful motion' (left, gold)
    and 'heat + sound + bending' (right, ember). Total length fixed."""
    uf = float(np.clip(useful_frac, 0.0, 1.0))
    frame = Rectangle(width=width, height=height, stroke_color=BAR_FRAME,
                      stroke_width=2, fill_opacity=0)
    left = Rectangle(width=max(width * uf, 0.001), height=height,
                     fill_color=KE_COL, fill_opacity=0.9, stroke_width=0)
    left.align_to(frame, LEFT)
    right = Rectangle(width=max(width * (1 - uf), 0.001), height=height,
                      fill_color=LOST_COL, fill_opacity=0.85, stroke_width=0)
    right.align_to(frame, RIGHT)
    l1 = Text("useful motion", font="sans", font_size=18, color=KE_COL
              ).next_to(frame, UP, buff=0.14).align_to(frame, LEFT)
    l2 = Text("heat + sound + bending", font="sans", font_size=18,
              color=LOST_COL).next_to(frame, DOWN, buff=0.14
                                      ).align_to(frame, RIGHT)
    g = VGroup(frame, left, right, l1, l2).move_to(pos)
    return g


def make_split_fills(bar_group, useful_frac):
    """Replacement (left, right) fill rects for a split_bar."""
    frame = bar_group[0]
    w = frame.width
    h = frame.height
    uf = float(np.clip(useful_frac, 0.0, 1.0))
    left = Rectangle(width=max(w * uf, 0.001), height=h,
                     fill_color=KE_COL, fill_opacity=0.9, stroke_width=0)
    left.move_to(frame.get_left() + RIGHT * (w * uf / 2))
    right = Rectangle(width=max(w * (1 - uf), 0.001), height=h,
                      fill_color=LOST_COL, fill_opacity=0.85, stroke_width=0)
    right.move_to(frame.get_right() + LEFT * (w * (1 - uf) / 2))
    return left, right


def shimmer(center, spread=1.4, n=14, seed=5, color=LOST_COL):
    """Heat/sound/bending shimmer: small wavy strokes radiating outward."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    for k in range(n):
        ang = TAU * k / n + rng.random() * 0.3
        base = np.array([np.cos(ang), np.sin(ang), 0])
        r0 = spread * (0.35 + 0.25 * rng.random())
        r1 = r0 + spread * (0.35 + 0.4 * rng.random())
        perp = np.array([-np.sin(ang), np.cos(ang), 0])
        mid = base * (r0 + r1) / 2 + perp * 0.12 * (rng.random() - 0.5) * 2
        wave = VMobject()
        wave.set_points_smoothly([
            center + base * r0,
            center + mid,
            center + base * r1,
        ])
        wave.set_stroke(color=color, width=2.4,
                        opacity=0.75 - 0.3 * rng.random())
        g.add(wave)
    return g


def checklist(pos, rows):
    """rows = [(label, ok_bool, note), ...]. Tick (green) or cross (ember)."""
    g = VGroup()
    for idx, (label, ok, note) in enumerate(rows):
        y = -idx * 0.95
        mark = (Text("✓", font="sans", font_size=34, color=GOOD)
                if ok else Text("✗", font="sans", font_size=34, color=BAD))
        mark.move_to([-2.6, y, 0])
        lab = Text(label, font="sans", font_size=26, color=INK
                   ).next_to(mark, RIGHT, buff=0.30)
        nt = Text(note, font="sans", font_size=20, color=DIM
                  ).next_to(lab, RIGHT, buff=0.40)
        g.add(VGroup(mark, lab, nt))
    return g.move_to(pos)


def slider(pos, width=6.0, knob_frac=0.5,
           left_label="perfectly\nelastic",
           right_label="perfectly\ninelastic"):
    """A horizontal track with a knob; labels at each end."""
    track = Line([-width / 2, 0, 0], [width / 2, 0, 0],
                 color=BAR_FRAME, stroke_width=4)
    tickL = Line([-width / 2, -0.12, 0], [-width / 2, 0.12, 0],
                 color=BAR_FRAME, stroke_width=4)
    tickR = Line([width / 2, -0.12, 0], [width / 2, 0.12, 0],
                 color=BAR_FRAME, stroke_width=4)
    kf = float(np.clip(knob_frac, 0.0, 1.0))
    kx = -width / 2 + width * kf
    knob = Dot([kx, 0, 0], radius=0.16, color=KE_COL)
    lL = Text(left_label, font="sans", font_size=20, color=GOOD,
              line_spacing=0.7).next_to(tickL, DOWN, buff=0.22)
    lR = Text(right_label, font="sans", font_size=20, color=LOST_COL,
              line_spacing=0.7).next_to(tickR, DOWN, buff=0.22)
    g = VGroup(track, tickL, tickR, lL, lR, knob).move_to(pos)
    g.knob = knob
    g.track = track
    return g


def qmark(pos, size=72, color=INK):
    return Text("?", font="sans", font_size=size, color=color).move_to(pos)


def speed_arrow(start, vec, color=MOM_COL, width=5):
    s = np.array(start, dtype=float)
    e = s + np.array(vec, dtype=float)
    return Arrow(s, e, color=color, stroke_width=width, buff=0,
                 max_tip_length_to_length_ratio=0.32)
