from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                small_label)

# "The bell was never the homework. This is: in one sentence, your own
#  words — trace one unit of energy from the squeeze to the top."
DUR = 10.8


class SpringdropS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-3.4, -1.6, 0], height=1.4, compress=0.4)
        ball = make_ball(sp["top"] + UP * 0.2, r=0.20)
        bell = make_bell([-3.4, 1.6, 0], scale=0.7)
        self.add(sp["group"], ball, bell)
        self.wait(1.0)

        prompt = small_label("in one sentence, your own words —",
                             [1.0, 1.0, 0], size=24, color="#EAE4D5")
        line = Line([-1.2, -0.2, 0], [3.4, -0.2, 0], color="#5A5446",
                    stroke_width=2).set_opacity(0.6)
        self.play(FadeIn(prompt), run_time=1.2)
        self.play(Create(line), run_time=1.0)
        # silence holds — the launcher stays still
        self.wait(DUR - 4.2)
