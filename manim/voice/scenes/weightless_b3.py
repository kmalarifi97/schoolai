from manim import *
import numpy as np
from weightless_helpers import make_astronaut, question_mark

# "So if gravity is still pulling them — why don't they feel it?"
DUR = 5.7


class WeightlessS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        astro = make_astronaut([-1.0, 0.2, 0], scale=1.05, tilt=0.2)
        self.play(FadeIn(astro, scale=0.85), run_time=1.0)
        self.play(astro.animate.shift(UP * 0.25).rotate(0.1),
                  run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        qm = question_mark([2.0, 0.5, 0], size=88)
        self.play(FadeIn(qm, scale=0.6), run_time=0.9)
        self.wait(DUR - 3.5)
