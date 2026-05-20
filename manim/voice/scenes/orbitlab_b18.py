from manim import *
import numpy as np
from orbitlab_helpers import velocity_control, run_counter

# "He adjusts the speed. Predicts again. Three runs. That's all he
#  gets."
DUR = 6.5


class OrbitlabS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        vc = velocity_control([0, 1.0, 0], frac=0.35, w=3.4)
        self.play(FadeIn(vc), run_time=1.0)
        # nudge the speed control deliberately
        target = vc.rail.get_left() + RIGHT * 3.4 * 0.55
        self.play(vc.knob.animate.move_to(
            [target[0], vc.knob.get_center()[1], 0]), run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.5)
        rc = run_counter([0, -1.6, 0], used=0, total=3)
        self.play(FadeIn(rc), run_time=1.0)
        self.wait(DUR - 3.9)
