from manim import *
import numpy as np
from balancerig_helpers import (balancing_act, level_indicator,
                                run_counter, small_label)

# "Her first prediction is wrong. That is not the problem. That is the
#  point. Each miss tells her which reach she misjudged."
DUR = 10.2


class BalancerigS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([-0.4, -0.2, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.9)
        pv = b["group"].get_center()
        self.add(b["group"])
        li = level_indicator([4.4, 1.6, 0], level=False, scale=0.85)
        rc = run_counter([3.6, -1.8, 0], used=0, total=3)
        self.add(li, rc)

        # run 1: clearly tilted (wrong)
        b["beam"].rotate(-0.22, about_point=pv)
        self.wait(1.0)
        # run 2: closer
        self.play(Rotate(b["beam"], angle=0.13, about_point=pv),
                  run_time=1.3,
                  rate_func=rate_functions.ease_in_out_sine)
        li2 = level_indicator([4.4, 1.6, 0], level=False, scale=0.85)
        self.play(Transform(li, li2), run_time=0.5)
        # run 3: level
        self.play(Rotate(b["beam"], angle=0.09, about_point=pv),
                  run_time=1.3,
                  rate_func=rate_functions.ease_in_out_sine)
        li3 = level_indicator([4.4, 1.6, 0], level=True, scale=0.85)
        self.play(Transform(li, li3), run_time=0.6)
        self.play(FadeIn(small_label("each miss = which reach",
                                     [-0.4, -2.5, 0], color="#8C8576",
                                     size=20)), run_time=0.9)
        self.wait(DUR - 7.4)
