from manim import *
import numpy as np
from balancerig_helpers import (make_mobile, wrench_lever, com_marker,
                                small_label)

# "It is the same rule as a long wrench: reach matters as much as
#  force. And it is where the whole thing balances — its center of
#  mass — sitting right under the string."
DUR = 13.4


class BalancerigS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # PART 1: the long-wrench / lever inset
        wr = wrench_lever([-1.4, 1.2, 0], length=2.4, scale=0.9,
                          color="#EAE4D5", push=True)
        self.play(FadeIn(wr, shift=UP * 0.1), run_time=1.2)
        self.play(FadeIn(small_label("reach matters as much as force",
                                     [0, -0.2, 0], color="#8C8576",
                                     size=24)), run_time=1.0)
        self.wait(1.4)
        self.play(*[FadeOut(mo) for mo in self.mobjects], run_time=1.0)
        self.clear()
        self.camera.background_color = "#000000"

        # PART 2: the combined center of mass, right under the string
        m = make_mobile([0, 0.7, 0], half_w=3.0,
                        shapes=[(-2.4, 1.0, "#C98A6B"),
                                (-0.9, 0.6, "#9BD6B0"),
                                (1.6, 0.8, "#E8C46B"),
                                (2.6, 0.7, "#9BD6B0")],
                        ceil_y=3.4)
        self.play(FadeIn(m["group"]), run_time=1.2)
        # a thin plumb from the string straight down
        top = m["string"].get_end()
        plumb = DashedLine(top, [top[0], top[1] - 2.0, 0],
                           color="#B8B0A0", stroke_width=1.5
                           ).set_opacity(0.6)
        self.play(Create(plumb), run_time=1.0)
        com = com_marker([top[0], top[1] - 1.7, 0], scale=1.1)
        self.play(FadeIn(com, scale=1.2), run_time=1.2)
        self.wait(DUR - 9.6)
