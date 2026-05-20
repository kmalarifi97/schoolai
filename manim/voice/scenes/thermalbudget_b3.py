from manim import *
import numpy as np
from thermalbudget_helpers import (ice_on_heater, thermometer,
                                   make_maha, qmark)

# "She turns the heater high. The thermometer races up, then stalls
#  dead at zero while the ice just sits there."
DUR = 9.3


class ThermalbudgetS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rig = ice_on_heater([-1.6, -0.4, 0], scale=1.0, heat=0.0,
                             melt=0.0)
        self.add(rig)
        maha = make_maha([-4.6, -0.5, 0], scale=0.9)
        self.add(maha)

        rig_hot = ice_on_heater([-1.6, -0.4, 0], scale=1.0, heat=0.95,
                                melt=0.0)
        self.play(Transform(rig, rig_hot), run_time=1.0)

        th = thermometer([3.0, 0.0, 0], scale=0.9, level=0.0)
        self.add(th)
        # races up...
        th_up = thermometer([3.0, 0.0, 0], scale=0.9, level=42)
        self.play(Transform(th, th_up), run_time=1.2,
                  rate_func=rate_functions.ease_out_sine)
        # then stalls dead at zero
        th_zero = thermometer([3.0, 0.0, 0], scale=0.9, level=0.0)
        self.play(Transform(th, th_zero), run_time=1.0)

        q = qmark([3.0, 2.4, 0])
        self.play(FadeIn(q), run_time=0.8)
        self.wait(DUR - 5.0)
