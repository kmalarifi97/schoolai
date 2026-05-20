from manim import *
import numpy as np
from rotke_helpers import (make_flywheel, axis_pin, speed_zero_tag,
                           question_mark)

# "By the usual rule, motion energy comes from a thing's speed through
#  space. This thing's center has none."
DUR = 9.0


class RotkeS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-0.6, -0.4, 0])
        fw = make_flywheel(C, radius=1.7)
        self.add(fw, axis_pin(C, scale=1.1))
        fw.add_updater(lambda m, dt: m.rotate(-1.1 * dt, about_point=C))

        tag = speed_zero_tag(C + np.array([0, 0, 0]))
        self.play(FadeIn(tag), run_time=1.2)
        self.wait(1.0)
        qm = question_mark(C + np.array([3.4, 0.6, 0]), size=72)
        self.play(Write(qm), run_time=1.0)
        self.wait(DUR - 3.2)
        fw.clear_updaters()
