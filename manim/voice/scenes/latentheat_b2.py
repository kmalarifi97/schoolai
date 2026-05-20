from manim import *
import numpy as np
from latentheat_helpers import (make_glass, make_flame, make_thermometer,
                                energy_arrows, small_label)

# "You're pouring energy in steadily. But while ice remains, the
#  temperature does not budge. Zero. Still zero."
DUR = 9.3


class LatentheatS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        glass = make_glass([-1.4, 0.7, 0], scale=1.0, ice_frac=1.0)
        flame = make_flame([-1.4, -1.9, 0], scale=1.0)
        therm = make_thermometer([2.4, 0.4, 0], scale=1.0, level=0.0)
        self.add(glass, flame, therm)

        arrows = energy_arrows([-1.4, 0.7, 0], n=5, length=0.7,
                               spread=1.4, y=-2.7)
        # steady pulses of energy going up into the glass base
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.12, run_time=1.6))
        for _ in range(2):
            self.play(arrows.animate.shift(UP * 0.18), run_time=0.5)
            self.play(arrows.animate.shift(DOWN * 0.18), run_time=0.5)

        zero = small_label("0°", [3.5, 0.4, 0], color="#E8615A",
                           size=40)
        self.play(FadeIn(zero), run_time=0.8)
        self.wait(DUR - 5.4)
