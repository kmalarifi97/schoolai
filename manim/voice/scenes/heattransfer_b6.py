from manim import *
import numpy as np
from heattransfer_helpers import convection_loop, small_label

# "Hot water expands, grows light, rises. Cool water sinks to take its
#  place. The fluid carries the heat by moving."
DUR = 9.6


class HeattransferS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, 0.0, 0]
        loop = convection_loop(C, w=4.0, h=3.0)
        self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow)
                                else Create(a) for a in loop],
                              lag_ratio=0.05, run_time=2.4))

        rise = small_label("hot rises", [0, 1.95, 0],
                           color="#E0552B", size=26)
        sink = small_label("cool sinks", [2.55, -0.1, 0],
                           color="#5B8FC9", size=26)
        self.play(FadeIn(rise), run_time=1.0)
        self.play(FadeIn(sink), run_time=1.0)

        # let the loop pulse, conveying continuous motion
        self.play(loop.animate.scale(1.04),
                  rate_func=rate_functions.there_and_back, run_time=1.4)
        self.play(loop.animate.scale(1.04),
                  rate_func=rate_functions.there_and_back, run_time=1.4)
        self.wait(DUR - 7.2)
