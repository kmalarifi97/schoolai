from manim import *
import numpy as np
from latentheat_helpers import (make_glass, make_flame, make_thermometer,
                                small_label)

# "Heat a glass of ice water and watch the thermometer."
DUR = 5.2


class LatentheatS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        glass = make_glass([-1.4, 0.7, 0], scale=1.0, ice_frac=1.0)
        flame = make_flame([-1.4, -1.9, 0], scale=1.0)
        therm = make_thermometer([2.4, 0.4, 0], scale=1.0, level=0.0)
        self.play(FadeIn(glass), run_time=1.0)
        self.play(FadeIn(flame, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(therm, shift=LEFT * 0.3), run_time=1.0)
        self.wait(DUR - 2.9)
