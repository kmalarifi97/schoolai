from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_clock, clock_wedge, divider,
                             label, make_equation, PLANET_A, PLANET_B,
                             RED, CHALK, DIM)

# "And the ratio of the years. T-A over T-B. How many times longer A's
#  year runs."
DUR = 7.1


class Kepler3S1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # LEFT: two clocks, A's visibly longer (more filled / bigger).
        clkA = make_clock([-4.4, 0.6, 0], r=0.75)
        clkB = make_clock([-2.4, 0.0, 0], r=0.48)
        self.add(clkA, clkB)
        self.add(clock_wedge(clkA, 0.70, color=RED))
        self.add(clock_wedge(clkB, 0.30, color=RED))
        lblA = label("T_A", [-4.4, -0.6, 0], size=24, color=PLANET_A)
        lblB = label("T_B", [-2.4, -0.8, 0], size=24, color=PLANET_B)
        self.play(FadeIn(lblA), FadeIn(lblB), run_time=0.8)
        longer = label("A's year is longer", [-3.4, -1.9, 0],
                       size=22, color=RED)
        self.play(FadeIn(longer), run_time=0.6)

        # RIGHT: full equation, T-fraction turns red (r-fraction already red).
        eq = make_equation([3.3, 0.2, 0], scale=1.1)
        eq.set_color(DIM)
        # r fraction stays red from b8
        VGroup(eq.lp_l, eq.rfrac, eq.rp_l).set_color(RED)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        self.add(eq)
        tfrac = VGroup(eq.lp_r, eq.tfrac, eq.rp_r)
        self.play(tfrac.animate.set_color(RED), run_time=1.0)
        eq.get_part_by_tex("T_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("T_B")[-1].set_color(PLANET_B)
        self.wait(max(0.3, DUR - 3.4))
