from manim import *
import numpy as np
from balancerig_helpers import callback_wrench_bolt, small_label

# "And if this felt familiar — it should. Do you remember the stuck
#  bolt, and how a longer wrench turned it with a gentler push — reach
#  against force?"
DUR = 12.1


class BalancerigS1B21(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.0)

        # the torque callback: short vs long wrench on a bolt, faint
        cb = callback_wrench_bolt([0, 0.3, 0], scale=1.3, opacity=0.0)
        self.play(cb.animate.set_opacity(0.85), run_time=1.6)
        self.wait(1.4)

        # the long wrench gives more turn with a gentler push
        self.play(FadeIn(small_label("reach against force",
                                     [0, -2.0, 0], color="#8C8576",
                                     size=24)), run_time=1.2)
        self.wait(2.0)
        self.play(cb.animate.set_opacity(0.55), run_time=1.4)
        self.wait(DUR - 8.6)
