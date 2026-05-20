from manim import *
import numpy as np
from thermalbudget_helpers import (energy_ledger, thermometer,
                                   temp_energy_curve, small_label)

# "And a huge chunk pays only to change state — melting the ice — with
#  the thermometer flat the entire time."
DUR = 9.1


class ThermalbudgetS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # a big melt line-item fills up
        led = energy_ledger(
            [("hidden melt", 0.0, "#9BD6B0")],
            [-2.6, 2.0, 0], scale=1.0)
        self.play(FadeIn(led), run_time=0.9)
        led_full = energy_ledger(
            [("hidden melt", 1.0, "#9BD6B0")],
            [-2.6, 2.0, 0], scale=1.0)

        # temperature curve with its flat melting plateau
        crv = temp_energy_curve([0.4, -0.6, 0], scale=0.85,
                                progress=1.0)
        self.play(Create(crv.axes), run_time=0.9)
        self.play(Create(crv.curve), run_time=1.4)
        self.play(Create(crv.plateau_seg), run_time=1.0)

        # the thermometer stays flat at 0 the entire time the melt
        # line-item fills
        th = thermometer([4.7, -0.3, 0], scale=0.6, level=0.0)
        self.add(th)
        self.play(Transform(led, led_full), run_time=2.0)
        # thermometer deliberately does NOT move — flat at 0
        flat = small_label("flat at 0", [4.7, 2.0, 0],
                           color="#9BD6B0", size=20)
        self.play(FadeIn(flat), run_time=0.7)
        self.wait(DUR - 7.8)
