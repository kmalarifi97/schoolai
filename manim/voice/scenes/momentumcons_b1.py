from manim import *
import numpy as np
from momentumcons_helpers import frozen_lake, make_figure, make_bag

# "Stand on a frozen lake, perfectly still. Throw a heavy bag forward."
DUR = 6.2


class MomentumconsS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        lake = frozen_lake((0, 0, 0))
        self.play(FadeIn(lake, run_time=1.0))
        fig = make_figure((-0.7, 0, 0), scale=1.0)
        bag = make_bag((0.4, 0, 0), scale=0.95)
        self.play(FadeIn(fig, scale=0.8), run_time=1.0)
        self.play(FadeIn(bag, scale=0.8), run_time=0.9)
        # perfectly still — just hold
        self.wait(DUR - 2.9)
