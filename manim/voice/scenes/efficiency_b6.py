from manim import *
import numpy as np
from efficiency_helpers import (bar_only, label, WORK_COLOR, USEFUL_COLOR,
                                LABEL_COL)

# "The ratio of what you got to what you put in — that's efficiency."
DUR = 5.7


class EfficiencyS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        got = bar_only(2.1, [-3.4, 0.85, 0], color=USEFUL_COLOR, height=0.6)
        put = bar_only(3.4, [-3.4, -0.85, 0], color=WORK_COLOR, height=0.6)
        self.play(GrowFromEdge(got, LEFT), GrowFromEdge(put, LEFT),
                  run_time=1.2)
        self.add(label("what you got", [-1.4, 0.85, 0], size=22,
                       color=USEFUL_COLOR))
        self.add(label("what you put in", [-1.0, -0.85, 0], size=22,
                       color=WORK_COLOR))

        frac = Line([0.6, 0.0, 0], [2.2, 0.0, 0],
                    stroke_color=LABEL_COL, stroke_width=3)
        self.play(Create(frac), run_time=0.6)
        eff = label("= efficiency", [4.1, 0.0, 0], size=30,
                    color=USEFUL_COLOR)
        self.play(Write(eff), run_time=1.2)
        self.wait(DUR - 3.0)
