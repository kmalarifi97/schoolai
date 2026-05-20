"""Helpers for the Heat Transfer (heattransfer) scene.

Conduction / Convection / Radiation primitives:
  - make_bowl: a soup bowl with steam wisps
  - make_spoon: a metal spoon (bowl + handle), handle returned for heat tinting
  - heat_tint: interpolate a stroke color from cool steel to hot orange
  - make_particle_chain: bonded particles for the vibration relay
  - make_pot_on_flame: a pot of water sitting on a flame
  - convection_loop: red-up-the-middle / blue-down-the-sides arrows
  - make_sun_void / glow_path: Sun + faint glow across emptiness
  - radiation_rays: wavy energy rays from a source toward a target
  - make_face / make_campfire / make_stove: warming-a-face props
  - small_label: the project's standard caption text
"""

from manim import *
import numpy as np

VOID = "#000000"

STEEL_COOL = "#9AA6B2"
STEEL_HOT  = "#F2913D"
HOT_RED    = "#E0552B"
COOL_BLUE  = "#5B8FC9"
FLAME_OUT  = "#E0552B"
FLAME_IN   = "#F2C14E"
WATER_COL  = "#3E6E8E"
LABEL_COL  = "#EAE4D5"
STEAM_COL  = "#C8D0D8"
RAY_COL    = "#F2C14E"
SUN_CORE   = "#FFF4D6"
EARTH_BLUE = "#3B6FB0"
EARTH_LAND = "#4F8A52"


def heat_tint(t, cool=STEEL_COOL, hot=STEEL_HOT):
    """t in [0,1]: 0 = cool steel, 1 = hot orange."""
    return interpolate_color(ManimColor(cool), ManimColor(hot), float(np.clip(t, 0, 1)))


