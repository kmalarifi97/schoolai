"""
Helpers for the gravity-homework scene — a meta-explainer about using the
interactive sim. The visual world is a 'homework interface': canvas above
holding two rocks, controls below (sliders, play, timer), instruction text
above the canvas, reflection text boxes that slide in/out from below.

Continuity with the gravity scene: the two rocks reuse seed=7 (big) and
seed=13 (small) from grav_helpers so they read as the same rocks the user
just saw pulling each other across empty space.
"""

from manim import *
import numpy as np


VOID         = "#000000"
CANVAS_EDGE  = "#3A3D44"
CANVAS_INNER = "#07090C"
PANEL_LINE   = "#2A2E36"
TRACK_BG     = "#1C2028"
TRACK_FG     = "#7CC6FF"
HANDLE       = "#EAE4D5"
BUTTON_DIM   = "#2A2E36"
BUTTON_LIT   = "#7CC6FF"
BUTTON_ICON  = "#0B0D11"
TEXT_DIM     = "#5A5C62"
TEXT_MID     = "#9CA0A8"
TEXT_BRIGHT  = "#EAE4D5"
TEXT_PROMPT  = "#C9CDD6"
GLOW         = "#FFE08A"
ACCENT_RED   = "#D03A1B"
ACCENT_GREEN = "#5AAA6C"
ACCENT_COOL  = "#7CC6FF"


# Canonical layout — share across all 25 beats so the interface
# is in the same place every time.
CANVAS_CENTER = np.array([0.0, 1.20, 0.0])
CANVAS_W      = 11.0
CANVAS_H      = 3.80

# Rock home positions inside the canvas — slight downshift from
# the gravity-scene originals to sit inside the frame.
ROCK_BIG_HOME   = np.array([-2.00,  1.40, 0.0])
ROCK_SMALL_HOME = np.array([ 1.90,  0.55, 0.0])

# Controls panel positions
PANEL_Y_TOP    = -0.90
PANEL_Y_BOTTOM = -3.60
SLIDER_X       = -2.40
SLIDER_W       =  3.20
SLIDER_Y_A     = -1.55
SLIDER_Y_B     = -2.30
SLIDER_Y_D     = -3.05

PLAY_POS       = np.array([ 3.10, -2.30, 0.0])
TIMER_POS      = np.array([ 5.10, -2.30, 0.0])
INSTRUCTION_Y  =  3.50
ATTEMPT_POS    = np.array([ 5.60,  3.40, 0.0])


# ---------------------------------------------------------------------------
# Canvas (the frame holding the rocks)
# ---------------------------------------------------------------------------

def make_canvas(center=CANVAS_CENTER, width=CANVAS_W, height=CANVAS_H,
                edge=CANVAS_EDGE, inner=None):
    """Rectangular canvas — outline only by default."""
    fill_color = inner if inner is not None else CANVAS_INNER
    fill_op    = 0.0 if inner is None else 1.0
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.12,
        fill_color=fill_color, fill_opacity=fill_op,
        stroke_color=edge, stroke_width=1.8,
    ).move_to(center)
    return rect


# ---------------------------------------------------------------------------
# Slider
# ---------------------------------------------------------------------------

def make_slider(label_text, value=0.5, y=0.0, x=SLIDER_X, width=SLIDER_W,
                fill_color=TRACK_FG, label_color=TEXT_MID,
                value_label=None, value_color=TEXT_BRIGHT):
    """
    Horizontal slider with label on the left and optional value on the right.
    value ∈ [0, 1].
    Returns VGroup(label, track, fill, handle, [value_text]).
    """
    label = Text(label_text, font="sans", font_size=22, color=label_color
                 ).move_to([x - width/2 - 1.30, y, 0])
    track = RoundedRectangle(width=width, height=0.10, corner_radius=0.05,
                             fill_color=TRACK_BG, fill_opacity=1,
                             stroke_color="#3A3D44", stroke_width=1.0
                             ).move_to([x, y, 0])
    fill_w = max(0.04, width * value)
    fill = RoundedRectangle(width=fill_w, height=0.10, corner_radius=0.05,
                            fill_color=fill_color, fill_opacity=0.85,
                            stroke_width=0)
    fill.move_to([x - width/2 + fill_w/2, y, 0])
    hx = x - width/2 + width * value
    handle = Circle(radius=0.16, fill_color=HANDLE, fill_opacity=1,
                    stroke_color="#1A1F26", stroke_width=1.6
                    ).move_to([hx, y, 0])
    g = VGroup(label, track, fill, handle)
    if value_label is not None:
        val = Text(value_label, font="sans", font_size=22, color=value_color
                   ).move_to([x + width/2 + 0.85, y, 0])
        g.add(val)
    return g


