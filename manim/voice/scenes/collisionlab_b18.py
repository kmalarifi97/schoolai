from manim import *
import numpy as np
from collisionlab_helpers import mass_slider, run_counter, cl_puck

# "She adjusts a mass. Predicts again. Three runs. That's all she
#  gets."
DUR = 6.4


class CollisionlabS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        p1 = cl_puck([-2.4, 1.4, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([1.4, 1.4, 0], color="#E8C46B", mass="1")
        self.add(p1, p2)

        ms = mass_slider([-2.4, -0.6, 0], frac=0.4, w=2.8,
                         label="mass")
        self.play(FadeIn(ms), run_time=0.8)
        # nudge the slider deliberately
        self.play(ms.knob.animate.move_to(
            ms.rail.get_left() + RIGHT * 2.8 * 0.7),
            p1[0].animate.scale(1.15), run_time=1.2,
            rate_func=rate_functions.ease_in_out_sine)

        rc = run_counter([2.4, -0.6, 0], used=0, total=3)
        self.play(FadeIn(rc), run_time=1.0)
        self.wait(DUR - 3.0)
