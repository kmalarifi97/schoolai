from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, divider, label,
                                make_equation_mE, CHALK, DIM, RED)

# "Put them in. Out comes six, times ten to the twenty-fourth, kilograms.
#  You just weighed the planet — without ever lifting it."
DUR = 10.5

LC = np.array([-3.5, 0.4, 0])


class WeighearthS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_earth(LC, r=1.15)
        self.add(earth)

        # The m_E equation up top.
        eq = make_equation_mE([3.3, 1.6, 0], scale=1.2)
        eq.get_part_by_tex("m_E").set_color(RED)
        self.add(eq)
        self.wait(0.4)

        # Plug numbers in.
        numbers = MathTex(
            r"m_E = \frac{(9.8)(6.37\times 10^{6})^{2}}{6.67\times 10^{-11}}",
            color=CHALK).scale(0.72).move_to([3.3, 0.1, 0])
        self.play(FadeIn(numbers, shift=UP * 0.2), run_time=1.6)
        self.wait(0.6)

        # Out comes ~6e24 kg.
        result = MathTex(r"\approx 6\times 10^{24}\ \text{kg}",
                         color=RED).scale(1.1).move_to([3.3, -1.4, 0])
        self.play(Write(result), run_time=1.4)
        self.play(Flash(result.get_center(), color=RED, line_length=0.25),
                  earth.body.animate.set_stroke(RED, width=5),
                  run_time=0.8)
        weighed = label("you weighed the planet — without lifting it",
                        [3.3, -2.4, 0], size=19, color=DIM)
        self.play(FadeIn(weighed), run_time=0.8)
        self.wait(max(0.3, DUR - 6.4))
