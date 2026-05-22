from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, radius_line,
                             make_clock, clock_wedge, divider, label,
                             make_equation, PLANET, PLANET_D, DIM, RED, CHALK)

# "Push the planet farther out, and its year grows — fast. The distance is
#  cubed under the root, so the year stretches by its cube root. Distance
#  rules the calendar."
DUR = 13.2

LC = np.array([-3.3, 0.6, 0])


class OrbitalS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.5))

        r_tr = ValueTracker(1.0)
        ring = always_redraw(lambda: orbit_ring(LC, r=r_tr.get_value()))
        planet = always_redraw(lambda: make_planet(
            LC + np.array([0, r_tr.get_value(), 0]), color=PLANET,
            edge=PLANET_D))
        rline = always_redraw(lambda: radius_line(
            LC, PI / 2, r_tr.get_value(), color=RED, width=4))
        self.add(ring, rline, planet)

        # Clock whose filled year grows ~ r^{3/2}.
        clk = make_clock([-3.3, -2.7, 0], r=0.5)
        self.add(clk)

        def year_frac():
            # T ~ r^{3/2}; normalized so r=1 -> 0.3 fill, capped at 1.
            return float(np.clip(0.30 * (r_tr.get_value() / 1.0) ** 1.5,
                                 0.0, 1.0))
        wedge = always_redraw(lambda: clock_wedge(clk, year_frac(), color=RED))
        self.add(wedge)
        self.add(label("T", [-2.4, -2.7, 0], size=24, color=RED))

        # Equation; r^3 under the root pulses red.
        eq = make_equation([3.3, 0.5, 0], scale=1.15)
        eq.set_color(CHALK)
        self.add(eq)
        self.play(eq.rcube.animate.set_color(RED).scale(1.3), run_time=0.8)
        self.play(eq.rcube.animate.scale(1 / 1.3), run_time=0.4)

        note = label("distance rules the calendar", [3.3, -1.6, 0],
                     size=22, color=DIM)
        self.play(FadeIn(note), run_time=0.8)

        # Sweep r outward — orbit balloons, year stretches.
        self.play(r_tr.animate.set_value(2.4), run_time=3.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        self.play(r_tr.animate.set_value(1.0), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(max(0.3, DUR - 9.5))
