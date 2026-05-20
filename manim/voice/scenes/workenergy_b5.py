from manim import *
import numpy as np
from workenergy_helpers import (make_cart, force_arrow,
                                displacement_arrow, work_region)

# "Force, times the distance it pushes through. That's work. And it
#  isn't lost — it goes somewhere."
DUR = 8.3


class WorkenergyS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fa = force_arrow([-3.6, 1.6, 0], length=1.6, direction=RIGHT,
                         label="F")
        da = displacement_arrow([-3.6, 0.4, 0], length=3.4,
                                direction=RIGHT, label="distance")
        self.play(GrowArrow(fa[0]), FadeIn(fa[1]), run_time=0.9)
        self.play(GrowArrow(da[0]), FadeIn(da[1]), run_time=0.9)
        self.wait(0.4)

        rect, rlbl = work_region([-3.6, -1.7, 0], w=3.4, h=1.3,
                                 label="W = F × distance")
        self.play(FadeIn(rect), run_time=0.8)
        self.play(Write(rlbl), run_time=0.9)
        self.wait(0.5)
        # goes somewhere — an arrow leading into a cart
        cart = make_cart([3.4, -1.05, 0], scale=0.85)
        flow = Arrow([-0.1, -1.05, 0], [2.4, -1.05, 0], color="#9CC97F",
                     stroke_width=6, buff=0.1,
                     max_tip_length_to_length_ratio=0.18)
        self.play(FadeIn(cart), run_time=0.6)
        self.play(GrowArrow(flow), run_time=1.0)
        self.wait(DUR - 6.0)
