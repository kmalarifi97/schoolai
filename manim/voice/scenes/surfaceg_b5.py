from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, radius_line, divider,
                              label, make_equation_reduced,
                              CHALK, DIM, RED)

# "What's left is g — the pull per kilogram at the surface. It depends
#  only on the Earth's mass, and your distance from its center: its
#  radius."
DUR = 11.6

LC = np.array([-3.5, -0.6, 0])


class SurfacegS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.2, kind="earth")
        person = make_person(scale=0.85)
        person.move_to([LC[0], earth.get_top()[1] + 0.32, 0])
        self.add(earth, person)

        # RIGHT: the reduced equation g = G m_E / r_E^2.
        eq = make_equation_reduced([3.3, 0.4, 0], scale=1.3)
        g_sym = eq[0]
        self.add(eq)

        # g — the pull per kilogram at the surface (g glows red briefly).
        self.play(g_sym.animate.set_color(RED), run_time=0.8)
        gnote = label("pull per kilogram", [3.3, -1.4, 0], size=22,
                      color=RED)
        self.play(FadeIn(gnote), run_time=0.8)
        self.play(g_sym.animate.set_color(CHALK), FadeOut(gnote),
                  run_time=0.8)
        self.wait(0.3)

        # m_E: the Earth's mass — body + m_E symbol glow red.
        mE = eq.get_part_by_tex("m_E")
        mlabel = label("m_E", [LC[0] + 1.0, LC[1] - 1.6, 0], size=26,
                       color=RED)
        self.play(
            earth.body.animate.set_stroke(RED, width=5),
            mE.animate.set_color(RED),
            FadeIn(mlabel),
            run_time=1.2)
        self.wait(0.4)

        # r_E: distance to center -> radius line + r_E symbol glow red.
        rline = radius_line(earth, angle=-PI / 4, color=RED, width=5)
        rlabel = label("r_E",
                       earth.center_pt + np.array([1.15, -0.65, 0]),
                       size=26, color=RED)
        rE = eq.get_part_by_tex("r_E")
        self.play(
            Create(rline),
            rE.animate.set_color(RED),
            FadeIn(rlabel),
            run_time=1.4)
        self.wait(max(0.3, DUR - 7.5))
