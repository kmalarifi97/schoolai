from manim import *
import numpy as np
from balancerig_helpers import make_mobile, small_label

# "One goal. It hangs level. Not nose-down on one side."
DUR = 5.2


class BalancerigS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.3, 0], half_w=3.0,
                        shapes=[(-2.0, 0.9, "#C98A6B"),
                                (1.8, 0.9, "#9BD6B0")],
                        ceil_y=3.4)
        self.add(m["group"])

        bar = m["bar"]
        level = DashedLine(bar.get_left() + LEFT * 0.6,
                           bar.get_right() + RIGHT * 0.6,
                           color="#9BD6B0", stroke_width=2,
                           dash_length=0.14).set_opacity(0.7)
        self.play(Create(level), run_time=1.0)

        # the tilted-ghost we are trying to avoid
        ghost = m["rig"].copy().set_opacity(0.22)
        self.play(FadeIn(ghost), run_time=0.6)
        self.play(Rotate(ghost, angle=-0.34,
                         about_point=m["string"].get_end()),
                  run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 2.6)
