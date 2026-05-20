from manim import *
import numpy as np
from skatepark_helpers import predict_vs_result, small_label

# "After — he explains the gap. If he said this and the bars said
#  that: which lever did he misjudge? The height? The friction?"
DUR = 10.4


class SkateparkS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        pvr = predict_vs_result([0, 0.4, 0], pred=0.42, res=0.74)
        self.play(FadeIn(pvr), run_time=1.2)
        self.wait(0.6)

        # highlight the difference
        gap = DoubleArrow(pvr[1].get_top() + UP * 0.05,
                          pvr[2].get_top() + UP * 0.05,
                          color="#D98C5F", stroke_width=4, buff=0.1,
                          tip_length=0.18)
        self.play(GrowFromCenter(gap), run_time=1.0)
        self.wait(0.5)

        # two suspects
        s1 = small_label("height?", [-2.4, -2.6, 0],
                         color="#8C8576", size=26)
        s2 = small_label("friction?", [2.4, -2.6, 0],
                         color="#8C8576", size=26)
        self.play(FadeIn(s1), FadeIn(s2), run_time=1.0)
        self.wait(DUR - 4.3)
