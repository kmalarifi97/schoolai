from manim import *
import numpy as np
from efficiency_helpers import (winch, heat_shimmer, stream, label,
                                HEAT_COLOR, FAINT_LABEL)

# "It didn't vanish. Friction turned part of your work into heat and
#  sound. Useless for the job."
DUR = 7.4


class EfficiencyS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        w = winch([-2.4, 0.6, 0], scale=1.0)
        self.add(w["group"])

        thin = stream([-2.4, 0.6, 0], [-1.85, 0.8, 0],
                      color=HEAT_COLOR, width=3)
        heat = heat_shimmer([-1.8, 0.9, 0], n=5, spread=0.6, rise=0.9)
        self.play(GrowArrow(thin), run_time=0.5)
        self.play(LaggedStart(*[Create(s) for s in heat],
                              lag_ratio=0.12, run_time=1.1))

        lbl = label("friction  →  heat, sound", [1.6, 0.9, 0], size=26,
                    color=HEAT_COLOR)
        self.play(Write(lbl), run_time=1.4)
        sub = label("useless for the job", [1.6, 0.1, 0], size=22,
                    color=FAINT_LABEL)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(DUR - 4.0)
