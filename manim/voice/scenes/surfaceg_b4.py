from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, make_feather,
                              make_hammer, divider, label,
                              make_equation_full, make_equation_reduced,
                              CHALK, DIM, RED)

# "Your own mass sits on both sides — so it cancels. Gravity's pull per
#  kilogram doesn't care how heavy you are. A feather and a hammer fall
#  together."
DUR = 12.1

LC = np.array([-3.5, -0.9, 0])


class SurfacegS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.15, kind="earth")
        self.add(earth)

        # RIGHT: the full equation with the two m's already red (from b3).
        eq = make_equation_full([3.3, 0.5, 0], scale=1.25)
        left_m = eq[0]
        num_m = eq[4][0]
        left_m.set_color(RED)
        num_m.set_color(RED)
        self.add(eq)
        self.wait(0.6)

        # The m's cancel — red strike through each.
        s1 = Line(left_m.get_corner(DL) + LEFT * 0.05 + DOWN * 0.02,
                  left_m.get_corner(UR) + RIGHT * 0.05 + UP * 0.02,
                  color=RED, stroke_width=5)
        s2 = Line(num_m.get_corner(DL) + LEFT * 0.05 + DOWN * 0.02,
                  num_m.get_corner(UR) + RIGHT * 0.05 + UP * 0.02,
                  color=RED, stroke_width=5)
        self.play(Create(s1), Create(s2), run_time=1.0)
        self.wait(0.4)

        # The two m's fade out (cancelled).
        self.play(
            FadeOut(VGroup(s1, s2), scale=0.4),
            FadeOut(left_m, scale=0.3, shift=UP * 0.3),
            FadeOut(num_m, scale=0.3, shift=UP * 0.3),
            run_time=1.0)

        # Collapse to the reduced equation g = G m_E / r_E^2 (clean crossfade).
        eqr = make_equation_reduced([3.3, 0.5, 0], scale=1.25)
        self.play(
            FadeOut(VGroup(eq[1], eq[2], eq[3], eq[4])),
            FadeIn(eqr),
            run_time=1.2)
        self.wait(0.4)

        # LEFT: a feather and a hammer drop side by side and land together.
        startY = 2.4
        feather = make_feather([LC[0] - 0.8, startY, 0], scale=1.0)
        hammer = make_hammer([LC[0] + 0.8, startY, 0], scale=1.0)
        self.play(FadeIn(feather), FadeIn(hammer), run_time=0.8)

        groundY = earth.get_top()[1] + 0.25
        # both fall at the same accelerating rate, land together
        self.play(
            feather.animate.move_to([LC[0] - 0.8, groundY, 0]),
            hammer.animate.move_to([LC[0] + 0.8, groundY, 0]),
            run_time=1.6, rate_func=rate_functions.ease_in_quad)
        # land flash
        self.play(
            Flash([LC[0] - 0.8, groundY, 0], color=CHALK, line_length=0.15),
            Flash([LC[0] + 0.8, groundY, 0], color=CHALK, line_length=0.15),
            run_time=0.6)
        self.wait(max(0.3, DUR - 7.9))
