from manim import *
import numpy as np
from efficiency_helpers import (work_bar, bar_only, label,
                                WORK_COLOR, USEFUL_COLOR, FAINT_LABEL)

# "So a machine has two stories. The work you hoped for. And the work you
#  actually got."
DUR = 6.7


class EfficiencyS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # ideal output: tall
        ideal = bar_only(0.001, [-3.6, 1.0, 0], color=WORK_COLOR,
                         height=0.7)
        self.add(ideal)
        self.play(ideal.animate.become(
            bar_only(3.4, [-3.6, 1.0, 0], color=WORK_COLOR, height=0.7)),
            run_time=1.3)
        self.add(label("work you hoped for", [-1.9, 1.75, 0], size=24,
                       color=WORK_COLOR))

        # real output: shorter
        real = bar_only(0.001, [-3.6, -1.0, 0], color=USEFUL_COLOR,
                        height=0.7)
        self.add(real)
        self.play(real.animate.become(
            bar_only(2.1, [-3.6, -1.0, 0], color=USEFUL_COLOR, height=0.7)),
            run_time=1.3)
        self.add(label("work you actually got", [-1.6, -1.75, 0], size=24,
                       color=USEFUL_COLOR))

        self.add(label("two stories", [3.7, 0, 0], size=26,
                       color=FAINT_LABEL))
        self.wait(DUR - 2.6)
