from manim import *
import numpy as np
from balancerig_helpers import (callback_wrench_bolt,
                                callback_tumbling_wrench,
                                balancing_act, com_marker, small_label)

# "This rig was both at once — twist, and the point it all balances on.
#  That is the concept."
DUR = 7.9


class BalancerigS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the two callbacks present, faint, on each side
        wb = callback_wrench_bolt([-3.6, 1.6, 0], scale=0.6,
                                  opacity=0.8)
        tw = callback_tumbling_wrench([3.6, 1.6, 0], scale=0.6,
                                      opacity=0.8)
        self.play(FadeIn(wb), FadeIn(tw), run_time=1.2)
        self.wait(0.6)

        # they converge into the level plank + CoM point
        center = np.array([0, 0.2, 0])
        self.play(
            wb.animate.move_to(center).scale(0.3).set_opacity(0.0),
            tw.animate.move_to(center).scale(0.3).set_opacity(0.0),
            run_time=1.8, rate_func=rate_functions.ease_in_out_sine)

        b = balancing_act([0, -0.4, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.9)
        com = com_marker([0, -1.55, 0], scale=1.0, label=False)
        self.play(FadeIn(b["group"], scale=1.04),
                  FadeIn(com, scale=1.1), run_time=1.6)
        self.play(FadeIn(small_label("twist  +  balance point",
                                     [0, 2.5, 0], color="#EAE4D5",
                                     size=24)), run_time=0.9)
        self.wait(DUR - 6.1)
