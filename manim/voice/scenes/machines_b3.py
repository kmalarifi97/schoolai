from manim import *
import numpy as np
from machines_helpers import (make_boulder, make_fulcrum, make_bar,
                              bar_end, make_hand, arc_trace, small_label)

# "It isn't. Watch your hand, not the rock. Your end traveled a long
#  way down."
DUR = 6.5


class MachinesS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground_y = -2.4
        piv = np.array([-1.4, ground_y + 0.55, 0])
        ful = make_fulcrum(piv, w=0.95, h=0.85)
        a0 = -0.30  # start tilted (continuing from b2): boulder up, hand down
        bar = make_bar(piv, angle=a0, left_len=1.9, right_len=4.0)
        bld = make_boulder(bar_end(piv, a0, 1.9, -1) + UP * 0.78, scale=0.78)
        hand = make_hand(bar_end(piv, a0, 4.0, 1) + UP * 0.4, scale=0.7)
        self.add(ful, bar, bld, hand)
        self.wait(0.4)

        # the long arc the effort end swept (effort side: angle == bar angle)
        ang_top = 0.0     # bar level
        ang_bot = a0      # bar tilted (effort end pushed down? -> use +a0 sweep)
        arc = arc_trace(piv, 4.0, ang_top, ang_bot, color="#7FB8E8")
        self.play(Create(arc), run_time=1.6)
        lbl = small_label("a long way", bar_end(piv, -0.15, 4.0, 1)
                          + RIGHT * 0.7 + UP * 0.3, color="#7FB8E8", size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 3.9)
