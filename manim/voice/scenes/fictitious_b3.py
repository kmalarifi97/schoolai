from manim import *
import numpy as np
from fictitious_helpers import top_down_car, curve_path, frame_label

# "But step outside the car. Watch from above, from the still ground."
DUR = 5.8


class FictitiousS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # start "close" (big car), then pull back to a fixed overhead view
        car = top_down_car([0, -0.2, 0], scale=1.6, angle=-0.3)
        self.add(car)
        self.wait(0.6)

        road = curve_path([-5.0, -2.6, 0], [3.6, 2.4, 0], bend=-2.6)
        self.play(car.animate.scale(0.40).move_to([-2.4, -1.4, 0]),
                  Create(road), run_time=1.8,
                  rate_func=rate_functions.ease_in_out_sine)
        lbl = frame_label("overhead — the still ground", [0, -3.2, 0],
                          size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 4.3)
