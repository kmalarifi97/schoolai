from manim import *
import numpy as np
from thermalbudget_helpers import target_dotted, small_label

# "One goal. Not melted early. Not still icy at the end. Done, right on
#  the buzzer."
DUR = 7.3


class ThermalbudgetS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        goal = small_label("one goal", [0, 1.7, 0], color="#EAE4D5",
                           size=30)
        self.play(Write(goal), run_time=1.0)

        tg = target_dotted([0, 0.0, 0], scale=1.1)
        self.play(FadeIn(tg[1:], shift=UP * 0.1), run_time=1.0)
        self.play(Create(tg[0]), run_time=1.4)
        self.wait(DUR - 3.4)
