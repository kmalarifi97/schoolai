from manim import *
import numpy as np
from specificheat_helpers import standing_figure, label, HOT_COL, COOL_COL
from specificheat_helpers import WATER_COL, INK

# "And it's why your own body, mostly water, holds a steady temperature
#  through a changing day."
DUR = 7.7


class SpecificheatS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fig = standing_figure([-3.4, -0.4, 0], scale=1.4, color=WATER_COL)
        lf = label("mostly water", [-3.4, -2.4, 0], size=22)
        # environment temperature curve (swings) vs body line (flat)
        ax_o = [0.3, 0.0, 0]
        env = FunctionGraph(lambda x: 1.0 * np.sin(1.4 * x),
                            x_range=[-2.6, 2.6], color=HOT_COL,
                            stroke_width=4).shift(np.array(ax_o))
        body = Line([-2.6, 0, 0], [2.6, 0, 0], color=INK,
                    stroke_width=5).shift(np.array(ax_o))
        le = label("environment", [3.4, 1.2, 0], size=20, color=HOT_COL)
        lb = label("body — steady", [3.4, 0.0, 0], size=20, color=INK)
        self.play(FadeIn(fig), FadeIn(lf), run_time=1.0)
        self.play(Create(env), FadeIn(le), run_time=1.6)
        self.play(Create(body), FadeIn(lb), run_time=1.3)
        self.wait(DUR - 3.9)
