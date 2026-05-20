"""Helpers for the Gravitational Potential Energy (gravpe) scene.

Primitives: a book, a wall shelf, a table with floor, energy/speed bars,
dashed reference lines, height brackets, and labels. All on pure #000000,
font="sans".
"""

from manim import *
import numpy as np

VOID = "#000000"

BOOK_COVER = "#C8743A"   # warm orange-brown cover
BOOK_PAGES = "#EAE4D5"   # cream page edge
BOOK_SPINE = "#9A5526"
WOOD       = "#7A6248"   # shelf / table wood
WOOD_DARK  = "#5A4836"
WORK_COL   = "#7FB8E8"   # the "work you did" / stored-energy bar (blue)
SPEED_COL  = "#E8B45A"   # the speed / released-energy bar (amber)
GLOW_COL   = "#F2D27A"   # stored-book glow
REF_COL    = "#8C98A6"   # dashed reference / guide lines
LABEL_COL  = "#EAE4D5"
DIM_LABEL  = "#8C98A6"


def make_book(scale=1.0, color=BOOK_COVER):
    """A small closed book seen edge-on: cover + page block + spine."""
    w, h = 1.05 * scale, 0.30 * scale
    cover = RoundedRectangle(width=w, height=h, corner_radius=0.035 * scale,
                             fill_color=color, fill_opacity=1.0,
                             stroke_color=BOOK_SPINE, stroke_width=2.0)
    pages = Rectangle(width=w * 0.92, height=h * 0.62,
                      fill_color=BOOK_PAGES, fill_opacity=1.0,
                      stroke_width=0).move_to(cover.get_center())
    spine = Line(cover.get_left() + UP * h * 0.5,
                 cover.get_left() + DOWN * h * 0.5,
                 color=BOOK_SPINE, stroke_width=3.5)
    line1 = Line(pages.get_left() + RIGHT * 0.04, pages.get_right() - RIGHT * 0.04,
                 color=BOOK_SPINE, stroke_width=1.0).set_opacity(0.4)
    g = VGroup(cover, pages, spine, line1)
    return g


def make_shelf(center, width=2.4, color=WOOD):
    """A wall-mounted shelf: a horizontal plank with two small brackets."""
    center = np.array(center, dtype=float)
    plank = Rectangle(width=width, height=0.16, fill_color=color,
                      fill_opacity=1.0, stroke_color=WOOD_DARK,
                      stroke_width=1.5).move_to(center)
    b_l = Polygon(plank.get_corner(DL), plank.get_corner(DL) + DOWN * 0.30,
                  plank.get_corner(DL) + RIGHT * 0.30,
                  color=WOOD_DARK, fill_color=WOOD_DARK,
                  fill_opacity=1.0, stroke_width=0)
    b_r = Polygon(plank.get_corner(DR), plank.get_corner(DR) + DOWN * 0.30,
                  plank.get_corner(DR) + LEFT * 0.30,
                  color=WOOD_DARK, fill_color=WOOD_DARK,
                  fill_opacity=1.0, stroke_width=0)
    return VGroup(plank, b_l, b_r)


def shelf_top_y(shelf):
    """The y where a book should rest on a shelf made by make_shelf."""
    return shelf[0].get_top()[1]


def make_table(center, top_width=3.0, leg_height=1.6, color=WOOD):
    """A table: a top plank and two legs. center = center of the table top."""
    center = np.array(center, dtype=float)
    top = Rectangle(width=top_width, height=0.16, fill_color=color,
                    fill_opacity=1.0, stroke_color=WOOD_DARK,
                    stroke_width=1.5).move_to(center)
    lx = top_width * 0.5 - 0.18
    leg_l = Rectangle(width=0.16, height=leg_height, fill_color=WOOD_DARK,
                      fill_opacity=1.0, stroke_width=0)
    leg_l.next_to(top.get_corner(DL) + RIGHT * 0.10, DOWN, buff=0)
    leg_l.align_to(top, LEFT).shift(RIGHT * 0.10)
    leg_r = Rectangle(width=0.16, height=leg_height, fill_color=WOOD_DARK,
                      fill_opacity=1.0, stroke_width=0)
    leg_r.next_to(top.get_corner(DR) + LEFT * 0.10, DOWN, buff=0)
    leg_r.align_to(top, RIGHT).shift(LEFT * 0.10)
    return VGroup(top, leg_l, leg_r)


def table_top_y(table):
    return table[0].get_top()[1]


def floor_line(y=-3.3, x_half=6.6, color=WOOD_DARK):
    """A solid floor line."""
    return Line([-x_half, y, 0], [x_half, y, 0], color=color,
                stroke_width=3.0)


def dashed_ref(y, x_half=5.6, color=REF_COL, opacity=0.85, sw=2.4):
    """A horizontal dashed reference line at height y."""
    ln = DashedLine([-x_half, y, 0], [x_half, y, 0], color=color,
                    stroke_width=sw, dash_length=0.16,
                    dashed_ratio=0.55)
    ln.set_opacity(opacity)
    return ln


def energy_bar(anchor, height=0.0, max_height=2.2, width=0.34,
               color=WORK_COL, label=None):
    """A vertical filled bar growing UP from `anchor` (its bottom-center).

    Returns VGroup [frame, fill]. Set fill height via set_bar().
    """
    anchor = np.array(anchor, dtype=float)
    frame = Rectangle(width=width, height=max_height, stroke_color=color,
                      stroke_width=2.0, fill_opacity=0)
    frame.move_to(anchor + np.array([0, max_height / 2.0, 0]))
    fh = max(1e-4, height)
    fill = Rectangle(width=width, height=fh, fill_color=color,
                     fill_opacity=0.85, stroke_width=0)
    fill.move_to(anchor + np.array([0, fh / 2.0, 0]))
    return VGroup(frame, fill)


def set_bar(bar, height, anchor, max_height=2.2, width=0.34, color=WORK_COL):
    """Return a fresh fill rectangle for `bar` set to `height` (for .become)."""
    anchor = np.array(anchor, dtype=float)
    fh = max(1e-4, min(height, max_height))
    f = Rectangle(width=width, height=fh, fill_color=color,
                  fill_opacity=0.85, stroke_width=0)
    f.move_to(anchor + np.array([0, fh / 2.0, 0]))
    return f


def height_bracket(x, y_lo, y_hi, color=REF_COL, label="h", size=30):
    """A vertical double-arrow from y_lo to y_hi at x, with a label."""
    line = DoubleArrow([x, y_lo, 0], [x, y_hi, 0], color=color,
                       buff=0, stroke_width=3.0,
                       max_tip_length_to_length_ratio=0.10,
                       tip_length=0.16)
    lbl = Text(label, font="sans", font_size=size, color=color,
               slant=ITALIC)
    lbl.next_to(line, RIGHT, buff=0.12)
    return VGroup(line, lbl)


def glow(mobj, color=GLOW_COL, n=4, base=0.16, spread=0.12):
    """Soft layered glow halo behind a mobject (book)."""
    g = VGroup()
    for k in range(n):
        c = mobj.copy()
        c.set_stroke(width=0)
        c.set_fill(color, opacity=base * (1.0 - k / n))
        c.scale(1.0 + spread * (k + 1))
        g.add(c)
    return g


def label(text, pos, color=LABEL_COL, size=28, opacity=1.0):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)


def small_label(text, pos, color=DIM_LABEL, size=22, opacity=0.95):
    return Text(text, font="sans", font_size=size, color=color
                ).move_to(pos).set_opacity(opacity)
