from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, divider, label,
                              qmark, CHALK, DIM, RED)

# "You feel your weight right now, pressing into the floor. But what IS
#  that, really?"
DUR = 7.4

LC = np.array([-3.5, -0.9, 0])


class SurfacegS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # carry the law on the scoreboard, dimmed
        law = MathTex(r"F = G\,\frac{m_1 m_2}{r^{2}}", color=DIM).scale(1.08)
        law.move_to([3.3, 1.8, 0])
        self.add(law)

        earth = make_world(LC, r=1.15, kind="earth")
        person = make_person(scale=1.0)
        person.move_to([LC[0], earth.get_top()[1] + 0.4, 0])
        self.add(earth, person)

        # A weight arrow points down from the person, into the Earth.
        top = person.get_bottom()
        arrow = Arrow(top + UP * 0.05, top + DOWN * 0.95, color=RED,
                      stroke_width=6, buff=0.05,
                      max_tip_length_to_length_ratio=0.3)
        wlabel = label("weight", [LC[0] + 1.1, top[1] - 0.5, 0],
                       size=24, color=RED)
        self.play(GrowArrow(arrow), run_time=1.2)
        self.play(FadeIn(wlabel), run_time=0.6)
        self.wait(0.6)

        # A big "?" beside it.
        q = qmark([LC[0] + 1.9, top[1] - 0.1, 0], size=80, color=CHALK,
                  opacity=0.9)
        self.play(FadeIn(q, scale=0.6), run_time=1.0)
        self.wait(max(0.3, DUR - 4.4))
