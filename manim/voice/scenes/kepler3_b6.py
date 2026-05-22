from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, make_clock,
                             clock_wedge, divider, label, make_equation,
                             PLANET_A, PLANET_AD, PLANET_B, PLANET_BD,
                             RED, CHALK, DIM)

# "Now take two planets, not one. A and B. Not cryptic symbols — two
#  worlds, held side by side. Earth and Mars."
DUR = 9.3


class Kepler3S1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # LEFT splits into two mini-systems, stacked.
        TopC = np.array([-3.5, 1.5, 0])
        BotC = np.array([-3.5, -1.6, 0])

        sysA = VGroup(make_sun(TopC, scale=0.35),
                      orbit_ring(TopC, r=1.3))
        pA = make_planet(TopC + np.array([0, 1.3, 0]), r=0.16,
                         color=PLANET_A, edge=PLANET_AD)
        sysA.add(pA)
        lblA = label("A — Earth", TopC + np.array([1.7, 0.9, 0]),
                     size=22, color=PLANET_A)

        sysB = VGroup(make_sun(BotC, scale=0.35),
                      orbit_ring(BotC, r=1.0))
        pB = make_planet(BotC + np.array([0, 1.0, 0]), r=0.14,
                         color=PLANET_B, edge=PLANET_BD)
        sysB.add(pB)
        lblB = label("B — Mars", BotC + np.array([1.7, 0.7, 0]),
                     size=22, color=PLANET_B)

        self.play(FadeIn(sysA, shift=DOWN * 0.2), run_time=1.2)
        self.play(FadeIn(lblA), run_time=0.6)
        self.play(FadeIn(sysB, shift=UP * 0.2), run_time=1.2)
        self.play(FadeIn(lblB), run_time=0.6)
        self.wait(0.6)

        # RIGHT: the equation appears faint; subscripts pick up blue/green.
        eq = make_equation([3.3, 0.2, 0], scale=1.1)
        eq.set_color(DIM)
        self.play(FadeIn(eq), run_time=1.0)
        # Color the A subscripts blue, B subscripts green.
        rA = eq.get_part_by_tex("r_A"); rB = eq.get_part_by_tex("r_B")
        tA = eq.get_part_by_tex("T_A"); tB = eq.get_part_by_tex("T_B")
        # subscript = last glyph of each isolated part
        self.play(
            rA[-1].animate.set_color(PLANET_A),
            tA[-1].animate.set_color(PLANET_A),
            rB[-1].animate.set_color(PLANET_B),
            tB[-1].animate.set_color(PLANET_B),
            run_time=1.0)
        self.wait(max(0.3, DUR - 7.0))
