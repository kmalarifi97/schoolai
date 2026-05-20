from manim import *
import numpy as np
from workenergy_helpers import EnergyBar, big_label, small_label

# "That's the work–energy theorem. The net work done on a thing equals
#  the change in its energy of motion. Exactly."
DUR = 9.2


class WorkenergyS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = big_label("the work–energy theorem", [0, 3.0, 0],
                          color="#EAE4D5", size=36)
        self.play(FadeIn(title, run_time=1.0))
        self.wait(0.4)

        left = EnergyBar([-3.4, -0.6, 0], height=2.8, label="net work")
        left.set_level(0.7)
        right = EnergyBar([3.4, -0.6, 0], height=2.8,
                          label="change in motion")
        right.set_level(0.001)
        self.play(FadeIn(left), FadeIn(right.frame), FadeIn(right.caption),
                  run_time=1.0)

        eq = big_label("=", [0, 0.2, 0], color="#EAE4D5", size=60)
        self.play(FadeIn(eq), run_time=0.5)

        def fill(m, a):
            m.set_level(0.7 * a)
        self.play(UpdateFromAlphaFunc(right, fill), run_time=1.8)
        self.wait(DUR - 5.7)
