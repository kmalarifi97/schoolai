from manim import *
import numpy as np
from fictitious_helpers import (top_down_car, outward_arrow, frame_label,
                                big_label, FORCE_COL)

# "That invented push has a name we use anyway, because it's useful
#  inside the turning frame. The centrifugal force."
DUR = 10.4


class FictitiousS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        car = top_down_car([-0.8, 0.2, 0], scale=1.15, angle=0.0)
        self.add(car)
        self.wait(0.5)

        arr = outward_arrow([0.1, 0.4, 0], [2.2, 0, 0])
        self.play(GrowArrow(arr), run_time=1.0)

        name = big_label("centrifugal force", [0, -2.4, 0],
                         color=FORCE_COL, size=44)
        sub = frame_label("only in the rotating frame", [0, -3.1, 0],
                          size=24)
        self.play(Write(name), run_time=1.4)
        self.play(FadeIn(sub), run_time=0.9)
        self.play(arr.animate.set_stroke(width=8), run_time=0.9,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 5.7)
