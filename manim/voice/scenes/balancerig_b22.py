from manim import *
import numpy as np
from balancerig_helpers import callback_tumbling_wrench, small_label

# "And the tumbling wrench whose one quiet point traced a clean arc —
#  the place a thing balances, whether or not it's in the middle?"
DUR = 10.8


class BalancerigS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)

        cb = callback_tumbling_wrench([0, 0.0, 0], scale=1.4,
                                      opacity=0.85)
        parab = cb.parab
        wrench = cb.wrench
        com = cb.com
        # ensure the path is a thin stroked arc, never a filled dome
        parab.set_fill(opacity=0.0)
        parab.set_stroke("#EAE4D5", width=2, opacity=0.5)

        # the path appears first, faint
        self.play(Create(parab), run_time=1.4)
        self.play(FadeIn(wrench), FadeIn(com), run_time=0.8)
        self.wait(0.4)

        # the wrench tumbles while its CoM glides the clean parabola
        self.play(
            MoveAlongPath(com, parab),
            MoveAlongPath(wrench, parab),
            Rotate(wrench, angle=4 * PI),
            run_time=3.4, rate_func=rate_functions.linear)
        self.wait(0.5)
        self.play(FadeIn(small_label("the point it balances on",
                                     [0, -2.4, 0], color="#8C8576",
                                     size=22)), run_time=1.1)
        self.wait(DUR - 8.4)
