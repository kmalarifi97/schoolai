from manim import *
import numpy as np
from efficiency_helpers import (winch, make_load, heat_shimmer, stream,
                                label, WORK_COLOR, USEFUL_COLOR, HEAT_COLOR)

# "You crank a real winch. Some of your effort lifts the load. Some just
#  warms the gears."
DUR = 7.1


class EfficiencyS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        w = winch([-1.6, 1.0, 0], scale=1.05)
        load = make_load([-1.6, -1.55, 0], size=0.6)
        self.play(FadeIn(w["group"]), FadeIn(load), run_time=1.1)

        # crank turns
        self.play(Rotate(w["crank"], -TAU, about_point=w["drum_center"]),
                  Rotate(w["handle"], -TAU, about_point=w["drum_center"]),
                  Rotate(w["drum"], -TAU, about_point=w["drum_center"]),
                  run_time=1.4)

        # most effort lifts the load
        lift = stream([-1.6, -0.05, 0], [-1.6, -1.0, 0],
                      color=USEFUL_COLOR, width=6)
        self.play(GrowArrow(lift),
                  load.animate.shift(UP * 0.7), run_time=1.3)
        self.add(label("lifts the load", [1.0, -1.0, 0], size=22,
                       color=USEFUL_COLOR))

        # a thin stream just warms the gears
        heat = heat_shimmer([-1.0, 1.3, 0], n=4, spread=0.5, rise=0.7)
        thin = stream([-1.6, 1.0, 0], [-1.05, 1.2, 0],
                      color=HEAT_COLOR, width=3)
        self.play(GrowArrow(thin), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in heat],
                              lag_ratio=0.15, run_time=1.0))
        self.add(label("warms the gears", [1.2, 1.3, 0], size=22,
                       color=HEAT_COLOR))
        self.wait(DUR - 5.8)