def small_label(text, pos, color=LABEL_COL, size=26, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def make_bowl(pos=ORIGIN, scale=1.0):
    """A simple soup bowl: a half-ellipse body with a soup surface."""
    pos = np.array(pos, dtype=float)
    body = ArcBetweenPoints(
        np.array([-1.5, 0.0, 0]) * scale + pos,
        np.array([1.5, 0.0, 0]) * scale + pos,
        angle=-PI * 0.78,
    )
    body.set_stroke(color="#B7BCC2", width=4)
    body.set_fill(color="#23282E", opacity=1.0)
    soup = Ellipse(width=2.95 * scale, height=0.45 * scale,
                   fill_color="#B5732E", fill_opacity=1.0,
                   stroke_color="#D08A3C", stroke_width=2)
    soup.move_to(pos + np.array([0, 0.0, 0]))
    rim_l = Dot(np.array([-1.5, 0.0, 0]) * scale + pos, radius=0.05,
                color="#C7CCD2")
    rim_r = Dot(np.array([1.5, 0.0, 0]) * scale + pos, radius=0.05,
                color="#C7CCD2")
    return VGroup(body, soup, rim_l, rim_r)


def steam_wisps(top_center, n=3, height=1.6, color=STEAM_COL):
    """Wavy translucent steam curves rising from a point."""
    top = np.array(top_center, dtype=float)
    g = VGroup()
    for k in range(n):
        x0 = (k - (n - 1) / 2.0) * 0.42
        pts = []
        for s in np.linspace(0, 1, 24):
            x = x0 + 0.22 * np.sin(s * 3.4 * PI + k)
            y = s * height
            pts.append(top + np.array([x, y, 0]))
        c = VMobject().set_points_smoothly(pts)
        c.set_stroke(color=color, width=3, opacity=0.0)
        g.add(c)
    return g


def make_spoon(handle_top, bowl_center, scale=1.0):
    """A metal spoon. Returns (group, handle_segments) where handle_segments
    is a VGroup of short line pieces from soup end (idx 0) up to the top, so
    each can be tinted independently for the 'heat creeping up' effect."""
    handle_top = np.array(handle_top, dtype=float)
    bowl_center = np.array(bowl_center, dtype=float)

    # spoon bowl (the scoop)
    scoop = Ellipse(width=0.62 * scale, height=0.42 * scale,
                    fill_color=STEEL_COOL, fill_opacity=1.0,
                    stroke_color="#7E8A96", stroke_width=2)
    scoop.move_to(bowl_center)

    # handle: a series of segments from just above the scoop to handle_top
    base = bowl_center + np.array([0, 0.22 * scale, 0])
    n_seg = 10
    handle = VGroup()
    pts = [base + (handle_top - base) * (i / n_seg) for i in range(n_seg + 1)]
    for i in range(n_seg):
        seg = Line(pts[i], pts[i + 1], stroke_width=10 * scale)
        seg.set_color(STEEL_COOL)
        handle.add(seg)
    return VGroup(scoop, handle), handle


def make_particle(pos, color="#9AA6B2", r=0.16):
    return Circle(radius=r, fill_color=color, fill_opacity=1.0,
                  stroke_color=WHITE, stroke_width=1.2
                  ).move_to(np.array(pos, dtype=float))


def make_particle_chain(start, end, n=8, color="#9AA6B2", r=0.16):
    """A chain of bonded particles (springs between them) from start to end.
    Returns (group, particles, bonds)."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    centers = [start + (end - start) * (i / (n - 1)) for i in range(n)]
    particles = VGroup(*[make_particle(c, color=color, r=r) for c in centers])
    bonds = VGroup()
    for i in range(n - 1):
        b = Line(centers[i], centers[i + 1], color="#5C6670", stroke_width=3)
        bonds.add(b)
    return VGroup(bonds, particles), particles, bonds


def make_pot_on_flame(pos=ORIGIN, scale=1.0):
    """A pot of water with a flame underneath. Returns
    (group, water_rect, flame) so beats can animate the water/flame."""
    pos = np.array(pos, dtype=float)
    w, h = 3.2 * scale, 1.9 * scale

    body = RoundedRectangle(width=w, height=h, corner_radius=0.10,
                            stroke_color="#9098A0", stroke_width=4,
                            fill_color="#1C2026", fill_opacity=1.0)
    body.move_to(pos)
    water = Rectangle(width=w - 0.22, height=h - 0.55,
                      fill_color=WATER_COL, fill_opacity=1.0,
                      stroke_width=0)
    water.move_to(pos + np.array([0, -0.20 * scale, 0]))
    handle_l = ArcBetweenPoints(body.get_left() + np.array([0, 0.30, 0]),
                                body.get_left() + np.array([0, -0.30, 0]),
                                angle=PI * 0.9)
    handle_l.set_stroke(color="#9098A0", width=5)
    handle_r = ArcBetweenPoints(body.get_right() + np.array([0, 0.30, 0]),
                                body.get_right() + np.array([0, -0.30, 0]),
                                angle=-PI * 0.9)
    handle_r.set_stroke(color="#9098A0", width=5)

    flame = VGroup()
    fb = body.get_bottom()
    for k in range(7):
        fx = (k - 3) * 0.34 * scale
        tip = fb + np.array([fx, -1.05 * scale - 0.05 * abs(k - 3), 0])
        base_l = fb + np.array([fx - 0.18 * scale, -0.05, 0])
        base_r = fb + np.array([fx + 0.18 * scale, -0.05, 0])
        f = VMobject().set_points_smoothly([base_l, tip, base_r])
        f.set_fill(color=FLAME_OUT, opacity=0.85)
        f.set_stroke(width=0)
        fi = VMobject().set_points_smoothly([
            fb + np.array([fx - 0.09 * scale, -0.05, 0]),
            fb + np.array([fx, -0.62 * scale, 0]),
            fb + np.array([fx + 0.09 * scale, -0.05, 0]),
        ])
        fi.set_fill(color=FLAME_IN, opacity=0.95)
        fi.set_stroke(width=0)
        flame.add(f, fi)

    return VGroup(handle_l, handle_r, body, water), water, flame


def convection_loop(center, w=2.4, h=1.5, color_up=HOT_RED,
                    color_down=COOL_BLUE):
    """A turning loop: red arrows rising in the middle, blue arrows
    sinking at the sides — the classic convection cell."""
    c = np.array(center, dtype=float)
    g = VGroup()
    # rising center (red, upward)
    for k in range(3):
        y0 = -h / 2 + k * (h / 3)
        a = Arrow(c + np.array([0, y0, 0]),
                  c + np.array([0, y0 + h / 3 + 0.05, 0]),
                  color=color_up, buff=0, stroke_width=6,
                  max_tip_length_to_length_ratio=0.35)
        g.add(a)
    # top spread outward
    for sgn in (-1, 1):
        a = CurvedArrow(c + np.array([0.05 * sgn, h / 2, 0]),
                        c + np.array([w / 2 * sgn, h / 2 - 0.05, 0]),
                        color=color_up, angle=-0.5 * sgn, stroke_width=5,
                        tip_length=0.2)
        g.add(a)
    # sinking sides (blue, downward)
    for sgn in (-1, 1):
        for k in range(3):
            y0 = h / 2 - k * (h / 3)
            a = Arrow(c + np.array([w / 2 * sgn, y0, 0]),
                      c + np.array([w / 2 * sgn, y0 - h / 3 - 0.05, 0]),
                      color=color_down, buff=0, stroke_width=6,
                      max_tip_length_to_length_ratio=0.35)
            g.add(a)
    # bottom return inward
    for sgn in (-1, 1):
        a = CurvedArrow(c + np.array([w / 2 * sgn, -h / 2, 0]),
                        c + np.array([0.05 * -sgn, -h / 2 + 0.05, 0]),
                        color=color_down, angle=-0.5 * sgn, stroke_width=5,
                        tip_length=0.2)
        g.add(a)
    return g


def make_sun_void(pos, scale=1.0):
    """A glowing Sun (layered)."""
    pos = np.array(pos, dtype=float)
    g = VGroup()
    for r, op in [(1.05, 0.05), (0.80, 0.10), (0.55, 0.22), (0.36, 0.55)]:
        g.add(Circle(radius=r * scale, color=SUN_CORE, fill_color=SUN_CORE,
                      fill_opacity=op, stroke_width=0))
    g.add(Circle(radius=0.22 * scale, color=WHITE, fill_color=WHITE,
                 fill_opacity=1.0, stroke_width=0))
    return g.move_to(pos)


def make_earth(pos, scale=1.0):
    """A small blue Earth."""
    pos = np.array(pos, dtype=float)
    body = Circle(radius=0.42 * scale, fill_color=EARTH_BLUE,
                  fill_opacity=1.0, stroke_color="#9FC0E8",
                  stroke_width=1.4)
    land1 = Ellipse(width=0.30 * scale, height=0.20 * scale,
                    fill_color=EARTH_LAND, fill_opacity=0.9,
                    stroke_width=0).shift((LEFT * 0.10 + UP * 0.08) * scale)
    land2 = Ellipse(width=0.22 * scale, height=0.16 * scale,
                    fill_color=EARTH_LAND, fill_opacity=0.9,
                    stroke_width=0).shift((RIGHT * 0.12 + DOWN * 0.10) * scale)
    hl = Ellipse(width=0.18 * scale, height=0.12 * scale, fill_color=WHITE,
                 fill_opacity=0.15, stroke_width=0
                 ).shift((LEFT * 0.14 + UP * 0.13) * scale)
    return VGroup(body, land1, land2, hl).move_to(pos)


def glow_path(src, dst, color=RAY_COL):
    """A faint straight glow connecting source to destination."""
    src = np.array(src, dtype=float)
    dst = np.array(dst, dtype=float)
    line = Line(src, dst, color=color, stroke_width=10).set_opacity(0.10)
    return line


def radiation_rays(src, dst, n=4, color=RAY_COL, spread=0.55,
                   amp=0.16, cycles=5.0):
    """Wavy sinusoidal rays travelling from src toward dst."""
    src = np.array(src, dtype=float)
    dst = np.array(dst, dtype=float)
    axis = dst - src
    L = np.linalg.norm(axis)
    u = axis / L
    perp = np.array([-u[1], u[0], 0])
    g = VGroup()
    for k in range(n):
        off = (k - (n - 1) / 2.0) * spread
        pts = []
        for s in np.linspace(0.0, 1.0, 60):
            base = src + u * (L * s) + perp * off
            wob = perp * amp * np.sin(s * cycles * TAU)
            pts.append(base + wob)
        c = VMobject().set_points_smoothly(pts)
        c.set_stroke(color=color, width=3.2, opacity=0.9)
        g.add(c)
    return g


def make_flame_tongue(base, height=1.0, width=0.5, out=FLAME_OUT,
                      inn=FLAME_IN):
    base = np.array(base, dtype=float)
    f = VMobject().set_points_smoothly([
        base + np.array([-width / 2, 0, 0]),
        base + np.array([0, height, 0]),
        base + np.array([width / 2, 0, 0]),
    ])
    f.set_fill(color=out, opacity=0.9)
    f.set_stroke(width=0)
    fi = VMobject().set_points_smoothly([
        base + np.array([-width / 4, 0, 0]),
        base + np.array([0, height * 0.6, 0]),
        base + np.array([width / 4, 0, 0]),
    ])
    fi.set_fill(color=inn, opacity=0.95)
    fi.set_stroke(width=0)
    return VGroup(f, fi)


def make_campfire(pos, scale=1.0):
    """Logs + flames."""
    pos = np.array(pos, dtype=float)
    logs = VGroup()
    for ang in (-0.4, 0.4):
        log = RoundedRectangle(width=1.3 * scale, height=0.24 * scale,
                               corner_radius=0.10,
                               fill_color="#6B4A2E", fill_opacity=1.0,
                               stroke_color="#4A3320", stroke_width=2)
        log.rotate(ang).move_to(pos + np.array([0, -0.05, 0]))
        logs.add(log)
    flames = VGroup()
    for k, (dx, hgt, wid) in enumerate([(-0.32, 0.85, 0.5),
                                        (0.0, 1.25, 0.62),
                                        (0.34, 0.9, 0.5)]):
        flames.add(make_flame_tongue(pos + np.array([dx, 0.06, 0]),
                                     height=hgt * scale, width=wid * scale))
    return VGroup(logs, flames)


def make_face(pos, scale=1.0, facing=LEFT):
    """A simple side-profile head facing `facing` (a direction vector)."""
    pos = np.array(pos, dtype=float)
    facing = np.array(facing, dtype=float)
    head = Circle(radius=0.55 * scale, fill_color="#D9B48F",
                  fill_opacity=1.0, stroke_color="#A07A55",
                  stroke_width=2).move_to(pos)
    # nose: a small triangle poking in the facing direction
    tip = pos + facing * 0.62 * scale
    n1 = pos + facing * 0.30 * scale + np.array([0, 0.10 * scale, 0])
    n2 = pos + facing * 0.30 * scale + np.array([0, -0.14 * scale, 0])
    nose = Polygon(n1, tip, n2, fill_color="#D9B48F", fill_opacity=1.0,
                   stroke_color="#A07A55", stroke_width=2)
    eye = Dot(pos + facing * 0.22 * scale + np.array([0, 0.14 * scale, 0]),
              radius=0.045 * scale, color="#2A2A2A")
    return VGroup(head, nose, eye)


def make_stove(pos, scale=1.0):
    """A glowing stove element: a flat coil disk."""
    pos = np.array(pos, dtype=float)
    plate = Ellipse(width=2.0 * scale, height=0.7 * scale,
                    fill_color="#1A1A1E", fill_opacity=1.0,
                    stroke_color="#3A3A40", stroke_width=2).move_to(pos)
    coil = VGroup()
    for r in (0.72, 0.50, 0.28):
        coil.add(Ellipse(width=2 * r * scale, height=0.66 * r * scale,
                          stroke_color="#E0552B", stroke_width=5,
                          fill_opacity=0).move_to(pos))
    return VGroup(plate, coil)
