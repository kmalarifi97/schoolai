from manim import *
import numpy as np
from balancerig_helpers import balancing_act, level_indicator

# "Then she lets go. And she watches the level indicator, not the
#  bricks."
DUR = 6.5


class BalancerigS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([-0.6, -0.3, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.95)
        self.add(b["group"])
        li = level_indicator([4.4, 1.2, 0], level=True, scale=0.95)
        self.add(li)
        self.wait(0.5)

        # released: the plank settles slightly off; indicator reacts
        pv = b["group"].get_center()
        self.play(Rotate(b["beam"], angle=-0.10, about_point=pv),
                  run_time=1.4, rate_func=rate_functions.ease_out_sine)
        # the camera's attention is on the indicator -> it shifts
        new_li = level_indicator([4.4, 1.2, 0], level=False,
                                 scale=0.95)
        self.play(Transform(li, new_li), run_time=1.2)
        self.wait(DUR - 3.6)
