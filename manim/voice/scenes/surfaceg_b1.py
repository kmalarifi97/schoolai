from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, divider, label,
                              CHALK, DIM, RED)

# "Newton's law works for ANY two masses. Now point it at something
#  personal — you, and the Earth under your feet."
DUR = 9.5

LC = np.array([-3.5, -0.9, 0])


class SurfacegS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Newton's law of gravitation, carried over from the previous video.
        law = MathTex(r"F = G\,\frac{m_1 m_2}{r^{2}}", color=CHALK).scale(1.2)
        law.move_to(ORIGIN)
        self.play(FadeIn(law), run_time=1.2)
        self.wait(1.0)

        # The frame splits; the law slides to the RIGHT scoreboard.
        self.play(Create(divider()),
                  law.animate.scale(0.9).move_to([3.3, 1.8, 0]),
                  run_time=1.4)

        # LEFT: the Earth, with a person standing on it.
        earth = make_world(LC, r=1.15, kind="earth")
        person = make_person(scale=1.0)
        person.move_to([LC[0], earth.get_top()[1] + 0.4, 0])
        self.play(FadeIn(earth, scale=0.85), run_time=1.2)
        self.play(FadeIn(person, shift=DOWN * 0.2), run_time=1.0)

        you = label("you", [LC[0] + 1.0, person.get_center()[1], 0],
                    size=24, color=DIM)
        earth_lbl = label("the Earth", [LC[0], LC[1] - 1.5, 0],
                          size=24, color=DIM)
        self.play(FadeIn(you), FadeIn(earth_lbl), run_time=1.0)
        self.wait(max(0.3, DUR - 6.8))
