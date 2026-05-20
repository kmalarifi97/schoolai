from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                make_yousef)

# "Yousef built a spring launcher. Press a ball onto the spring,
#  release, and it should rise and tap a bell."
DUR = 9.1


class SpringdropS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.0)
        ball = make_ball(sp["top"] + UP * 0.22, r=0.24)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        you = make_yousef([1.6, -1.7, 0], scale=0.95)

        self.play(Create(sp["group"]), run_time=1.8)
        self.play(FadeIn(ball, shift=DOWN * 0.1), run_time=1.0)
        self.play(FadeIn(bell, shift=DOWN * 0.15), run_time=1.2)
        self.play(FadeIn(you, shift=UP * 0.15), run_time=1.0)
        self.wait(DUR - 5.0)
