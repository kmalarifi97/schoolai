from manim import *
import numpy as np
from power_helpers import (value_bar, time_bar, small_label,
                           WORK_COL, TIME_COL)

# "What's different isn't how much. It's how fast. The same job,
#  packed into less time."
DUR = 7.5


class PowerS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        h = 2.3
        wb1 = value_bar(h, width=1.0, color=WORK_COL,
                        anchor=[-2.8, -0.4, 0], label="work")
        wb2 = value_bar(h, width=1.0, color=WORK_COL,
                        anchor=[2.8, -0.4, 0], label="work")
        self.play(GrowFromEdge(wb1.bar, DOWN), GrowFromEdge(wb2.bar, DOWN),
                  run_time=1.2)
        self.play(FadeIn(wb1[1]), FadeIn(wb2[1]), run_time=0.5)
        eq = small_label("same work", [0, 1.9, 0], size=28, color=WORK_COL)
        self.play(FadeIn(eq), run_time=0.6)

        # very different time widths underneath
        tb_long = time_bar(4.6, color=TIME_COL, anchor=[-5.1, -2.9, 0],
                           label="long time")
        tb_short = time_bar(1.2, color=TIME_COL, anchor=[2.3, -2.9, 0],
                            label="short time")
        self.play(GrowFromEdge(tb_long.bar, LEFT),
                  GrowFromEdge(tb_short.bar, LEFT), run_time=1.3)
        self.play(FadeIn(tb_long[1]), FadeIn(tb_short[1]), run_time=0.6)
        self.wait(max(0.3, DUR - 5.5))
