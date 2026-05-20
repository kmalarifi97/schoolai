from manim import *
import numpy as np
from skatepark_helpers import friction_slider, run_counter

# "He adjusts the friction. Predicts again. Three runs. That's all he
#  gets."
DUR = 6.7


class SkateparkS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fs = friction_slider([0, 1.0, 0], frac=0.65, w=3.4)
        self.play(FadeIn(fs), run_time=1.0)
        # nudge the slider deliberately
        target = fs.rail.get_left() + RIGHT * 3.4 * 0.4
        self.play(fs.knob.animate.move_to(
            [target[0], fs.knob.get_center()[1], 0]), run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        rc = run_counter([0, -1.6, 0], used=0, total=3)
        self.play(FadeIn(rc), run_time=1.0)
        self.wait(DUR - 3.9)
