from manim import *
import numpy as np
from workenergy_helpers import (force_arrow, displacement_arrow,
                                small_label, big_label)

# "Work isn't effort. Work isn't being tired. Work is a force that
#  actually moves something along its direction."
DUR = 9.6


class WorkenergyS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        n1 = small_label("not effort", [-3.4, 2.2, 0],
                         color="#8C98A6", size=30)
        n2 = small_label("not being tired", [-3.4, 1.5, 0],
                         color="#8C98A6", size=30)
        self.play(FadeIn(n1, run_time=0.7))
        self.play(FadeIn(n2, run_time=0.7))
        self.wait(0.6)
        self.play(n1.animate.set_opacity(0.25),
                  n2.animate.set_opacity(0.25), run_time=0.6)

        fa = force_arrow([-2.4, -0.2, 0], length=2.4, direction=RIGHT,
                         label="force")
        da = displacement_arrow([-2.4, -1.1, 0], length=2.4,
                                direction=RIGHT, label="moves this way")
        self.play(GrowArrow(fa[0]), FadeIn(fa[1]), run_time=1.0)
        self.play(GrowArrow(da[0]), FadeIn(da[1]), run_time=1.0)
        self.wait(0.5)
        prod = big_label("force, along its direction", [0, 1.4, 0],
                         color="#9CC97F", size=32)
        self.play(FadeIn(prod, run_time=1.0))
        self.wait(DUR - 6.8)
