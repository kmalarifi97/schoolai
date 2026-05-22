from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, make_clock,
                             clock_wedge, divider, label, make_equation,
                             PLANET_A, PLANET_B, RED, CHALK, DIM)

# "Why cubed, why squared? Double a planet's distance, and its year
#  doesn't just double — it stretches further. Those exponents are exactly
#  how much further."
DUR = 12.6

LC = np.array([-3.5, 0.8, 0])


class Kepler3S1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.5))

        r_tr = ValueTracker(1.2)
        ring = always_redraw(lambda: orbit_ring(LC, r=r_tr.get_value()))
        planet = always_redraw(lambda: make_planet(
            LC + np.array([0, r_tr.get_value(), 0]), r=0.15, color=CHALK,
            edge=DIM))
        self.add(ring, planet)

        # two bars showing r (red) and T (red) growing at different rates
        base_x = -1.0
        rbar_lbl = label("r", [base_x - 0.4, -2.1, 0], size=22, color=RED)
        tbar_lbl = label("T", [base_x - 0.4, -2.7, 0], size=22, color=RED)
        self.add(rbar_lbl, tbar_lbl)

        def rbar():
            w = (r_tr.get_value() / 1.2) * 0.9
            return Line([base_x, -2.1, 0], [base_x + w, -2.1, 0],
                        color=RED, stroke_width=10)

        def tbar():
            # T ~ r^{3/2}: doubling r -> ~2.83x T
            w = (r_tr.get_value() / 1.2) ** 1.5 * 0.9
            return Line([base_x, -2.7, 0], [base_x + w, -2.7, 0],
                        color=RED, stroke_width=10)
        self.add(always_redraw(rbar), always_redraw(tbar))

        # Equation, balanced, with cube + square highlighted.
        eq = make_equation([3.3, 0.8, 0], scale=1.0)
        eq.set_color(CHALK)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        self.add(eq)
        cube_note = label("cube", [2.3, -1.4, 0], size=22, color=RED)
        sq_note = label("square", [4.3, -1.4, 0], size=22, color=RED)
        self.play(eq.cube.animate.set_color(RED).scale(1.3),
                  FadeIn(cube_note), run_time=0.8)
        self.play(eq.square.animate.set_color(RED).scale(1.3),
                  FadeIn(sq_note), run_time=0.8)

        # Double r: orbit doubles, period stretches ~2.8x.
        self.play(r_tr.animate.set_value(2.4), run_time=2.6,
                  rate_func=rate_functions.ease_in_out_sine)
        x28 = label("year ~ 2.8x", [-3.4, -3.3, 0], size=22, color=RED)
        self.play(FadeIn(x28), run_time=0.8)
        self.wait(0.6)
        self.play(r_tr.animate.set_value(1.2), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(max(0.3, DUR - 8.0))
