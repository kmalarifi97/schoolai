from manim import *
import numpy as np
from machines_helpers import (make_fulcrum, make_bar, bar_end,
                              force_arrow, small_label, title_label)

# "Computing the mechanical advantage of a lever or ramp from its
#  dimensions, and the input force a given load needs — that's yours."
DUR = 10.3


class MachinesS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        piv = np.array([0, -0.2, 0])
        ful = make_fulcrum(piv, w=0.9, h=0.8)
        bar = make_bar(piv, angle=0.0, left_len=2.2, right_len=3.6)
        self.play(Create(bar), FadeIn(ful), run_time=1.4)

        load_end = bar_end(piv, 0.0, 2.2, -1)
        eff_end = bar_end(piv, 0.0, 3.6, 1)
        # labelled arms
        arm_in = DoubleArrow(piv + UP * 0.7, eff_end + UP * 0.7,
                             color="#7FB8E8", stroke_width=3,
                             buff=0, tip_length=0.18)
        arm_out = DoubleArrow(load_end + UP * 0.7, piv + UP * 0.7,
                              color="#E8A86B", stroke_width=3,
                              buff=0, tip_length=0.18)
        self.play(GrowFromCenter(arm_in), GrowFromCenter(arm_out),
                  run_time=1.2)
        self.add(small_label("effort arm", eff_end * 0.5 + piv * 0.5
                             + UP * 1.05, color="#7FB8E8", size=24),
                 small_label("load arm", load_end * 0.5 + piv * 0.5
                             + UP * 1.05, color="#E8A86B", size=24))

        # output / load force down, input arrow left open
        self.play(GrowArrow(force_arrow(load_end + DOWN * 0.15,
                                        [0, -1.0, 0], color="#E8A86B")),
                  run_time=0.8)
        q = title_label("MA = ?", [0, 2.4, 0], size=40)
        self.play(Write(q), run_time=1.2)
        self.wait(DUR - 5.8)
