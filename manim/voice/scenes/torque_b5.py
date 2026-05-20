from manim import *
import numpy as np
from torque_helpers import make_bolt, make_wrench, force_arrow, small_label

# "Push at the same spot but straight along the handle — also nothing.
#  The direction matters too."
DUR = 8.27


class TorqueS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([2.4, -0.2, 0])
        bolt = make_bolt(P, radius=0.44)
        wr = make_wrench(P, length=4.0, angle=PI)  # handle to the left
        self.add(bolt, wr)
        self.wait(0.6)
        # force applied at the handle end, pointing straight along the
        # handle toward the pivot -> no turning
        end = P + np.array([-(0.44 + 4.0), 0, 0])
        f = force_arrow(end, [1.6, 0, 0], width=8)
        self.play(GrowArrow(f), run_time=1.0)
        self.play(f.animate.shift(RIGHT * 0.10), run_time=0.5,
                  rate_func=rate_functions.there_and_back)
        lbl = small_label("force along the handle — no turn",
                          P + np.array([-1.6, -1.5, 0]), size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 4.0)
