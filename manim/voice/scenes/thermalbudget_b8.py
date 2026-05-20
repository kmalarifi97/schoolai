from manim import *
import numpy as np
from thermalbudget_helpers import (energy_ledger, thermometer,
                                   small_label)

# "Some energy raises temperature — and how much it takes depends on
#  the substance and how much there is."
DUR = 8.8


class ThermalbudgetS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        led = energy_ledger(
            [("raise temperature", 0.0, "#D98C5F")],
            [-2.4, 1.3, 0], scale=1.0)
        self.play(FadeIn(led), run_time=1.0)
        led2 = energy_ledger(
            [("raise temperature", 0.55, "#D98C5F")],
            [-2.4, 1.3, 0], scale=1.0)
        self.play(Transform(led, led2), run_time=1.2)

        # a thermometer climbing for the temperature cost
        th = thermometer([3.4, 0.4, 0], scale=0.7, level=10)
        self.add(th)
        th2 = thermometer([3.4, 0.4, 0], scale=0.7, level=70)
        self.play(Transform(th, th2), run_time=1.4,
                  rate_func=rate_functions.ease_out_sine)

        rel = small_label("substance  x  amount  x  rise",
                          [-0.4, -2.2, 0], color="#8C8576", size=24)
        self.play(Write(rel), run_time=1.4)
        self.wait(DUR - 5.0)
