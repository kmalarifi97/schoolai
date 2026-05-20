from manim import *
import numpy as np
from machines_helpers import (make_ramp, make_barrel, force_arrow,
                              rise_trace, small_label)

# "A ramp is the same deal. Sliding a barrel up a long slope is easy —
#  but you walk much farther."
DUR = 8.1


class MachinesS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tri, top, br, su = make_ramp([-4.4, -2.2, 0], base_len=7.0,
                                     height=2.6)
        self.play(Create(tri), run_time=1.2)

        start = br + np.array([-0.55, 0.35, 0])
        barrel = make_barrel(start, scale=0.85)
        self.play(FadeIn(barrel), run_time=0.7)

        end = top + np.array([0.05, 0.45, 0])
        # small push force along the slope
        push = force_arrow(start + np.array([0.5, 0.4, 0]), su * 0.9,
                           color="#7FB8E8")
        self.play(GrowArrow(push), run_time=0.7)
        self.play(barrel.animate.move_to(end),
                  push.animate.shift(end - start),
                  run_time=2.0, rate_func=rate_functions.linear)

        # contrast: the short straight-up height vs the long path
        rt = rise_trace([br[0] + 0.5, br[1], 0], [br[0] + 0.5, top[1], 0],
                        color="#E8A86B")
        self.add(rt)
        self.add(small_label("long path, small force",
                             [-0.6, -1.5, 0], color="#7FB8E8", size=24))
        self.wait(DUR - 5.6)
