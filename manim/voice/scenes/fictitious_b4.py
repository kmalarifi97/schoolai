from manim import *
import numpy as np
from fictitious_helpers import (top_down_car, curve_path, straight_dashed,
                                frame_label, PATH_COL)

# "From out here, nothing pushed you outward. Your body simply wanted
#  to go straight — and the car turned out from under you."
DUR = 10.4


class FictitiousS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        road = curve_path([-5.0, -2.4, 0], [3.4, 2.6, 0], bend=-2.6)
        self.add(road)

        start = np.array([-4.0, -1.7, 0])
        car = top_down_car(start, scale=0.62, angle=-0.5)
        self.play(FadeIn(car), run_time=0.7)

        # the car follows the curve
        car_path = ArcBetweenPoints(start, [1.6, 1.7, 0], angle=-2.6)
        # the body's straight-line tendency: a tangent dashed line
        tang_end = start + np.array([5.6, 2.6, 0])
        tang = straight_dashed(start, tang_end)
        self.play(MoveAlongPath(car, car_path), Create(tang),
                  run_time=2.6, rate_func=rate_functions.linear)

        lbl = frame_label("the body wants to go straight",
                          [1.0, -3.2, 0], color=PATH_COL, size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.2)
