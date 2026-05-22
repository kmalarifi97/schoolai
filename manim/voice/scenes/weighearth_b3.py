from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, divider, label,
                                make_equation_g, CHALK, DIM, RED)

# "But you don't have to lift it. The equation already holds the Earth's
#  mass inside it — just solve for that instead."
DUR = 9.8

LC = np.array([-3.5, 0.0, 0])


class WeighearthS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_earth(LC, r=1.2)
        self.add(earth)

        # RIGHT: the g-equation.
        eq = make_equation_g([3.3, 0.5, 0], scale=1.4)
        self.add(eq)
        self.wait(0.6)

        # The m_E inside it glows red — and the Earth on the left glows too.
        mE = eq.get_part_by_tex("m_E")
        self.play(
            mE.animate.set_color(RED),
            earth.body.animate.set_stroke(RED, width=5),
            run_time=1.2)

        # A ring circles m_E — it's the thing hiding inside the equation.
        ring = SurroundingRectangle(mE, color=RED, buff=0.12,
                                    corner_radius=0.08)
        self.play(Create(ring), run_time=1.0)
        note = label("the Earth's mass is already inside", [3.3, -1.6, 0],
                     size=21, color=RED)
        self.play(FadeIn(note), run_time=0.8)
        self.play(mE.animate.scale(1.2), run_time=0.5)
        self.play(mE.animate.scale(1 / 1.2), run_time=0.5)
        self.wait(max(0.3, DUR - 5.6))
