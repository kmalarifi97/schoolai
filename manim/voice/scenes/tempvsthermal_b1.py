from manim import *
import numpy as np
from tempvsthermal_helpers import make_match, make_bathtub

# "A lit match. And a warm bathtub."
DUR = 3.8


class TempvsthermalS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([-3.6, 0.0, 0], scale=1.05)
        tub = make_bathtub([2.2, -0.5, 0], scale=1.0)
        self.play(FadeIn(match, run_time=1.0))
        self.play(FadeIn(tub, run_time=1.0))
        # gentle flame flicker
        self.play(match[2].animate.scale(1.06),
                  run_time=0.7, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 2.7)
