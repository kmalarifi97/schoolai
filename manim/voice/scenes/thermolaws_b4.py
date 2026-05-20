from manim import *
import numpy as np
from thermolaws_helpers import balance_scale, small_label

# "So the first rule says you can't win — you can't get more energy
#  out than you put in."
DUR = 7.2


class ThermolawsS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bal = balance_scale([0, -0.2, 0], tilt=0.0, scale=1.0)
        inl = small_label("in", [-2.3, 0.7, 0], size=24, color="#E07B4C")
        outl = small_label("out", [2.3, 0.7, 0], size=24, color="#7FC8A0")
        self.play(FadeIn(bal), FadeIn(inl), FadeIn(outl), run_time=1.4)
        self.wait(0.6)
        # try to push output above input — needle won't pass parity
        bal2 = balance_scale([0, -0.2, 0], tilt=0.07, scale=1.0)
        self.play(Transform(bal, bal2), run_time=1.2)
        self.play(Transform(bal, balance_scale([0, -0.2, 0], tilt=0.0,
                                                scale=1.0)), run_time=1.0)
        cw = small_label("can't win", [0, -2.4, 0], size=30,
                         color="#EAE4D5")
        self.play(FadeIn(cw), run_time=0.8)
        self.wait(DUR - 5.0)
