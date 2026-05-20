from manim import *
import numpy as np
from collisions_helpers import (steel_ball, energy_bar, make_energy_fill,
                                title)

# "The steel balls kept almost all their motion energy.
#  We call that an elastic collision."
DUR = 7.40


class CollisionsS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        before = energy_bar([-3.6, -0.2, 0], frac=0.92,
                            label="before")
        after = energy_bar([-1.2, -0.2, 0], frac=0.01,
                           label="after")
        self.add(before, after)
        s1 = steel_ball([2.0, 1.6, 0], r=0.38)
        s2 = steel_ball([3.4, 1.6, 0], r=0.38)
        self.play(FadeIn(before), FadeIn(s1), FadeIn(s2), run_time=0.9)

        grown = make_energy_fill(after, 0.86)
        self.play(Transform(after[1], grown),
                  s1.animate.shift(LEFT * 0.7),
                  s2.animate.shift(RIGHT * 0.7),
                  run_time=1.3, rate_func=rate_functions.ease_out_quad)
        lbl = title("elastic", [2.7, -0.6, 0], size=44, color="#7FC27F")
        self.play(Write(lbl), run_time=0.9)
        self.play(lbl.animate.scale(1.08), run_time=0.5,
                  rate_func=there_and_back)
        self.wait(DUR - 4.5)
