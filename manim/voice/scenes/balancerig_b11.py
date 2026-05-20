from manim import *
import numpy as np
from balancerig_helpers import make_mobile, balancing_act

# "Before she re-hangs another shape — she builds it where she can see
#  the twist."
DUR = 7.1


class BalancerigS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.7, 0], half_w=3.0,
                        shapes=[(-2.2, 0.9, "#C98A6B"),
                                (1.8, 0.8, "#E8C46B")],
                        ceil_y=3.4)
        self.add(m["group"])
        self.wait(0.6)

        # the mobile dissolves and resolves into Balancing Act
        b = balancing_act([0, -0.4, 0], half_w=3.2,
                          bricks=[(-3, 2), (2, 3)], scale=1.0)
        b["group"].set_opacity(0.0)
        self.play(m["group"].animate.set_opacity(0.0), run_time=1.4)
        self.play(b["group"].animate.set_opacity(1.0), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 3.6)
