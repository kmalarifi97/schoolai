from manim import *
import numpy as np
from machines_helpers import (make_boulder, make_fulcrum, make_bar,
                              bar_end, rise_trace, force_arrow, small_label)

# "The boulder barely moved. You pushed gently — but through a huge
#  distance."
DUR = 6.3


class MachinesS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground_y = -2.4
        piv = np.array([-1.4, ground_y + 0.55, 0])
        ful = make_fulcrum(piv, w=0.95, h=0.85)
        a0 = -0.30  # boulder (load) end up, effort end down
        bar = make_bar(piv, angle=a0, left_len=1.9, right_len=4.0)
        bld = make_boulder(bar_end(piv, a0, 1.9, -1) + UP * 0.78, scale=0.78)
        self.add(ful, bar, bld)
        self.wait(0.4)

        # tiny rise on the load side
        lo = bar_end(piv, 0.0, 1.9, -1)
        hi = bar_end(piv, a0, 1.9, -1)
        rt = rise_trace([lo[0] - 0.7, lo[1], 0], [lo[0] - 0.7, hi[1], 0],
                        color="#E8A86B")
        self.play(Create(rt), run_time=1.1)
        self.add(small_label("tiny", [lo[0] - 1.5, (lo[1] + hi[1]) / 2, 0],
                             color="#E8A86B", size=24))

        # gentle push arrow on effort side
        eff = bar_end(piv, a0, 4.0, 1)
        self.play(GrowArrow(force_arrow(eff + UP * 0.9, [0, -0.45, 0],
                                        color="#7FB8E8")), run_time=0.9)
        self.add(small_label("gentle, but far", eff + RIGHT * 0.2 + UP * 1.4,
                             color="#7FB8E8", size=24))
        self.wait(DUR - 3.4)
