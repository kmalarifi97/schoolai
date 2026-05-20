from manim import *
import numpy as np
from thermalbudget_helpers import (countdown_timer, energy_ledger,
                                   small_label)

# "After — she explains the gap. Finished early? She underpaid the
#  hidden melt. Late? She overpaid the rest."
DUR = 9.1


class ThermalbudgetS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # timer-vs-done mismatch
        tmr = countdown_timer([-3.4, 1.3, 0], scale=0.7, frac=0.18,
                              label="timer")
        done = small_label("done", [-3.4, -0.7, 0], color="#5A9BD4",
                           size=24)
        gap = DashedLine([-3.4, 0.55, 0], [-3.4, -0.4, 0],
                         color="#D98C5F", stroke_width=3)
        self.play(FadeIn(tmr), FadeIn(done), run_time=1.0)
        self.play(Create(gap), run_time=0.8)
        gl = small_label("the gap", [-2.2, 0.1, 0], color="#D98C5F",
                         size=20)
        self.play(FadeIn(gl), run_time=0.6)

        led = energy_ledger(
            [("hidden melt", 0.45, "#9BD6B0"),
             ("the rest", 0.8, "#D98C5F")],
            [2.4, 0.6, 0], scale=0.9)
        self.play(FadeIn(led), run_time=1.0)
        # highlight the under/over item
        self.play(led.rows[0].animate.scale(1.08).set_opacity(1.0),
                  run_time=0.8)
        self.wait(DUR - 5.2)
