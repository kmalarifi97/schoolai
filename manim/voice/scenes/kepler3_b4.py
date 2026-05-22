from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, radius_line,
                             divider, label, NEUTRAL, DIM, RED, CHALK)

# "Start with what you can actually measure. How far the planet sits from
#  the sun. Call it r — the size of the orbit itself."
DUR = 10.2

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        sun = make_sun(LC, scale=0.6)
        self.add(sun)

        r0 = 1.8
        ring = orbit_ring(LC, r=r0)
        planet = make_planet(
            LC + np.array([0, r0, 0]), r=0.16, color=NEUTRAL)
        self.add(ring, planet)
        self.wait(0.4)

        # Draw the radius line, label it r — line + r-slot glow RED together.
        rline = radius_line(LC, PI / 2, r0, color=RED)
        rlabel = label("r", LC + np.array([0.55, r0 / 2, 0]),
                       size=30, color=RED)
        self.play(Create(rline), run_time=1.0)

        # The RIGHT-side r symbol (the slot that will live in the equation).
        r_sym = MathTex("r", color=RED).scale(1.4).move_to([3.3, 0.2, 0])
        self.play(Write(rlabel), FadeIn(r_sym, scale=0.7), run_time=1.0)
        self.play(rline.animate.set_stroke(RED, width=6),
                  r_sym.animate.scale(1.18), run_time=0.5)
        self.play(rline.animate.set_stroke(RED, width=4),
                  r_sym.animate.scale(1 / 1.18), run_time=0.5)

        # Sweep r larger then smaller — the orbit balloons / shrinks; the
        # red line and red r grow/shrink in step.
        r_tr = ValueTracker(r0)

        def get_ring():
            return orbit_ring(LC, r=r_tr.get_value())
        ring.add_updater(lambda m: m.become(get_ring()))
        planet.add_updater(lambda m: m.move_to(
            LC + np.array([0, r_tr.get_value(), 0])))
        rline.add_updater(lambda m: m.become(
            radius_line(LC, PI / 2, r_tr.get_value(), color=RED, width=4)))
        rlabel.add_updater(lambda m: m.move_to(
            LC + np.array([0.55, r_tr.get_value() / 2, 0])))
        r_sym.add_updater(lambda m: m.set_height(
            0.42 + 0.18 * (r_tr.get_value() - 1.0)))

        self.play(r_tr.animate.set_value(2.9), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(r_tr.animate.set_value(1.1), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(r_tr.animate.set_value(1.8), run_time=1.2,
                  rate_func=rate_functions.ease_in_out_sine)
        for m in (ring, planet, rline, rlabel, r_sym):
            m.clear_updaters()
        self.wait(max(0.3, DUR - 9.6))
