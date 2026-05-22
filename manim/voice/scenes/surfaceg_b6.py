from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, radius_line, divider,
                              label, make_equation_reduced,
                              CHALK, DIM, RED)

# "So g equals big G times the Earth's mass, over its radius squared. Put
#  in the numbers, and out comes nine-point-eight — the number you've
#  known all along."
DUR = 12.6

LC = np.array([-3.5, -0.6, 0])


class SurfacegS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.1, kind="earth")
        person = make_person(scale=0.8)
        person.move_to([LC[0], earth.get_top()[1] + 0.3, 0])
        self.add(earth, person)

        # The assembled equation, fully lit.
        eq = make_equation_reduced([3.3, 1.4, 0], scale=1.3)
        eq.get_part_by_tex("m_E").set_color(RED)
        eq.get_part_by_tex("r_E").set_color(RED)
        self.play(Write(eq), run_time=1.8)
        self.wait(0.6)

        # Plug numbers in below.
        numbers = MathTex(
            r"g = \frac{(6.67\times 10^{-11})(5.97\times 10^{24})}"
            r"{(6.37\times 10^{6})^{2}}",
            color=CHALK).scale(0.72).move_to([3.3, -0.4, 0])
        self.play(FadeIn(numbers, shift=UP * 0.2), run_time=1.6)
        self.wait(0.6)

        # Out comes 9.8 m/s^2.
        result = MathTex(r"= 9.8\ \text{m/s}^{2}", color=RED).scale(1.1)
        result.move_to([3.3, -1.9, 0])
        self.play(Write(result), run_time=1.2)
        self.play(Flash(result.get_center(), color=RED, line_length=0.25),
                  run_time=0.6)
        known = label("the number you've known all along",
                      [3.3, -2.7, 0], size=20, color=DIM)
        self.play(FadeIn(known), run_time=0.8)
        self.wait(max(0.3, DUR - 7.8))
