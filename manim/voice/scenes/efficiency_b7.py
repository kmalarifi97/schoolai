from manim import *
import numpy as np
from efficiency_helpers import percent_dial, label, USEFUL_COLOR, FAINT_LABEL

# "A perfect machine would be one hundred percent. Nothing real ever is."
DUR = 5.7


class EfficiencyS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        d = percent_dial([0, -0.4, 0], 100, scale=1.1, show_100=True)
        # start needle high (at 100), then settle below
        self.play(FadeIn(d["group"]), run_time=1.2)
        self.wait(0.6)

        # rebuild a dial resting below 100
        d2 = percent_dial([0, -0.4, 0], 82, scale=1.1, show_100=True)
        self.play(Transform(d["needle"], d2["needle"]),
                  Transform(d["value_label"], d2["value_label"]),
                  run_time=1.4)
        self.add(label("never quite there", [0, -2.5, 0], size=24,
                       color=FAINT_LABEL))
        self.wait(DUR - 3.2)
