from manim import *
import numpy as np
from balancerig_helpers import balancing_act, hand_hold, small_label

# "Here is the real job. Not letting go of the plank. Predicting —
#  before she does."
DUR = 7.3


class BalancerigS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([0, -0.2, 0], half_w=3.2,
                          bricks=[(-3, 2), (2, 2)], scale=1.0)
        self.add(b["group"])
        self.wait(0.4)

        # a hand deliberately holding the plank level, NOT releasing
        hand = hand_hold([3.4, 0.55, 0], scale=1.0)
        self.play(FadeIn(hand, shift=DOWN * 0.15), run_time=1.2)
        self.play(FadeIn(small_label("not letting go — yet",
                                     [0, -2.4, 0], color="#8C8576",
                                     size=22)), run_time=1.0)
        self.wait(0.5)
        self.play(FadeIn(small_label("predict first", [0, 2.5, 0],
                                     color="#EAE4D5", size=26)),
                  run_time=1.0)
        self.wait(DUR - 4.1)
