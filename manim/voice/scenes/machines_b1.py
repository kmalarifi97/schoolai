from manim import *
import numpy as np
from machines_helpers import (make_boulder, make_fulcrum, make_bar,
                              bar_end, make_hand)

# "A boulder you cannot possibly lift. Slide a bar under it, rest it on
#  a rock, and push the far end down."
DUR = 8.9


class MachinesS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground_y = -2.4
        bld = make_boulder([-3.0, ground_y + 0.85, 0], scale=0.95)
        self.play(FadeIn(bld, shift=DOWN * 0.3), run_time=1.2)
        self.wait(0.6)

        piv = np.array([-1.4, ground_y + 0.55, 0])
        ful = make_fulcrum(piv, w=0.95, h=0.85)
        bar = make_bar(piv, angle=0.0, left_len=1.9, right_len=4.0)
        self.play(FadeIn(ful, shift=UP * 0.2), run_time=0.9)
        self.play(Create(bar), run_time=1.1)
        self.wait(0.4)

        hand = make_hand(bar_end(piv, 0.0, 4.0, 1) + UP * 0.4, scale=0.7)
        self.play(FadeIn(hand, shift=DOWN * 0.3), run_time=1.0)
        self.wait(DUR - 6.2)
