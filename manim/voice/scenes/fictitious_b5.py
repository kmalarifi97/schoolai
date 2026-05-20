from manim import *
import numpy as np
from fictitious_helpers import (top_down_car, curve_path, outward_arrow,
                                straight_dashed, split_divider,
                                frame_label, PATH_COL, FORCE_COL)

# "The outward push was never a force. It was the feeling of your own
#  straight-line motion, seen from a turning frame."
DUR = 9.3


class FictitiousS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        div = split_divider(0.0)
        self.add(div)

        # LEFT: inside-the-car view — feels a force
        lcar = top_down_car([-3.4, 0.4, 0], scale=0.95, angle=0.0)
        larr = outward_arrow([-2.7, 0.6, 0], [1.4, 0, 0])
        lcap = frame_label("inside the car", [-3.4, 3.0, 0], size=24)
        lsub = frame_label("feels a force", [-3.4, -2.6, 0],
                           color=FORCE_COL, size=22)

        # RIGHT: ground view — just straight-line inertia
        road = curve_path([1.0, -2.4, 0], [6.2, 1.6, 0], bend=-2.0)
        rcar = top_down_car([1.8, -1.6, 0], scale=0.5, angle=-0.5)
        rtan = straight_dashed([1.8, -1.6, 0], [6.6, 0.7, 0])
        rcap = frame_label("from the ground", [3.7, 3.0, 0], size=24)
        rsub = frame_label("just straight-line inertia", [3.7, -2.6, 0],
                           color=PATH_COL, size=22)

        self.play(FadeIn(VGroup(lcar, lcap)),
                  FadeIn(VGroup(road, rcar, rcap)), run_time=1.2)
        self.play(GrowArrow(larr), Create(rtan), run_time=1.2)
        self.play(FadeIn(lsub), FadeIn(rsub), run_time=1.0)
        self.wait(DUR - 3.9)
