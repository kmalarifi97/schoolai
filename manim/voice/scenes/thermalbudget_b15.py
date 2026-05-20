from manim import *
import numpy as np
from thermalbudget_helpers import (countdown_timer, small_label,
                                   heat_rate_control)

# "What heat rate makes the temperature cost plus the hidden melt cost
#  finish exactly when the timer hits zero?"
DUR = 9.3


class ThermalbudgetS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hr = heat_rate_control([-3.0, 1.6, 0], frac=0.5, w=2.4,
                               label="heat rate = ?")
        self.play(FadeIn(hr), run_time=1.0)

        # the small relation, sized to fit
        rel = MathTex(r"Q = mc\,\Delta T \;+\; mL",
                      color="#EAE4D5")
        rel.scale_to_fit_width(5.0).move_to([0.6, 0.6, 0])
        self.play(Write(rel), run_time=1.6)

        over = small_label("over time", [0.6, -0.4, 0],
                           color="#8C8576", size=22)
        self.play(FadeIn(over), run_time=0.8)

        tmr = countdown_timer([0.6, -2.4, 0], scale=0.7, frac=0.0,
                              label="timer = 0")
        self.play(FadeIn(tmr), run_time=1.0)
        self.wait(DUR - 5.4)
