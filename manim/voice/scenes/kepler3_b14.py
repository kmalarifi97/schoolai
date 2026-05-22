from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, radius_line,
                             make_clock, clock_wedge, clock_hand, divider,
                             label, make_equation, PLANET_A, PLANET_AD,
                             PLANET_B, PLANET_BD, RED, CHALK, DIM)

# "No more weird codes. r is the orbit's width. T is the planet's year. A
#  and B, two worlds. The exponents, the rhythm of the curve. Read it now
#  — you can read it."
DUR = 13.0

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.55))

        r0 = 2.0
        ring = orbit_ring(LC, r=r0)
        rline = radius_line(LC, PI / 2, r0, color=CHALK, width=4)
        pA = make_planet(LC + np.array([0, r0, 0]), r=0.16,
                         color=PLANET_A, edge=PLANET_AD)
        pB = make_planet(LC + np.array([r0 * 0.6, -r0 * 0.6, 0]), r=0.13,
                         color=PLANET_B, edge=PLANET_BD)
        clk = make_clock([-2.0, -2.5, 0], r=0.5)
        wedge = clock_wedge(clk, 0.4, color=CHALK)
        hand = clock_hand(clk, 0.4)
        self.add(ring, rline, pA, pB, clk, wedge, hand)

        eq = make_equation([3.3, 0.2, 0], scale=1.2)
        eq.set_color(CHALK)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        self.add(eq)
        self.wait(0.8)

        # r + orbit pulse red together.
        self.play(
            eq.rfrac.animate.set_color(RED),
            rline.animate.set_stroke(RED, width=6),
            ring.animate.set_stroke(RED, opacity=0.9),
            run_time=1.2)
        # restore subscript tints
        eq.get_part_by_tex("r_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("r_B")[-1].set_color(PLANET_B)
        self.wait(0.4)

        # T + clock pulse red together.
        new_wedge = clock_wedge(clk, 0.4, color=RED)
        self.play(
            eq.tfrac.animate.set_color(RED),
            Transform(wedge, new_wedge),
            run_time=1.2)
        eq.get_part_by_tex("T_A")[-1].set_color(PLANET_A)
        eq.get_part_by_tex("T_B")[-1].set_color(PLANET_B)
        self.wait(0.4)

        # A pulse blue (planet A + its subscripts).
        self.play(
            eq.get_part_by_tex("r_A")[-1].animate.scale(1.4),
            eq.get_part_by_tex("T_A")[-1].animate.scale(1.4),
            Flash(pA.get_center(), color=PLANET_A, line_length=0.2),
            run_time=1.0)
        self.play(
            eq.get_part_by_tex("r_A")[-1].animate.scale(1 / 1.4),
            eq.get_part_by_tex("T_A")[-1].animate.scale(1 / 1.4),
            run_time=0.5)

        # B pulse green (planet B + its subscripts).
        self.play(
            eq.get_part_by_tex("r_B")[-1].animate.scale(1.4),
            eq.get_part_by_tex("T_B")[-1].animate.scale(1.4),
            Flash(pB.get_center(), color=PLANET_B, line_length=0.2),
            run_time=1.0)
        self.play(
            eq.get_part_by_tex("r_B")[-1].animate.scale(1 / 1.4),
            eq.get_part_by_tex("T_B")[-1].animate.scale(1 / 1.4),
            run_time=0.5)

        # hold steady
        self.wait(max(0.4, DUR - 9.5))
