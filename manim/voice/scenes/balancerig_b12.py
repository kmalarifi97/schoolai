from manim import *
import numpy as np
from balancerig_helpers import balancing_act, level_indicator, small_label

# "Balancing Act. She places the masses at marked distances. Turns the
#  level indicator on."
DUR = 7.8


class BalancerigS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = small_label("Balancing Act", [0, 2.9, 0],
                            color="#8C8576", size=24)
        self.play(FadeIn(title), run_time=0.8)

        b = balancing_act([-0.4, -0.3, 0], half_w=3.2, bricks=[],
                          scale=1.0)
        self.play(FadeIn(b["fulcrum"]), FadeIn(b["plank"]),
                  FadeIn(b["ticks"]), run_time=1.4)

        # place the masses at marked distances
        b2 = balancing_act([-0.4, -0.3, 0], half_w=3.2,
                           bricks=[(-3, 2), (2, 3)], scale=1.0)
        self.play(FadeIn(b2["bricks"], shift=DOWN * 0.2), run_time=1.4)

        li = level_indicator([4.6, 1.4, 0], level=True, scale=0.9)
        li.set_opacity(0.0)
        self.play(li.animate.set_opacity(1.0), run_time=1.0)
        self.wait(DUR - 4.6)
