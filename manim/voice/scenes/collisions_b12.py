from manim import *
import numpy as np
from collisions_helpers import (steel_ball, momentum_bar, energy_bar,
                                small_label, title)

# "Momentum always balances; energy of motion is the variable.
#  Solving each type with the right pair of rules — that's yours."
DUR = 9.42


class CollisionsS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bL = steel_ball([-3.2, 1.7, 0], r=0.34)
        bR = steel_ball([-1.4, 1.7, 0], r=0.34)
        beforeL = small_label("before", [-2.3, 0.9, 0], size=22)
        bL2 = steel_ball([1.4, 1.7, 0], r=0.34)
        bR2 = steel_ball([3.2, 1.7, 0], r=0.34)
        afterL = small_label("after", [2.3, 0.9, 0], size=22)
        arrow = Arrow([-0.6, 1.7, 0], [0.6, 1.7, 0], color="#5A6470",
                      stroke_width=4, buff=0.1)
        self.play(FadeIn(bL), FadeIn(bR), FadeIn(bL2), FadeIn(bR2),
                  GrowArrow(arrow), FadeIn(beforeL), FadeIn(afterL),
                  run_time=1.2)

        mom = momentum_bar([0, -0.2, 0], width=5.0, frac=0.6,
                           label="momentum — always balances")
        self.play(FadeIn(mom), run_time=0.9)
        eb = energy_bar([-1.0, -2.4, 0], frac=0.55, max_h=1.6,
                        label="motion energy")
        self.play(FadeIn(eb), run_time=0.9)
        var = small_label("the variable", [1.4, -2.4, 0], size=24,
                          color="#E8C24A")
        self.play(FadeIn(var), run_time=0.6)
        self.wait(DUR - 4.5)
