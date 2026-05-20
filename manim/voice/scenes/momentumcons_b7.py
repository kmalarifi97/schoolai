from manim import *
import numpy as np
from momentumcons_helpers import (isolated_boundary, make_figure,
                                  make_bag, label)

# "This holds whenever no outside force interferes. A system left to
#  itself. Isolated."
DUR = 6.9


class MomentumconsS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fig = make_figure((-1.4, 0, 0), scale=0.7)
        bag = make_bag((1.3, 0, 0), scale=0.65)
        self.add(fig, bag)
        self.wait(0.6)

        bnd = isolated_boundary((0, 0, 0), w=6.4, h=4.0, with_label=True)
        self.play(Create(bnd[0]), run_time=1.4)
        self.play(FadeIn(bnd[1]), run_time=0.8)

        # outside arrows try to cross but none do — they stop at the edge
        a1 = Arrow([-5.4, 1.0, 0], [-3.5, 1.0, 0], color="#5A6E80",
                   stroke_width=4, buff=0,
                   max_tip_length_to_length_ratio=0.3).set_opacity(0.5)
        a2 = Arrow([5.4, -1.0, 0], [3.5, -1.0, 0], color="#5A6E80",
                   stroke_width=4, buff=0,
                   max_tip_length_to_length_ratio=0.3).set_opacity(0.5)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        # they fade away — nothing interferes
        self.play(a1.animate.set_opacity(0.0),
                  a2.animate.set_opacity(0.0), run_time=1.0)
        self.wait(DUR - 4.8)
