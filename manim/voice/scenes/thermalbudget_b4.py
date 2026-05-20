from manim import *
import numpy as np
from thermalbudget_helpers import (ice_on_heater, thermometer,
                                   heat_rate_control, small_label)

# "She thinks the heater died. She turns it higher. The needle still
#  won't move off zero."
DUR = 7.7


class ThermalbudgetS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rig = ice_on_heater([-1.8, -0.3, 0], scale=1.0, heat=0.95,
                             melt=0.02)
        self.add(rig)
        th = thermometer([2.9, 0.1, 0], scale=0.85, level=0.0)
        self.add(th)

        hr = heat_rate_control([-1.8, -2.6, 0], frac=0.6, w=3.0,
                               label="heat rate")
        self.play(FadeIn(hr), run_time=0.9)
        # crank it higher
        target = hr.rail.get_right() + LEFT * 0.15
        self.play(hr.knob.animate.move_to(
            [target[0], hr.knob.get_center()[1], 0]), run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine)

        rig_more = ice_on_heater([-1.8, -0.3, 0], scale=1.0, heat=1.0,
                                 melt=0.10)
        self.play(Transform(rig, rig_more), run_time=1.2)

        # needle frozen
        froz = small_label("0", [3.45, -0.85, 0], color="#9BD6B0",
                           size=22)
        self.play(FadeIn(froz), run_time=0.6)
        self.wait(DUR - 4.9)
