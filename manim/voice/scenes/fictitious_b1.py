from manim import *
import numpy as np
from fictitious_helpers import (top_down_car, curve_path, outward_arrow,
                                straight_dashed)

# "A car takes a sharp turn. You feel thrown against the door."
DUR = 5.7


class FictitiousS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        road = curve_path([-5.2, -2.4, 0], [3.4, 2.6, 0], bend=-2.6)
        self.play(Create(road), run_time=1.2)

        car = top_down_car([-4.0, -1.7, 0], scale=0.9, angle=-0.5)
        self.play(FadeIn(car), run_time=0.7)

        path = ArcBetweenPoints([-4.0, -1.7, 0], [0.7, 1.45, 0],
                                angle=-2.6)
        self.play(MoveAlongPath(car, path), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        # passenger thrown toward the door (outward, to the right)
        arr = outward_arrow([1.05, 1.45, 0], [1.15, -0.4, 0])
        self.play(GrowArrow(arr), car.animate.shift(RIGHT * 0.14),
                  run_time=0.8)
        self.wait(DUR - 4.7)
