from manim import *
import numpy as np
from centerofmass_helpers import make_wrench

# "Throw a wrench, spinning, across the room."
DUR = 4.5


class CenterofmassS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wr = make_wrench(scale=0.62).move_to([-5.0, -1.4, 0])
        self.play(FadeIn(wr, run_time=0.6))
        # tumble end over end while flying across the room
        self.play(
            wr.animate.move_to([5.0, -0.6, 0]),
            Rotate(wr, angle=-3.4 * TAU, about_point=None),
            run_time=DUR - 1.4,
            rate_func=rate_functions.linear,
        )
        self.wait(0.8)
