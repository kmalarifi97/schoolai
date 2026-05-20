from manim import *
import numpy as np
from efficiency_helpers import (machine_block, percent_dial, label,
                                USEFUL_COLOR, HEAT_COLOR, FAINT_LABEL)

# "A good gearbox might keep ninety. A clumsy chain of parts, far less."
DUR = 5.7


class EfficiencyS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # clean gearbox, ~90%
        m1 = machine_block([-3.6, 1.4, 0], w=1.5, h=1.5)
        d1 = percent_dial([-3.6, -1.2, 0], 90, scale=0.62,
                          color=USEFUL_COLOR, show_100=False)
        self.play(FadeIn(m1), run_time=0.8)
        self.play(FadeIn(d1["group"]), run_time=0.9)
        self.add(label("good gearbox", [-3.6, 2.6, 0], size=22,
                       color=FAINT_LABEL))

        # clumsy compound chain, far less
        m2a = machine_block([2.1, 1.4, 0], w=1.1, h=1.1)
        m2b = machine_block([3.4, 1.4, 0], w=1.1, h=1.1)
        m2c = machine_block([4.7, 1.4, 0], w=1.1, h=1.1)
        d2 = percent_dial([3.4, -1.2, 0], 48, scale=0.62,
                          color=HEAT_COLOR, show_100=False)
        self.play(FadeIn(m2a), FadeIn(m2b), FadeIn(m2c), run_time=0.9)
        self.play(FadeIn(d2["group"]), run_time=0.9)
        self.add(label("clumsy chain of parts", [3.4, 2.6, 0], size=22,
                       color=FAINT_LABEL))
        self.wait(DUR - 4.4)
