from manim import *
import numpy as np
from torque_helpers import make_bolt, make_wrench, force_arrow

# "A stuck bolt. You push the wrench with everything you have. Nothing."
DUR = 6.4


class TorqueS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-1.6, -0.2, 0])
        bolt = make_bolt(P, radius=0.42)
        wr = make_wrench(P, length=2.0, angle=0.0)
        self.play(FadeIn(bolt), FadeIn(wr), run_time=1.2)
        self.wait(0.6)
        # a strong push at the handle end, straining
        tip = P + np.array([0.50 + 2.0, 0, 0])
        f = force_arrow(tip, [0, 1.5, 0], width=9)
        self.play(GrowArrow(f), run_time=0.9)
        # strain: tiny tremor, no rotation
        for _ in range(3):
            self.play(VGroup(wr, f).animate.shift(UP * 0.04),
                      run_time=0.18, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 4.3)
