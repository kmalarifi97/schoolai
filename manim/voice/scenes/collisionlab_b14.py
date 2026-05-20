from manim import *
import numpy as np
from collisionlab_helpers import (cl_track, cl_puck, momentum_arrow,
                                  play_button, small_label)

# "Here is the real job. Not pressing play. Predicting — before she
#  does."
DUR = 6.5


class CollisionlabS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tr = cl_track([0, 0.6, 0], w=6.8)
        p1 = cl_puck([-2.2, 0.6, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([1.8, 0.6, 0], color="#E8C46B", mass="1")
        # arrows frozen at start
        a1 = momentum_arrow([-2.2, 0.6, 0], 0.9, color="#E8C46B")
        self.add(tr, p1, p2, a1)

        pb = play_button([0, -2.0, 0], r=0.5)
        self.play(FadeIn(pb), run_time=0.8)
        # a finger hovers, deliberately not pressing
        finger = Arrow([1.4, -2.0, 0], [0.55, -2.0, 0],
                       color="#EAE4D5", stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(finger), run_time=1.0)
        self.play(finger.animate.shift(RIGHT * 0.25), run_time=1.0,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 2.8)
