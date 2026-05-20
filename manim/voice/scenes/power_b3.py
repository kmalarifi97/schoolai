from manim import *
import numpy as np
from power_helpers import value_bar, small_label, WORK_COL

# "Here's the thing. The work done was exactly the same. Same weight.
#  Same height."
DUR = 7.2


class PowerS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        h = 2.6
        wb1 = value_bar(h, width=1.1, color=WORK_COL,
                        anchor=[-2.4, -2.4, 0], label="work done")
        wb2 = value_bar(h, width=1.1, color=WORK_COL,
                        anchor=[2.4, -2.4, 0], label="work done")
        cap = small_label("the stroll", [-2.4, 1.7, 0], size=26)
        cap2 = small_label("the sprint", [2.4, 1.7, 0], size=26)
        self.play(GrowFromEdge(wb1.bar, DOWN),
                  GrowFromEdge(wb2.bar, DOWN), run_time=1.4)
        self.play(FadeIn(wb1[1]), FadeIn(wb2[1]),
                  FadeIn(cap), FadeIn(cap2), run_time=0.8)
        eq = small_label("=", [0, -1.1, 0], size=56, color=WORK_COL)
        self.play(FadeIn(eq, scale=1.3), run_time=0.7)
        self.wait(max(0.3, DUR - 3.6))
