from manim import *
import numpy as np
from balancerig_helpers import balancing_act, run_counter, small_label

# "She moves one mass. Predicts again. Three tries. That's all she
#  gets."
DUR = 6.5


class BalancerigS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([0, -0.3, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.95)
        self.add(b["group"])
        self.wait(0.4)

        # reposition one brick (the right stack moves outward, once)
        right_stack = b["bricks"][1]
        self.play(right_stack.animate.shift(RIGHT * b["step"]),
                  run_time=1.4,
                  rate_func=rate_functions.ease_in_out_sine)

        rc = run_counter([3.7, 2.2, 0], used=1, total=3)
        self.play(FadeIn(rc), run_time=1.0)
        self.play(FadeIn(small_label("deliberate — not random",
                                     [0, -2.5, 0], color="#8C8576",
                                     size=20)), run_time=0.9)
        self.wait(DUR - 3.7)
