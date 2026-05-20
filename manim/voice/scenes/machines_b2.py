from manim import *
import numpy as np
from machines_helpers import (make_boulder, make_fulcrum, make_bar,
                              bar_end, make_hand, force_arrow, small_label)

# "The boulder rises. With a force far smaller than its weight. It
#  feels like cheating."
DUR = 7.3


class MachinesS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground_y = -2.4
        piv = np.array([-1.4, ground_y + 0.55, 0])
        ful = make_fulcrum(piv, w=0.95, h=0.85)
        a0 = 0.0
        bar = make_bar(piv, angle=a0, left_len=1.9, right_len=4.0)
        bld = make_boulder(bar_end(piv, a0, 1.9, -1) + UP * 0.78, scale=0.78)
        hand = make_hand(bar_end(piv, a0, 4.0, 1) + UP * 0.4, scale=0.7)
        self.add(ful, bar, bld, hand)
        self.wait(0.5)

        a1 = -0.30  # bar rotates: effort end DOWN, load (boulder) end UP
        load0 = bar_end(piv, a0, 1.9, -1)
        load1 = bar_end(piv, a1, 1.9, -1)
        eff0 = bar_end(piv, a0, 4.0, 1)
        eff1 = bar_end(piv, a1, 4.0, 1)

        small_in = force_arrow(eff0 + UP * 0.95, [0, -0.55, 0], color="#7FB8E8")
        self.play(GrowArrow(small_in), run_time=0.7)
        self.play(
            Rotate(bar, a1 - a0, about_point=piv),
            bld.animate.shift(load1 - load0),
            hand.animate.shift(eff1 - eff0),
            small_in.animate.shift(eff1 - eff0),
            run_time=1.8, rate_func=rate_functions.ease_out_sine)

        tag = small_label("free lunch?", [3.4, 2.2, 0], color="#8C98A6",
                          size=28)
        self.play(FadeIn(tag, scale=0.7), run_time=0.9)
        self.wait(DUR - 4.9)
