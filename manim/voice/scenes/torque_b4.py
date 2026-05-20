from manim import *
import numpy as np
from torque_helpers import make_bolt, make_wrench, force_arrow

# "Push right at the bolt's center — and nothing turns, no matter how
#  hard."
DUR = 6.68


class TorqueS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([0.0, -0.2, 0])
        bolt = make_bolt(P, radius=0.46)
        wr = make_wrench(P, length=3.0, angle=0.0)
        self.add(bolt, wr)
        self.wait(0.6)
        # huge force applied AT the center / pivot itself
        f = force_arrow(P + np.array([0, 1.7, 0]), [0, -1.45, 0],
                        width=11)
        self.play(GrowArrow(f), run_time=0.9)
        # push harder: arrow lengthens, jitter, no rotation
        f2 = force_arrow(P + np.array([0, 2.1, 0]), [0, -1.85, 0],
                         width=12)
        self.play(Transform(f, f2), run_time=0.8)
        for _ in range(3):
            self.play(bolt.animate.scale(1.03), run_time=0.18,
                      rate_func=rate_functions.there_and_back)
        self.wait(DUR - 4.0)
