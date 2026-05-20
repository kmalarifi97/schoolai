from manim import *
import numpy as np
from balancerig_helpers import make_mobile

# "So she moves a heavy shape to the left. Now it slams over the other
#  way."
DUR = 6.7


class BalancerigS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.3, 0], half_w=3.0,
                        shapes=[(-1.4, 0.6, "#9BD6B0"),
                                (1.4, 0.9, "#C98A6B"),
                                (2.6, 0.8, "#E8C46B")],
                        ceil_y=3.4)
        pv = m["string"].get_end()
        m["rig"].rotate(-0.5, about_point=pv)   # still tilted right
        self.add(m["ceiling"], m["string"], m["rig"])
        self.wait(0.6)

        # the heavy shape (index 1) is dragged from right to left
        heavy = m["shapes"][1]
        self.play(heavy.animate.shift(LEFT * 3.8), run_time=1.4,
                  rate_func=rate_functions.ease_in_out_sine)
        # over-corrects: slams left
        self.play(Rotate(m["rig"], angle=0.92, about_point=pv),
                  run_time=1.3, rate_func=rate_functions.ease_in_sine)
        self.play(Rotate(m["rig"], angle=-0.05, about_point=pv),
                  run_time=0.5, rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 4.3)
