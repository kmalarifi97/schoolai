from manim import *
import numpy as np
from orbitlab_helpers import (gravity_orbits_panel, make_controls,
                              closed_circle_path, small_label)

# "Gravity and Orbits. He sets the masses and the distance. Turns the
#  force arrow and the path trace on."
DUR = 8.8


class OrbitlabS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = small_label("Gravity and Orbits", [0, 3.3, 0],
                            color="#8C8576", size=22)
        self.add(title)
        panel = gravity_orbits_panel([-2.4, -0.2, 0], scale=0.9,
                                     with_trace=False)
        self.play(FadeIn(panel.star), FadeIn(panel.body),
                  run_time=1.0)
        ctrl = make_controls([3.4, -0.2, 0], scale=0.85)
        self.play(FadeIn(ctrl, shift=LEFT * 0.2), run_time=1.2)
        # nudge the sliders
        self.play(ctrl.m1.knob.animate.shift(RIGHT * 0.4),
                  ctrl.dd.knob.animate.shift(LEFT * 0.3),
                  run_time=1.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)
        # force arrow + trace switch on
        self.play(GrowArrow(panel.garrow), run_time=1.0)
        tr = closed_circle_path([-2.4, -0.2, 0], r=1.7 * 0.9,
                                color="#9BD6B0", width=3)
        tr = DashedVMobject(tr, num_dashes=40, dashed_ratio=0.5
                            ).set_stroke("#9BD6B0", width=3)
        self.play(Create(tr), run_time=1.8)
        self.wait(DUR - 7.5)
