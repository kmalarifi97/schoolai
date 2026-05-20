from manim import *
import numpy as np
from power_helpers import (stick_figure, value_bar, small_label,
                           WORK_COL, FIG_COL)

# "Same work — but the sprint nearly killed you and the stroll didn't.
#  Work alone doesn't capture that."
DUR = 8.7


class PowerS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        calm = stick_figure("stand", scale=1.0).move_to([-3.4, 1.4, 0])
        coll = stick_figure("collapse", scale=1.0).move_to([3.0, 1.2, 0])
        c1 = small_label("calm", [-3.4, 0.2, 0], size=24)
        c2 = small_label("wrecked", [3.2, 0.2, 0], size=24)
        self.play(FadeIn(calm), FadeIn(coll), run_time=1.0)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.6)

        h = 1.7
        wb1 = value_bar(h, width=0.9, color=WORK_COL,
                        anchor=[-2.4, -3.0, 0], label="work")
        wb2 = value_bar(h, width=0.9, color=WORK_COL,
                        anchor=[2.4, -3.0, 0], label="work")
        eq = small_label("=", [0, -2.0, 0], size=44, color=WORK_COL)
        self.play(GrowFromEdge(wb1.bar, DOWN), GrowFromEdge(wb2.bar, DOWN),
                  run_time=1.0)
        self.play(FadeIn(wb1[1]), FadeIn(wb2[1]), FadeIn(eq), run_time=0.6)

        q = small_label("?", [0, 1.0, 0], size=72, color=FIG_COL)
        self.play(FadeIn(q, scale=1.4), run_time=0.8)
        self.wait(max(0.3, DUR - 5.0))
