from manim import *
import numpy as np
from rotke_helpers import make_flywheel, axis_pin, small_label

# "That total is rotational kinetic energy. Energy of spin, not of
#  going anywhere."
DUR = 7.2


class RotkeS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0.3, 0])
        fw = make_flywheel(C, radius=1.7)
        self.add(fw, axis_pin(C, scale=1.1))
        fw.add_updater(lambda m, dt: m.rotate(-1.4 * dt, about_point=C))

        title = small_label("rotational kinetic energy",
                            C + np.array([0, -2.5, 0]),
                            size=34, color="#EAE4D5")
        self.play(Write(title), run_time=1.4)
        sub = small_label("energy of spin — not of going anywhere",
                          C + np.array([0, -3.2, 0]),
                          size=22, color="#8C98A6")
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(DUR - 2.4)
        fw.clear_updaters()
