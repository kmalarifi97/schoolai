from manim import *
import numpy as np
from thermalbudget_helpers import (metal_cup, thermometer,
                                   small_label)

# "She swaps to a metal cup to help. It heats the water faster than she
#  expects and ruins her timing again."
DUR = 9.0


class ThermalbudgetS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cup = metal_cup([-1.8, -0.2, 0], scale=1.05, heat=0.85,
                        fill=0.45)
        self.play(FadeIn(cup, shift=UP * 0.15), run_time=1.2)

        lbl = small_label("metal cup", [-1.8, 1.7, 0], color="#B9BFC6",
                          size=22)
        self.play(FadeIn(lbl), run_time=0.7)

        th = thermometer([2.9, 0.0, 0], scale=0.85, level=8)
        self.add(th)
        # rise far steeper than predicted
        th_fast = thermometer([2.9, 0.0, 0], scale=0.85, level=95)
        self.play(Transform(th, th_fast), run_time=1.6,
                  rate_func=rate_functions.ease_in_sine)

        miss = small_label("too fast", [2.9, 2.4, 0], color="#D98C5F",
                           size=22)
        self.play(FadeIn(miss), run_time=0.7)
        self.wait(DUR - 4.9)
