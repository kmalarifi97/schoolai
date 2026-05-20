from manim import *
import numpy as np
from orbitlab_helpers import (gravity_orbits_panel, play_button,
                              small_label)

# "Here is the real job. Not pressing play. Predicting — before he
#  does."
DUR = 6.5


class OrbitlabS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        panel = gravity_orbits_panel([0, 0.5, 0], scale=0.9,
                                     with_trace=False)
        self.add(panel.star, panel.body, panel.garrow)
        pb = play_button([0, -2.4, 0], r=0.5)
        self.play(FadeIn(pb), run_time=0.8)
        # a finger hovers, deliberately not pressing
        finger = Arrow([1.4, -2.4, 0], [0.55, -2.4, 0],
                       color="#EAE4D5", stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(finger), run_time=1.0)
        self.play(finger.animate.shift(RIGHT * 0.25), run_time=1.2,
                  rate_func=rate_functions.there_and_back)
        lbl = small_label("predict first", [0, 2.9, 0],
                          color="#8C8576", size=24)
        self.play(FadeIn(lbl), run_time=0.7)
        self.wait(DUR - 3.7)
