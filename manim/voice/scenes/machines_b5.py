from manim import *
import numpy as np
from machines_helpers import make_balance, force_arrow, small_label

# "That's the bargain every machine makes. It trades force for
#  distance. It never gives you both."
DUR = 7.9


class MachinesS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bal, beam = make_balance([0, -0.3, 0], scale=1.2)
        self.play(FadeIn(bal), run_time=1.0)
        self.wait(0.4)

        # force on the left pan, distance on the right; product unchanged
        f_arr = force_arrow([-2.0, 1.6, 0], [0, -0.95, 0], color="#7FB8E8",
                            width=7)
        d_arr = force_arrow([2.0, 0.65, 0], [0, 0.95, 0], color="#A8C8A0",
                            width=7)
        self.play(GrowArrow(f_arr), run_time=0.8)
        self.play(GrowArrow(d_arr), run_time=0.8)
        self.add(small_label("force", [-2.0, 1.95, 0], color="#7FB8E8",
                             size=26),
                 small_label("distance", [2.0, 1.95, 0], color="#A8C8A0",
                             size=26))

        prod = small_label("force × distance  —  unchanged",
                           [0, -2.5, 0], color="#EAE4D5", size=28)
        # one rises as the other falls — beam tips, product holds
        self.play(f_arr.animate.scale(0.6, about_edge=UP),
                  d_arr.animate.scale(1.5, about_edge=DOWN),
                  Rotate(beam, -0.12, about_point=np.array([0, -0.3, 0]) + UP * 0.0),
                  run_time=1.6, rate_func=rate_functions.there_and_back)
        self.play(FadeIn(prod), run_time=0.9)
        self.wait(DUR - 6.4)
