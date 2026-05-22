from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d
from weighearth_helpers import (make_earth, make_cavendish, divider, label,
                                make_equation_mE, CHALK, DIM, RED)

# "No codes. m-Earth, the planet's mass — the thing we wanted. g and r,
#  what we could measure standing on it. Big G, the thread in Cavendish's
#  room. Read it: the equation that weighs worlds."
DUR = 15.0


class WeighearthS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The curved-space bend on the LEFT, with the Earth at the well.
        fabric = make_fabric_3d(dip_amount=1.1).shift(LEFT * 3.2)
        self.play(Create(fabric), run_time=2.0, lag_ratio=0.02)
        center = np.array([-3.2, -0.35, 0])
        earth = make_earth(center + np.array([0, 0.2, 0]), r=0.45)
        self.play(FadeIn(earth, scale=0.8), run_time=0.8)
        # Earth now labeled by its mass.
        emass = label("m_E = 6×10^24 kg",
                      center + np.array([0, -1.7, 0]), size=20, color=RED)
        self.play(FadeIn(emass), run_time=0.8)

        # RIGHT: the final m_E equation, fully lit and color-bound.
        eq = make_equation_mE([3.3, 1.9, 0], scale=1.2)
        self.add(eq)
        self.wait(0.4)

        mE = eq.get_part_by_tex("m_E")
        rE = eq.get_part_by_tex("r_E")
        frac = eq[2]
        g_glyph = frac[0]
        G_glyph = frac[5]

        # m_E — the thing we wanted (m_E + Earth pulse).
        self.play(mE.animate.set_color(RED),
                  earth.body.animate.set_stroke(RED, width=5), run_time=1.0)
        wanted = label("m_E — the thing we wanted", [3.3, 0.9, 0], size=20,
                       color=RED)
        self.play(FadeIn(wanted), run_time=0.6)
        self.wait(0.3)

        # g and r — what we could measure standing on it.
        self.play(g_glyph.animate.set_color(RED),
                  rE.animate.set_color(RED), run_time=1.0)
        meas = label("g, r — measured standing on it", [3.3, 0.1, 0],
                     size=20, color=DIM)
        self.play(FadeIn(meas), run_time=0.6)
        self.wait(0.3)

        # Big G — the thread in Cavendish's room.
        self.play(G_glyph.animate.set_color(RED), run_time=0.8)
        cav = make_cavendish([3.3, -1.4, 0], scale=0.55)
        self.play(FadeIn(cav), run_time=0.8)
        gnote = label("G — Cavendish's thread", [3.3, -2.5, 0], size=20,
                      color=DIM)
        self.play(FadeIn(gnote), run_time=0.6)

        # Hold the fully color-bound final.
        self.wait(max(0.4, DUR - 11.0))
