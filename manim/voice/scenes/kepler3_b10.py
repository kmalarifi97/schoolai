from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, divider,
                             label, make_equation, PLANET_A, PLANET_AD,
                             PLANET_B, PLANET_BD, RED, CHALK, DIM)

# "Cube the distances. Square the times. And the two sides come out
#  exactly equal. That's the rule — Kepler's third law."
DUR = 9.9

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.55))

        rA, rB = 2.4, 1.4
        self.add(orbit_ring(LC, r=rA, color=PLANET_AD, width=2),
                 orbit_ring(LC, r=rB, color=PLANET_BD, width=2))
        pA = make_planet(LC + np.array([0, rA, 0]), r=0.16,
                         color=PLANET_A, edge=PLANET_AD)
        pB = make_planet(LC + np.array([0, rB, 0]), r=0.14,
                         color=PLANET_B, edge=PLANET_BD)
        self.add(pA, pB)

        # Equation with both fractions present (red), subscripts tinted.
        eq = make_equation([3.3, 0.2, 0], scale=1.15)
        eq.set_color(CHALK)
        VGroup(eq.lp_l, eq.rfrac, eq.rp_l).set_color(RED)
        VGroup(eq.lp_r, eq.tfrac, eq.rp_r).set_color(RED)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        # Show everything except cube, square, and = ; then snap them in.
        eq.cube.set_opacity(0)
        eq.square.set_opacity(0)
        eq.eqsign.set_opacity(0)
        self.add(eq)
        self.wait(0.6)

        # Cube the distances.
        self.play(eq.cube.animate.set_opacity(1).set_color(CHALK),
                  Flash(eq.cube.get_center() + RIGHT * 0.1, color=RED,
                        line_length=0.2), run_time=1.0)
        # Square the times.
        self.play(eq.square.animate.set_opacity(1).set_color(CHALK),
                  Flash(eq.square.get_center() + RIGHT * 0.1, color=RED,
                        line_length=0.2), run_time=1.0)
        # The = snaps shut.
        self.play(eq.eqsign.animate.set_opacity(1).set_color(CHALK),
                  run_time=0.7)

        # Full equation flashes once; A & B orbit in agreement.
        box = SurroundingRectangle(eq, color=RED, buff=0.25,
                                   corner_radius=0.1)
        self.play(Create(box), run_time=0.5)
        self.play(FadeOut(box), run_time=0.6)

        prog = ValueTracker(0.0)
        pA.add_updater(lambda m: m.move_to(
            LC + np.array([rA * np.cos(PI / 2 - 2 * np.pi * prog.get_value()),
                           rA * np.sin(PI / 2 - 2 * np.pi * prog.get_value()),
                           0])))
        pB.add_updater(lambda m: m.move_to(
            LC + np.array(
                [rB * np.cos(PI / 2 - 2 * np.pi * 2.2 * prog.get_value()),
                 rB * np.sin(PI / 2 - 2 * np.pi * 2.2 * prog.get_value()),
                 0])))
        self.play(prog.animate.set_value(1.0),
                  run_time=max(1.0, DUR - 6.4), rate_func=linear)
        pA.clear_updaters(); pB.clear_updaters()
        self.wait(0.3)
