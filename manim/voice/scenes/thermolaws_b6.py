from manim import *
import numpy as np
from thermolaws_helpers import (make_beaker, ink_blobs, never_stamp,
                                small_label)

# "Drop ink in water; it spreads. You will never, ever watch it
#  gather itself back into a drop."
DUR = 7.8


class ThermolawsS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bk, bc = make_beaker([-3.0, 0, 0], scale=1.0)
        self.play(FadeIn(bk), run_time=1.0)
        # a tight drop of ink
        drop = ink_blobs(bc + [0, 0.2, 0], spread=0.0, n=22, seed=3)
        self.play(FadeIn(drop, scale=0.5), run_time=0.8)
        self.wait(0.3)
        # it diffuses
        spread = ink_blobs(bc + [0, -0.1, 0], spread=1.0, n=22, seed=3)
        self.play(Transform(drop, spread), run_time=2.0)
        self.wait(0.4)
        # the reverse, faded and crossed out
        rev = ink_blobs([3.0, 0.1, 0], spread=0.0, n=22, seed=3
                        ).set_opacity(0.35)
        rlbl = small_label("the reverse", [3.0, 1.8, 0], size=22,
                           color="#9B958A").set_opacity(0.6)
        self.play(FadeIn(rev), FadeIn(rlbl), run_time=0.8)
        nv = never_stamp([3.0, 0.0, 0], scale=1.0)
        self.play(FadeIn(nv), run_time=0.8)
        self.wait(DUR - 6.1)
