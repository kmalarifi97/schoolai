from manim import *
import numpy as np
from balancerig_helpers import balancing_act, small_label

# "After — she explains the gap. Tipped right? The right twist won. By
#  how much tells her how far she was off."
DUR = 9.2


class BalancerigS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([0, -0.2, 0], half_w=3.0,
                          bricks=[(-3, 2), (2, 3)], scale=0.95)
        pv = b["group"].get_center()
        b["beam"].rotate(-0.16, about_point=pv)   # tipped right
        self.add(b["group"])
        self.wait(0.4)

        # the level target line + the imbalance gap highlighted
        target = DashedLine([pv[0] - 3.2, pv[1], 0],
                            [pv[0] + 3.2, pv[1], 0],
                            color="#9BD6B0", stroke_width=2
                            ).set_opacity(0.6)
        self.play(Create(target), run_time=1.0)

        right_end = b["plank"].get_right()
        gap = DoubleArrow([right_end[0], pv[1], 0],
                          [right_end[0], right_end[1], 0],
                          color="#C98A6B", stroke_width=4, buff=0,
                          max_tip_length_to_length_ratio=0.25)
        self.play(GrowArrow(gap), run_time=1.0)
        self.play(FadeIn(small_label("right twist won", [0, 2.5, 0],
                                     color="#E8C46B", size=24)),
                  run_time=0.9)
        self.play(FadeIn(small_label("how far off", [right_end[0] + 1.1,
                                     (pv[1] + right_end[1]) / 2, 0],
                                     color="#C98A6B", size=20)),
                  run_time=0.8)
        self.wait(DUR - 5.1)