# ---------------------------------------------------------------------------
# Play button
# ---------------------------------------------------------------------------

def make_play_button(center=PLAY_POS, radius=0.45, lit=False):
    bg_color = BUTTON_LIT if lit else BUTTON_DIM
    edge     = TEXT_BRIGHT if lit else TEXT_DIM
    icon_col = BUTTON_ICON if lit else TEXT_MID
    body = Circle(radius=radius, fill_color=bg_color, fill_opacity=1,
                  stroke_color=edge, stroke_width=1.8).move_to(center)
    # play triangle
    tri = Polygon(
        [-0.14, -0.20, 0], [-0.14, 0.20, 0], [0.18, 0.0, 0],
        fill_color=icon_col, fill_opacity=1, stroke_width=0,
    ).move_to(center + RIGHT * 0.03)
    return VGroup(body, tri)


# ---------------------------------------------------------------------------
# Timer display
# ---------------------------------------------------------------------------

def make_timer(center=TIMER_POS, text="0.0 s", color=TEXT_BRIGHT, size=28):
    pill = RoundedRectangle(width=1.30, height=0.55, corner_radius=0.10,
                            fill_color="#15181E", fill_opacity=1,
                            stroke_color=PANEL_LINE, stroke_width=1.2
                            ).move_to(center)
    txt = Text(text, font="sans", font_size=size, color=color).move_to(center)
    return VGroup(pill, txt)


def update_timer(timer_group, new_text, color=TEXT_BRIGHT, size=28):
    """Return a fresh VGroup matching the timer but with new text."""
    pill = timer_group[0].copy()
    txt = Text(new_text, font="sans", font_size=size, color=color
               ).move_to(pill.get_center())
    return VGroup(pill, txt)


# ---------------------------------------------------------------------------
# Text box (used for prediction / reflection panels)
# ---------------------------------------------------------------------------

def make_text_box(center, width=8.5, height=2.0, label=None, body=None,
                  body_size=28, label_size=22, label_color=TEXT_DIM,
                  body_color=TEXT_PROMPT, stroke=PANEL_LINE, fill="#0D0F13"):
    rect = RoundedRectangle(width=width, height=height, corner_radius=0.18,
                            fill_color=fill, fill_opacity=1,
                            stroke_color=stroke, stroke_width=1.4
                            ).move_to(center)
    parts = [rect]
    if label is not None:
        lab = Text(label, font="sans", font_size=label_size, color=label_color
                   ).move_to(rect.get_top() + DOWN * 0.32)
        parts.append(lab)
    if body is not None:
        bod = Text(body, font="sans", font_size=body_size, color=body_color)
        bod.scale_to_fit_width(width - 0.6)
        bod.move_to(rect.get_center() + DOWN * 0.05)
        parts.append(bod)
    return VGroup(*parts)


# ---------------------------------------------------------------------------
# Attempt dots
# ---------------------------------------------------------------------------

def make_attempt_dots(filled=0, center=ATTEMPT_POS, color=TEXT_BRIGHT,
                      dim=TEXT_DIM, spacing=0.42, radius=0.13):
    g = VGroup()
    for i in range(3):
        x = center[0] - spacing + i * spacing
        if i < filled:
            c = Circle(radius=radius, fill_color=color, fill_opacity=1,
                       stroke_color=color, stroke_width=1.4)
        else:
            c = Circle(radius=radius, fill_color="#000000", fill_opacity=0,
                       stroke_color=dim, stroke_width=1.4)
        c.move_to([x, center[1], 0])
        g.add(c)
    label = Text("Attempts", font="sans", font_size=18, color=TEXT_DIM
                 ).move_to([center[0], center[1] - 0.40, 0])
    g.add(label)
    return g


# ---------------------------------------------------------------------------
# Cursor (small arrow pointer)
# ---------------------------------------------------------------------------

