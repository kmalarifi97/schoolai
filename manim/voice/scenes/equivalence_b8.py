from manim import *
import numpy as np
from equivalence_helpers import (side_panel, make_ball, gravity_arrow,
                                 small_label, INK)

# "A coincidence, said Newton. A fact you write down and use."
DUR = 5.7


class EquivalenceS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        panel = side_panel([0, 0, 0], w=8.0, h=5.0, title="Newton")
        self.play(Create(panel[0]), FadeIn(panel[1]), run_time=1.0)
        ball = make_ball([-1.6, 1.4, 0], radius=0.34, big=True)
        arr = gravity_arrow([-1.6, 0.9, 0], length=0.9)
        self.play(FadeIn(ball), GrowArrow(arr), run_time=0.9)
        # bookkeeping: the two m's written, then struck through
        eqn = MathTex(r"m_i\,a \;=\; m_g\,g",
                      color=INK).scale(1.0).move_to([1.4, 0.6, 0])
        self.play(Write(eqn), run_time=1.1)
        strike = Line(eqn.get_left() + LEFT * 0.05,
                      eqn.get_right() + RIGHT * 0.05,
                      color="#8C98A6", stroke_width=2.5).set_opacity(0.7)
        cap = small_label("just bookkeeping", [1.4, -0.7, 0],
                          color="#8C98A6", size=22)
        self.play(Create(strike), FadeIn(cap), run_time=1.0)
        self.wait(DUR - 4.0)
