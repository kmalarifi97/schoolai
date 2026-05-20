from manim import *
import numpy as np
from skatepark_helpers import (phet_track, bar_chart_panel, play_button,
                               small_label)

# "Here is the real job. Not pressing play. Predicting — before he
#  does."
DUR = 6.5


class SkateparkS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        track = phet_track([-2.4, 0.4, 0], launch_h=1.8, scale=0.9)
        panel = bar_chart_panel([3.2, 0.6, 0], pe=0.85, ke=0.05,
                                th=0.0, scale=0.75)
        self.add(track, panel)
        pb = play_button([0, -2.4, 0], r=0.5)
        self.play(FadeIn(pb), run_time=0.8)

        # a finger (a small line) hovers, deliberately not pressing
        finger = Arrow([1.4, -2.4, 0], [0.55, -2.4, 0],
                       color="#EAE4D5", stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(finger), run_time=1.0)
        # hovers — pulls back slightly, does not press
        self.play(finger.animate.shift(RIGHT * 0.25), run_time=1.0,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 2.8)
