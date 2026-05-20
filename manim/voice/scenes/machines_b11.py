from manim import *
import numpy as np
from machines_helpers import (make_boulder, make_fulcrum, make_bar,
                              bar_end, make_hand, work_bars, small_label)

# "The machine never makes energy. It only reshapes the deal — so a
#  human can do a job a human couldn't."
DUR = 8.7


class MachinesS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the lever scene returns, smaller, up top
        ground_y = 0.4
        piv = np.array([-1.2, ground_y + 0.4, 0])
        ful = make_fulcrum(piv, w=0.6, h=0.55)
        a0 = -0.22  # boulder (load) end lifted, effort end down
        bar = make_bar(piv, angle=a0, left_len=1.3, right_len=2.7)
        bld = make_boulder(bar_end(piv, a0, 1.3, -1) + UP * 0.5, scale=0.5)
        hand = make_hand(bar_end(piv, a0, 2.7, 1) + UP * 0.3, scale=0.5)
        self.play(FadeIn(VGroup(ful, bar, bld, hand)), run_time=1.2)
        self.wait(0.4)

        # energy bar identical in and out — only its shape changed
        wb = work_bars([0.3, -1.9, 0], scale=1.0, in_w=3.2, out_w=3.2)
        in_bar, out_bar, in_lbl, out_lbl = wb
        self.play(FadeIn(in_lbl), FadeIn(out_lbl), run_time=0.7)
        self.play(GrowFromEdge(in_bar, LEFT),
                  GrowFromEdge(out_bar, LEFT), run_time=1.3)
        self.add(small_label("same energy — different shape",
                             [0.3, -3.1, 0], color="#EAE4D5", size=26))
        self.wait(DUR - 4.9)
