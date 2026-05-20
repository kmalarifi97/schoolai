from manim import *
import numpy as np
from efficiency_helpers import (bar_only, split_bar, label, WORK_COLOR,
                                USEFUL_COLOR, HEAT_COLOR, FAINT_LABEL)

# "Energy is still conserved — none was destroyed. It just left the job
#  and became heat."
DUR = 7.3


class EfficiencyS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        TOT = 5.4
        LX = -2.7
        # one full input bar
        full = bar_only(0.001, [LX, 0.4, 0], color=WORK_COLOR, height=0.7)
        self.add(full)
        self.play(full.animate.become(
            bar_only(TOT, [LX, 0.4, 0], color=WORK_COLOR, height=0.7)),
            run_time=1.1)
        self.add(label("energy in", [0, 1.3, 0], size=24,
                       color=WORK_COLOR))

        # splits — nothing missing, only redirected
        sb = split_bar(TOT, [LX, 0.4, 0], 0.62, height=0.7)
        self.play(Transform(full, sb), run_time=1.4)
        self.add(label("useful", [LX + TOT * 0.31, -0.6, 0], size=22,
                       color=USEFUL_COLOR))
        self.add(label("heat", [LX + TOT * 0.81, -0.6, 0], size=22,
                       color=HEAT_COLOR))

        self.add(label("nothing destroyed — only redirected",
                       [0, -1.9, 0], size=24, color=FAINT_LABEL))
        self.wait(DUR - 3.5)
