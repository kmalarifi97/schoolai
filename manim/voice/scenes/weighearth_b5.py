from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, make_stone, make_cavendish,
                                divider, label, make_equation_mE,
                                CHALK, DIM, RED)

# "And every piece on the right, you already know. g is nine-point-eight —
#  you measured it by dropping a stone. r-Earth — measured by the ancient
#  Greeks. And big G — Cavendish, with two weights on a thread."
DUR = 16.1


class WeighearthS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # RIGHT: the m_E equation; right-side pieces light up one by one.
        eq = make_equation_mE([3.3, 1.6, 0], scale=1.25)
        eq.get_part_by_tex("m_E").set_color(RED)
        self.add(eq)
        frac = eq[2]  # the g r_E^2 / G fraction
        g_glyph = frac[0]            # g (numerator, leftmost)
        rE = eq.get_part_by_tex("r_E")
        G_glyph = frac[5]            # G (denominator)
        self.wait(0.6)

        # --- g: dropping a stone ---
        earth = make_earth([-4.6, -1.6, 0], r=0.7)
        self.add(earth)
        stone = make_stone([-4.6, 1.6, 0])
        self.play(FadeIn(stone), g_glyph.animate.set_color(RED), run_time=0.8)
        self.play(stone.animate.move_to([-4.6, -0.7, 0]), run_time=1.2,
                  rate_func=rate_functions.ease_in_quad)
        gval = label("g = 9.8\n(drop a stone)", [-4.6, 0.7, 0], size=19,
                     color=RED)
        self.play(FadeIn(gval), run_time=0.8)
        self.wait(0.6)

        # --- r_E: ancient measurement ---
        earth2 = make_earth([-2.0, 0.6, 0], r=0.6)
        rline = Line(earth2.get_center(),
                     earth2.get_center() + np.array([0.6, 0, 0]),
                     color=RED, stroke_width=4)
        self.play(FadeIn(earth2), rE.animate.set_color(RED), run_time=0.8)
        self.play(Create(rline), run_time=0.8)
        rval = label("r_E\n(the Greeks)", [-2.0, -0.7, 0], size=19, color=RED)
        self.play(FadeIn(rval), run_time=0.8)
        self.wait(0.6)

        # --- G: Cavendish torsion balance ---
        cav = make_cavendish([-3.3, -2.2, 0], scale=0.7)
        self.play(FadeIn(cav), G_glyph.animate.set_color(RED), run_time=1.0)
        Gval = label("G — Cavendish, two weights on a thread",
                     [-2.6, -3.3, 0], size=18, color=RED)
        self.play(FadeIn(Gval), run_time=0.8)
        self.wait(max(0.3, DUR - 11.0))
