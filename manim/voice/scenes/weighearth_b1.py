from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, divider, label,
                                make_equation_g, CHALK, DIM, RED)

# "You just found g equals big G times Earth's mass over its radius
#  squared. Now do something audacious. Flip it around."
DUR = 9.9

LC = np.array([-3.5, 0.0, 0])


class WeighearthS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The g-equation, carried over from the previous (surfaceg) video.
        eq = make_equation_g(ORIGIN, scale=1.4)
        self.play(Write(eq), run_time=1.8)
        self.wait(1.0)

        # The frame splits; the equation slides to the RIGHT scoreboard.
        self.play(Create(divider()),
                  eq.animate.scale(0.85).move_to([3.3, 0.5, 0]),
                  run_time=1.4)

        # LEFT: the Earth.
        earth = make_earth(LC, r=1.25)
        self.play(FadeIn(earth, scale=0.85), run_time=1.2)

        # "Flip it around" — a curved arrow circles the equation.
        flip = CurvedArrow(eq.get_top() + UP * 0.3 + RIGHT * 0.6,
                           eq.get_bottom() + DOWN * 0.3 + RIGHT * 0.6,
                           color=RED, angle=-PI * 1.2, stroke_width=4)
        flab = label("flip it around", [3.3, -1.6, 0], size=24, color=RED)
        self.play(Create(flip), FadeIn(flab), run_time=1.4)
        self.wait(max(0.3, DUR - 6.8))
