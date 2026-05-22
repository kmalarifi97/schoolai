from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, radius_line,
                             divider, label, make_equation, PLANET_A,
                             PLANET_AD, PLANET_B, PLANET_BD, RED, CHALK, DIM)

# "Try the ratio of the distances. r-A over r-B. How many times farther A
#  sits than B."
DUR = 7.5

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.55))

        rA, rB = 2.6, 1.3
        ringA = orbit_ring(LC, r=rA, color=PLANET_AD, width=2)
        ringB = orbit_ring(LC, r=rB, color=PLANET_BD, width=2)
        pA = make_planet(LC + np.array([0, rA, 0]), r=0.16,
                         color=PLANET_A, edge=PLANET_AD)
        pB = make_planet(LC + np.array([0, rB, 0]), r=0.14,
                         color=PLANET_B, edge=PLANET_BD)
        self.add(ringA, ringB, pA, pB)

        # The two orbit radii highlight red; arrow: A's radius ~2x B's.
        lineA = radius_line(LC, -PI / 2, rA, color=RED, width=4)
        lineB = radius_line(LC, -PI / 2, rB, color=RED, width=4)
        self.play(Create(lineB), Create(lineA), run_time=1.0)
        ratio = label("about 2x", LC + np.array([1.0, -2.0, 0]),
                      size=22, color=RED)
        self.play(FadeIn(ratio), run_time=0.6)

        # RIGHT: build the equation, the r-fraction turns red.
        eq = make_equation([3.3, 0.2, 0], scale=1.1)
        eq.set_color(DIM)
        eq.get_part_by_tex("r_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("r_B")[-1].set_color(PLANET_B)
        eq.get_part_by_tex("T_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("T_B")[-1].set_color(PLANET_B)
        self.add(eq)
        # the r fraction (with parens) glows red
        rfrac = VGroup(eq.lp_l, eq.rfrac, eq.rp_l)
        self.play(rfrac.animate.set_color(RED), run_time=1.0)
        # keep subscript tints on top of the red
        eq.get_part_by_tex("r_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("r_B")[-1].set_color(PLANET_B)
        self.wait(max(0.3, DUR - 3.6))
