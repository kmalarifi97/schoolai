from manim import *
import numpy as np
from efficiency_helpers import (bar_only, label, WORK_COLOR, USEFUL_COLOR,
                                LABEL_COL, FAINT_LABEL)

# "Computing efficiency as useful output over total input, and the work
#  lost to friction in a real machine — that's yours."
DUR = 9.0


class EfficiencyS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        useful = bar_only(2.0, [-2.0, 0.95, 0], color=USEFUL_COLOR,
                          height=0.55)
        total = bar_only(3.4, [-2.0, -0.95, 0], color=WORK_COLOR,
                         height=0.55)
        self.play(GrowFromEdge(useful, LEFT),
                  GrowFromEdge(total, LEFT), run_time=1.2)
        self.add(label("useful output", [0.4, 0.95, 0], size=22,
                       color=USEFUL_COLOR))
        self.add(label("total input", [0.0, -0.95, 0], size=22,
                       color=WORK_COLOR))

        frac = Line([-3.2, 0.0, 0], [-1.4, 0.0, 0],
                    stroke_color=LABEL_COL, stroke_width=3)
        self.play(Create(frac), run_time=0.6)
        eq = label("efficiency =", [-4.6, 0.0, 0], size=26,
                   color=LABEL_COL)
        self.play(Write(eq), run_time=1.0)

        hold = label("values left open — that's yours", [0, -2.5, 0],
                     size=24, color=FAINT_LABEL)
        self.play(FadeIn(hold), run_time=1.2)
        # holds
        self.wait(DUR - 4.0)
