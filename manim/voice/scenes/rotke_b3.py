from manim import *
import numpy as np
from rotke_helpers import make_flywheel, axis_pin, question_mark

# "So does a spinning wheel carry energy of motion — or not?"
DUR = 5.6


class RotkeS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.2, 0])
        fw = make_flywheel(C, radius=1.8)
        self.add(fw, axis_pin(C, scale=1.1))
        fw.add_updater(lambda m, dt: m.rotate(-1.3 * dt, about_point=C))
        qm = question_mark(C + np.array([0, 2.9, 0]), size=80)
        self.play(FadeIn(qm, shift=DOWN * 0.3), run_time=1.0)
        self.play(qm.animate.scale(1.12), rate_func=there_and_back,
                  run_time=1.4)
        self.wait(DUR - 2.4)
        fw.clear_updaters()
