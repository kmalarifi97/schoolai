from manim import *
import numpy as np
from balancerig_helpers import make_mobile, small_label

# "Heavy near the middle does almost nothing. Light far out swings it a
#  lot. Same weights, opposite effects."
DUR = 9.1


class BalancerigS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # CASE A: heavy near pivot -> small swing
        a = make_mobile([-3.4, 1.4, 0], half_w=1.6,
                        shapes=[(-0.5, 1.0, "#C98A6B")],
                        ceil_y=3.4)
        self.play(FadeIn(a["group"]), run_time=1.0)
        self.play(Rotate(a["rig"], angle=-0.10,
                         about_point=a["string"].get_end()),
                  run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(small_label("heavy, near", [-3.4, -0.7, 0],
                                     color="#8C8576", size=20)),
                  run_time=0.6)

        # CASE B: light far out -> big swing
        b = make_mobile([3.2, 1.4, 0], half_w=1.9,
                        shapes=[(-1.7, 0.45, "#9BD6B0")],
                        ceil_y=3.4)
        self.play(FadeIn(b["group"]), run_time=1.0)
        self.play(Rotate(b["rig"], angle=0.55,
                         about_point=b["string"].get_end()),
                  run_time=1.2, rate_func=rate_functions.ease_in_sine)
        self.play(FadeIn(small_label("light, far out", [3.2, -0.9, 0],
                                     color="#8C8576", size=20)),
                  run_time=0.6)
        self.play(FadeIn(small_label("same weights — opposite effects",
                                     [0, -2.6, 0], color="#EAE4D5",
                                     size=24)), run_time=0.8)
        self.wait(DUR - 7.2)
