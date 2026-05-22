from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             divider, label, make_balance, make_equation_full,
                             PLANET, PLANET_D, DIM, RED, CHALK)

# "The planet's own mass cancels — its year doesn't care how heavy it is.
#  Solve for the time of one loop, and you get this."
DUR = 10.1

LC = np.array([-3.5, 0.6, 0])


class OrbitalS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.5))
        self.add(orbit_ring(LC, r=1.7))
        self.add(make_planet(planet_at(LC, 1.7, 0.0), color=PLANET,
                             edge=PLANET_D))

        # The balance, with m_p red on both sides (carried from b4).
        bal = make_balance([3.3, 0.9, 0], scale=0.95)
        bal.set_color(CHALK)
        bal.mp_left.set_color(RED)
        bal.mp_right.set_color(RED)
        self.add(bal)
        self.wait(0.6)

        # m_p cancels with a red strike on each side.
        strike_l = Line(bal.mp_left.get_corner(DL) + DOWN * 0.05 + LEFT * 0.05,
                        bal.mp_left.get_corner(UR) + UP * 0.05 + RIGHT * 0.05,
                        color=RED, stroke_width=4)
        strike_r = Line(bal.mp_right.get_corner(DL) + DOWN * 0.05 + LEFT * 0.05,
                        bal.mp_right.get_corner(UR) + UP * 0.05 + RIGHT * 0.05,
                        color=RED, stroke_width=4)
        self.play(Create(strike_l), Create(strike_r), run_time=0.9)
        cancel_note = label("the planet's mass drops out", [3.3, -0.4, 0],
                            size=20, color=RED)
        self.play(FadeIn(cancel_note), run_time=0.7)
        self.play(FadeOut(VGroup(bal.mp_left, bal.mp_right,
                                 strike_l, strike_r)), run_time=0.6)
        self.wait(0.3)

        # Algebra collapses to the period equation.
        eq = make_equation_full([3.3, -1.3, 0], scale=1.05)
        self.play(
            ReplacementTransform(VGroup(bal, cancel_note).copy(), eq),
            run_time=1.6)
        self.play(Flash(eq.get_center(), color=RED, line_length=0.25),
                  run_time=0.6)
        self.wait(max(0.3, DUR - 6.3))
