from manim import *
import numpy as np
from thermalbudget_helpers import heat_rate_control, run_counter

# "She adjusts the heat rate. Predicts again. Three tries. That's all
#  she gets."
DUR = 7.0


class ThermalbudgetS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hr = heat_rate_control([0, 1.0, 0], frac=0.65, w=3.4,
                               label="heat rate")
        self.play(FadeIn(hr), run_time=1.0)
        target = hr.rail.get_left() + RIGHT * 3.4 * 0.42
        self.play(hr.knob.animate.move_to(
            [target[0], hr.knob.get_center()[1], 0]), run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)

        rc = run_counter([0, -1.6, 0], used=0, total=3)
        self.play(FadeIn(rc), run_time=1.0)
        self.wait(DUR - 3.9)
