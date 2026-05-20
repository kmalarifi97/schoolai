from manim import *
import numpy as np
from thermalbudget_helpers import (ice_on_heater, thermometer,
                                   countdown_timer, small_label)

# "Then, all at once, the ice is gone and the temperature shoots up —
#  and overshoots, boiling before the buzzer."
DUR = 9.3


class ThermalbudgetS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rig = ice_on_heater([-1.8, -0.3, 0], scale=1.0, heat=1.0,
                             melt=0.12)
        self.add(rig)
        th = thermometer([2.9, 0.1, 0], scale=0.85, level=0.0)
        self.add(th)
        tmr = countdown_timer([5.0, 1.5, 0], scale=0.55, frac=0.35)
        self.add(tmr)

        # all at once: ice gone
        rig_melt = ice_on_heater([-1.8, -0.3, 0], scale=1.0, heat=1.0,
                                 melt=1.0)
        self.play(Transform(rig, rig_melt), run_time=1.2)

        # temperature shoots up and overshoots into boil
        th_boil = thermometer([2.9, 0.1, 0], scale=0.85, level=108)
        self.play(Transform(th, th_boil), run_time=1.6,
                  rate_func=rate_functions.ease_in_sine)

        boil = small_label("boiling", [2.9, 2.5, 0], color="#D98C5F",
                           size=24)
        self.play(FadeIn(boil), run_time=0.7)
        self.wait(DUR - 5.5)
