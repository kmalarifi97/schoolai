from manim import *
import numpy as np
from fictitious_helpers import top_down_car, outward_arrow, big_label

# "It feels like a force pushed you outward. Name it, and it seems
#  real."
DUR = 6.4


class FictitiousS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        car = top_down_car([-0.6, 0, 0], scale=1.15, angle=0.0)
        self.add(car)
        self.wait(0.5)

        arr = outward_arrow([0.3, 0.2, 0], [2.0, 0, 0])
        self.play(GrowArrow(arr), run_time=0.9)
        q = big_label("?", [2.7, 0.55, 0], size=66)
        self.play(FadeIn(q, scale=0.6), run_time=0.9)
        self.play(arr.animate.set_stroke(width=8), q.animate.scale(1.12),
                  run_time=1.0, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.3)
