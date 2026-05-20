from manim import *
import numpy as np
from thermalbudget_helpers import (ice_on_heater, countdown_timer,
                                   make_maha)

# "Maha has a block of ice, a small heater, and a timer. The block must
#  be fully water exactly when the timer ends."
DUR = 9.6


class ThermalbudgetS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rig = ice_on_heater([-1.2, -0.4, 0], scale=1.0, heat=0.0,
                             melt=0.0)
        self.play(FadeIn(rig.heater, shift=UP * 0.2), run_time=1.2)
        self.play(FadeIn(rig.ice, shift=UP * 0.2), run_time=1.4)

        tmr = countdown_timer([2.6, 0.2, 0], scale=0.95, frac=1.0,
                              label="timer")
        self.play(FadeIn(tmr), run_time=1.2)

        maha = make_maha([-4.4, -0.5, 0], scale=0.95)
        self.play(FadeIn(maha, shift=UP * 0.15), run_time=1.0)
        self.wait(DUR - 4.8)
