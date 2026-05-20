from manim import *
import numpy as np
from thermolaws_helpers import time_arrow, small_label, ENTROPY_C

# "The second rule: total entropy always increases.
#  That's why time has a direction."
DUR = 6.3


class ThermolawsS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ta = time_arrow([0, -2.4, 0], length=9.0)
        self.play(FadeIn(ta[0]), FadeIn(ta[1]), run_time=1.0)
        self.wait(0.3)
        # entropy climbs as a rising staircase along the time arrow
        xs = np.linspace(-4.0, 4.0, 7)
        pts = [np.array([x, -1.9 + 0.55 * i, 0])
               for i, x in enumerate(xs)]
        path = VGroup(*[Line(pts[i], pts[i + 1], color=ENTROPY_C,
                             stroke_width=5)
                        for i in range(len(pts) - 1)])
        elbl = small_label("total entropy", [-3.2, 1.5, 0], size=24,
                           color=ENTROPY_C)
        self.play(LaggedStart(*[Create(s) for s in path],
                              lag_ratio=0.4, run_time=2.6))
        self.play(FadeIn(elbl), run_time=0.8)
        self.wait(DUR - 4.7)
