from manim import *
import numpy as np
from workenergy_helpers import EnergyBar, small_label

# "So work is the accounting of energy moving in and out of motion.
#  Add it, motion grows. Remove it, motion shrinks."
DUR = 9.6


class WorkenergyS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ledger = small_label("the accounting of motion", [0, 2.9, 0],
                             color="#EAE4D5", size=30)
        self.play(FadeIn(ledger, run_time=0.8))

        bar = EnergyBar([0, -0.3, 0], height=3.4, label="motion")
        bar.set_level(0.35)
        self.add(bar)
        self.wait(0.5)

        plus = small_label("+ work", [-2.6, 0.4, 0],
                           color="#9CC97F", size=30)
        self.play(FadeIn(plus), run_time=0.5)

        def up(m, a):
            m.set_level(0.35 + 0.50 * a)
        self.play(UpdateFromAlphaFunc(bar, up), run_time=1.6)
        self.play(FadeOut(plus), run_time=0.4)
        self.wait(0.3)

        minus = small_label("− work", [-2.6, 0.4, 0],
                            color="#E05A5A", size=30)
        self.play(FadeIn(minus), run_time=0.5)

        def down(m, a):
            m.set_level(0.85 - 0.55 * a)
        self.play(UpdateFromAlphaFunc(bar, down), run_time=1.6)
        self.wait(DUR - 7.7)
