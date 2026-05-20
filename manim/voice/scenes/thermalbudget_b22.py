from manim import *
import numpy as np
from thermalbudget_helpers import callback_water_oil, small_label

# "And the water that drank energy and barely warmed, while the oil
#  shot up — the same heat, different substance?"
DUR = 9.4


class ThermalbudgetS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        cb = callback_water_oil([0, 0.1, 0], scale=1.5, opacity=0.0)
        self.play(cb.animate.set_opacity(0.9), run_time=1.6)
        self.wait(2.4)

        t = small_label("same heat — different substance",
                        [0, -2.6, 0], color="#8C8576", size=24)
        self.play(FadeIn(t), run_time=1.2)
        self.wait(DUR - 6.0)
