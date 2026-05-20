from manim import *
import numpy as np
from power_helpers import (value_bar, time_bar, big_label, small_label,
                           WORK_COL, TIME_COL, POWER_COL)

# "Work divided by the time it took. That's power."
DUR = 4.9


class PowerS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wb = value_bar(1.4, width=2.6, color=WORK_COL,
                       anchor=[-1.3, 0.5, 0])
        wlbl = small_label("work", [0, 1.55, 0], size=28, color=WORK_COL)
        tb = time_bar(2.6, height=0.5, color=TIME_COL,
                      anchor=[-1.3, -0.3, 0])
        tlbl = small_label("time", [0, -0.95, 0], size=28, color=TIME_COL)
        bar = Line([-1.5, 0.1, 0], [1.5, 0.1, 0], color="#EAE4D5",
                   stroke_width=4)
        self.play(FadeIn(wb), FadeIn(wlbl), run_time=0.7)
        self.play(Create(bar), run_time=0.4)
        self.play(FadeIn(tb), FadeIn(tlbl), run_time=0.7)
        self.wait(0.4)

        grp = VGroup(wb, wlbl, tb, tlbl, bar)
        plabel = big_label("power", [0, 0.0, 0], size=64, color=POWER_COL)
        self.play(FadeOut(grp, scale=0.7),
                  FadeIn(plabel, scale=1.2), run_time=1.0)
        self.wait(max(0.3, DUR - 3.6))