def make_cursor(pos):
    tri = Polygon(
        [0, 0, 0], [0, -0.34, 0], [0.10, -0.24, 0],
        [0.22, -0.34, 0], [0.28, -0.30, 0], [0.18, -0.20, 0],
        [0.26, -0.12, 0],
        fill_color=TEXT_BRIGHT, fill_opacity=1,
        stroke_color="#1A1F26", stroke_width=1.2,
    )
    tri.move_to(pos)
    return tri


# ---------------------------------------------------------------------------
# Predicted / Actual / Gap row
# ---------------------------------------------------------------------------

def pred_actual_row(predicted, actual, pos, width=8.0, size=26,
                    pred_color=TEXT_MID, act_color=TEXT_BRIGHT,
                    gap_color=GLOW, gap_label=True):
    gap = abs(actual - predicted)
    pos = np.array(pos)
    cell_w = width / 3.0
    p_text = Text(f"pred {predicted}", font="sans", font_size=size,
                  color=pred_color).move_to(pos + LEFT * cell_w)
    a_text = Text(f"actual {actual}", font="sans", font_size=size,
                  color=act_color).move_to(pos)
    if gap_label:
        g_text = Text(f"gap {gap}", font="sans", font_size=size,
                      color=gap_color).move_to(pos + RIGHT * cell_w)
    else:
        g_text = Text(f"{gap}", font="sans", font_size=size,
                      color=gap_color).move_to(pos + RIGHT * cell_w)
    return VGroup(p_text, a_text, g_text)


# ---------------------------------------------------------------------------
# Quiet checkmark — neutral marker for "neither right nor wrong"
# ---------------------------------------------------------------------------

def quiet_check(pos, color=TEXT_MID, size=0.30):
    pts = [
        np.array([-size, 0.04, 0]),
        np.array([-0.10*size, -size, 0]),
        np.array([size*1.05, size*0.95, 0]),
    ]
    line = VMobject(stroke_color=color, stroke_width=4)
    line.set_points_as_corners(pts)
    line.move_to(pos)
    return line


# ---------------------------------------------------------------------------
# Icons: weight, ruler, both, equation, hand-on-slider
# ---------------------------------------------------------------------------

def icon_weight(pos, scale=1.0, color=TEXT_MID):
    body = Polygon(
        [-0.32, -0.36, 0], [ 0.32, -0.36, 0],
        [ 0.40,  0.20, 0], [-0.40,  0.20, 0],
        fill_color=color, fill_opacity=0.85, stroke_width=0,
    )
    handle = Arc(radius=0.22, start_angle=0, angle=PI,
                 stroke_color=color, stroke_width=4.0).shift(UP * 0.20)
    g = VGroup(body, handle).scale(scale).move_to(pos)
    return g


def icon_ruler(pos, scale=1.0, color=TEXT_MID):
    body = Rectangle(width=0.95, height=0.30, fill_color=color,
                     fill_opacity=0.85, stroke_width=0)
    ticks = VGroup()
    for k in range(1, 6):
        x = -0.45 + k * 0.15
        h = 0.10 if k % 2 else 0.16
        t = Line([x, 0.15, 0], [x, 0.15 - h, 0],
                 stroke_color=VOID, stroke_width=2.0)
        ticks.add(t)
    return VGroup(body, ticks).scale(scale).move_to(pos)


def icon_both(pos, scale=1.0, color=TEXT_MID):
    w = icon_weight(np.array([0, 0, 0]), scale=0.55, color=color
                    ).shift(LEFT * 0.30)
    r = icon_ruler(np.array([0, 0, 0]), scale=0.55, color=color
                   ).shift(RIGHT * 0.30 + DOWN * 0.05)
    return VGroup(w, r).scale(scale).move_to(pos)


def icon_equation(pos, scale=1.0, color=TEXT_DIM):
    try:
        eq = MathTex(r"F = G\,\frac{m_1 m_2}{r^2}", color=color)
    except Exception:
        eq = Text("F = G m1 m2 / r^2", font="sans", font_size=28, color=color)
    eq.scale(0.85 * scale).move_to(pos)
    return eq


