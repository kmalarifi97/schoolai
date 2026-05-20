from manim import *
import numpy as np
from collisionlab_helpers import (make_noura, make_cart, clue_dent,
                                  small_label)

# "So she guesses from the wreck. She's sure the dented one took the
#  bigger hit, so it was the slower one."
DUR = 8.9


class CollisionlabS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        no = make_noura([-4.4, -0.3, 0], scale=1.0, facing=1)
        self.play(FadeIn(no), run_time=1.0)

        dent = clue_dent([-1.6, 0.8, 0], scale=1.3)
        self.play(FadeIn(dent), run_time=1.0)

        arrow = Arrow([-0.9, 0.8, 0], [1.4, 0.8, 0], color="#EAE4D5",
                      stroke_width=4, buff=0.1,
                      max_tip_length_to_length_ratio=0.18)
        concl = small_label("slower cart", [2.5, 0.8, 0],
                            color="#EAE4D5", size=24)
        self.play(GrowArrow(arrow), run_time=1.2)
        self.play(Write(concl), run_time=1.2)
        # she nods at her own conclusion — confident
        self.play(no[0].animate.shift(DOWN * 0.06), run_time=0.5)
        self.play(no[0].animate.shift(UP * 0.06), run_time=0.5)
        self.wait(DUR - 6.4)
