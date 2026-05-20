from manim import *
import numpy as np
from thermalbudget_helpers import callback_match_tub, small_label

# "And if this felt familiar — it should. Do you remember the tiny
#  match and the warm tub — hotter is not the same as more heat?"
DUR = 10.5


class ThermalbudgetS1B21(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.0)
        cb = callback_match_tub([0, 0.0, 0], scale=1.4, opacity=0.0)
        self.play(cb.animate.set_opacity(0.9), run_time=1.6)
        self.wait(2.2)

        t = small_label("hotter  ≠  more heat", [0, -2.6, 0],
                        color="#8C8576", size=24)
        self.play(FadeIn(t), run_time=1.2)
        self.wait(DUR - 6.0)
