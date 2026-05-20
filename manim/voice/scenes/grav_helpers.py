"""
Shared helpers for the voiced gravity series.
- make_rock: irregular polygon rock (same as v2)
- make_fabric_3d: upgraded spacetime grid with perspective, depth, contour rings
- make_sun: layered glow
"""

from manim import *
import numpy as np


VOID = "#000000"


def make_rock(seed, scale=1.0, base="#6E6E6E", hi="#9A9A9A", lumpiness=1.0):
    rng = np.random.default_rng(seed)
    n = 16
    angles = np.linspace(0, TAU, n, endpoint=False)
    base_radii = rng.uniform(0.55, 1.0, n)
    if lumpiness != 1.0:
        m = base_radii.mean()
        base_radii = m + (base_radii - m) * lumpiness
    radii = np.array([
        0.25 * base_radii[(i - 1) % n] + 0.5 * base_radii[i] + 0.25 * base_radii[(i + 1) % n]
        for i in range(n)
    ])
    body_pts = [[radii[i]*np.cos(angles[i]), radii[i]*np.sin(angles[i]), 0]
                for i in range(n)]
    body = Polygon(*body_pts, fill_color=base, fill_opacity=1,
                   stroke_color=base, stroke_width=1.2, stroke_opacity=0.5)
    hl_radii = radii * rng.uniform(0.30, 0.55, n)
    hl_pts = [[hl_radii[i]*np.cos(angles[i]) - 0.08,
               hl_radii[i]*np.sin(angles[i]) + 0.12, 0] for i in range(n)]
    highlight = Polygon(*hl_pts, fill_color=hi, fill_opacity=0.55, stroke_width=0)
    return VGroup(body, highlight).scale(scale)


def make_sun():
    g = VGroup()
    for r, op in [(0.85, 0.04), (0.65, 0.08), (0.45, 0.18), (0.30, 0.50)]:
        g.add(Circle(radius=r, color="#FFF4D6", fill_color="#FFF4D6",
                     fill_opacity=op, stroke_width=0))
    g.add(Circle(radius=0.16, color=WHITE, fill_color=WHITE,
                 fill_opacity=1.0, stroke_width=0))
    return g


def make_fabric_3d(
    dip_amount=1.0,
    top_y=1.50, bottom_y=-2.20,
    top_w=3.0, bottom_w=11.0,
    n_x=12, n_y=8,
    dip_center=np.array([0, -0.35, 0]),
    dip_depth=1.50, dip_width=1.55,
    color="#9AA8C0",
    n_contours=4,
    line_width=1.4,
):
    """
    3D-looking spacetime fabric:
    - Strong trapezoidal perspective
    - Deep visible Gaussian dip
    - Latitude lines fade toward the back
    - Concentric foreshortened contour rings around the dip
    """

    def dip(x, y):
        dx, dy = x - dip_center[0], y - dip_center[1]
        return -dip_amount * dip_depth * np.exp(-(dx*dx + dy*dy) / (dip_width**2))

    grid = VGroup()
    n_pts = 50

    # Latitude lines
    for i in range(n_y + 1):
        t = i / n_y
        y0 = top_y * (1 - t) + bottom_y * t
        w0 = top_w * (1 - t) + bottom_w * t
        opacity = 0.30 + 0.55 * t
        pts = []
        for j in range(n_pts):
            s = j / (n_pts - 1)
            x = -w0/2 + w0 * s
            y = y0 + dip(x, y0)
            pts.append(np.array([x, y, 0]))
        line = VMobject(stroke_color=color, stroke_width=line_width)
        line.set_points_smoothly(pts); line.set_stroke(opacity=opacity)
        grid.add(line)

    # Longitude lines
    for i in range(n_x + 1):
        t = i / n_x
        edge = abs(t - 0.5) * 2
        opacity = 0.75 - 0.30 * edge
        x_top = -top_w/2 + top_w * t
        x_bot = -bottom_w/2 + bottom_w * t
        pts = []
        for j in range(n_pts):
            s = j / (n_pts - 1)
            x0 = x_top * (1 - s) + x_bot * s
            y0 = top_y * (1 - s) + bottom_y * s
            pts.append(np.array([x0, y0 + dip(x0, y0), 0]))
        line = VMobject(stroke_color=color, stroke_width=line_width)
        line.set_points_smoothly(pts); line.set_stroke(opacity=opacity)
        grid.add(line)

    # Concentric contour rings — gives clear 3D bowl shape
    if dip_amount > 0.01:
        for k in range(1, n_contours + 1):
            depth_frac = k / (n_contours + 1)
            r = dip_width * np.sqrt(-np.log(depth_frac))
            ring_pts = []
            for theta in np.linspace(0, TAU, 60, endpoint=True):
                x = dip_center[0] + r * np.cos(theta)
                yb = dip_center[1] + r * np.sin(theta) * 0.32
                y = yb + dip(x, yb)
                ring_pts.append(np.array([x, y, 0]))
            ring = VMobject(stroke_color=color, stroke_width=1.2)
            ring.set_points_smoothly(ring_pts)
            ring.set_stroke(opacity=0.55 - 0.10 * (k - 1))
            grid.add(ring)

    return grid


def bowling_ball(pos):
    body = Circle(radius=0.40, fill_color="#1A1A1A", fill_opacity=1,
                  stroke_color="#5A5A5A", stroke_width=1.6)
    hl = (Ellipse(width=0.22, height=0.12, fill_color="#9A9A9A",
                  fill_opacity=0.55, stroke_width=0)
          .shift(LEFT * 0.13 + UP * 0.14))
    return VGroup(body, hl).move_to(pos)


def make_earth(pos):
    body = Circle(radius=0.38, fill_color="#2A6BB5", fill_opacity=1,
                  stroke_color="#1A4885", stroke_width=1.6)
    c1 = Circle(radius=0.11, fill_color="#3A8B30", fill_opacity=1,
                stroke_width=0).shift(LEFT * 0.10 + UP * 0.05)
    c2 = Circle(radius=0.08, fill_color="#3A8B30", fill_opacity=1,
                stroke_width=0).shift(RIGHT * 0.12 + DOWN * 0.10)
    c3 = Circle(radius=0.06, fill_color="#3A8B30", fill_opacity=1,
                stroke_width=0).shift(RIGHT * 0.05 + UP * 0.18)
    hl = (Ellipse(width=0.20, height=0.11, fill_color=WHITE,
                  fill_opacity=0.30, stroke_width=0)
          .shift(LEFT * 0.13 + UP * 0.14))
    return VGroup(body, c1, c2, c3, hl).move_to(pos)