def icon_hand_on_slider(pos, scale=1.0):
    # Mini slider track + fingertip
    track = RoundedRectangle(width=1.20, height=0.10, corner_radius=0.05,
                             fill_color=TRACK_BG, fill_opacity=1,
                             stroke_color="#3A3D44", stroke_width=1.0)
    fill = RoundedRectangle(width=0.70, height=0.10, corner_radius=0.05,
                            fill_color=TRACK_FG, fill_opacity=0.85,
                            stroke_width=0).shift(LEFT * 0.25)
    handle = Circle(radius=0.13, fill_color=HANDLE, fill_opacity=1,
                    stroke_color="#1A1F26", stroke_width=1.2
                    ).shift(RIGHT * 0.10)
    finger = RoundedRectangle(width=0.14, height=0.32, corner_radius=0.06,
                              fill_color="#D5A887", fill_opacity=1,
                              stroke_color="#7A4A28", stroke_width=1.0
                              ).shift(RIGHT * 0.10 + UP * 0.32)
    return VGroup(track, fill, handle, finger).scale(scale).move_to(pos)


# ---------------------------------------------------------------------------
# Thought bubble (empty, holds for a beat)
# ---------------------------------------------------------------------------

def thought_bubble(pos, width=1.7, height=1.0, color=TEXT_DIM):
    body = RoundedRectangle(width=width, height=height, corner_radius=0.32,
                            fill_color="#0D0F13", fill_opacity=1,
                            stroke_color=color, stroke_width=1.6)
    pip1 = Circle(radius=0.10, fill_color="#0D0F13", fill_opacity=1,
                  stroke_color=color, stroke_width=1.4
                  ).shift(DOWN * (height/2 + 0.10) + LEFT * 0.15)
    pip2 = Circle(radius=0.06, fill_color="#0D0F13", fill_opacity=1,
                  stroke_color=color, stroke_width=1.2
                  ).shift(DOWN * (height/2 + 0.30) + LEFT * 0.05)
    return VGroup(body, pip1, pip2).move_to(pos)


# ---------------------------------------------------------------------------
# Question mark (shy, floating)
# ---------------------------------------------------------------------------

def shy_question(pos, color=TEXT_DIM, opacity=0.55, size=64):
    q = Text("?", font="sans", font_size=size, color=color, weight=BOLD
             ).move_to(pos).set_opacity(opacity)
    return q


# ---------------------------------------------------------------------------
# Instruction text (single line, optional emphasized substring)
# ---------------------------------------------------------------------------

def instruction_line(text, y=INSTRUCTION_Y, color=TEXT_BRIGHT, size=30):
    t = Text(text, font="sans", font_size=size, color=color).move_to([0, y, 0])
    t.scale_to_fit_width(min(t.width, 12.0))
    return t


# ---------------------------------------------------------------------------
# Soft red X overlay (for the "random clicking is the trap" beat)
# ---------------------------------------------------------------------------

def red_x(pos, size=0.8, color=ACCENT_RED, stroke=6, opacity=0.85):
    l1 = Line([-size, -size, 0], [size, size, 0],
              stroke_color=color, stroke_width=stroke)
    l2 = Line([-size, size, 0], [size, -size, 0],
              stroke_color=color, stroke_width=stroke)
    return VGroup(l1, l2).move_to(pos).set_opacity(opacity)


# ---------------------------------------------------------------------------
# Full interface bundle — convenience for the many beats that need the
# whole homework page visible. Returns a dict; the caller decides what to
# add() / animate.
# ---------------------------------------------------------------------------

def make_interface(mass_a=0.50, mass_b=0.50, distance=0.55,
                   play_lit=False, timer_text="0.0 s",
                   instruction="Make these two rocks collide in exactly 60 seconds.",
                   attempts_filled=0, include_instruction=True,
                   include_attempts=False):
    canvas = make_canvas()
    sl_a = make_slider("Mass A",   value=mass_a,    y=SLIDER_Y_A)
    sl_b = make_slider("Mass B",   value=mass_b,    y=SLIDER_Y_B)
    sl_d = make_slider("Distance", value=distance,  y=SLIDER_Y_D)
    play = make_play_button(lit=play_lit)
    timer = make_timer(text=timer_text)
    panel = VGroup(sl_a, sl_b, sl_d, play, timer)
    out = {"canvas": canvas, "panel": panel,
           "slider_a": sl_a, "slider_b": sl_b, "slider_d": sl_d,
           "play": play, "timer": timer}
    if include_instruction:
        out["instruction"] = instruction_line(instruction)
    if include_attempts:
        out["attempts"] = make_attempt_dots(filled=attempts_filled)
    return out
