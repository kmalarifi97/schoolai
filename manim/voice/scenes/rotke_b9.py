from manim import *
import numpy as np
from rotke_helpers import mass_disk, moi_label, small_label

# "That reluctance to spin up or slow down has a name of its own —
#  the moment of inertia."
DUR = 7.7


class RotkeS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0.6, 0])
        disk = mass_disk(C, radius=1.7, at_rim=True)
        self.play(FadeIn(disk), run_time=1.0)
        disk.add_updater(lambda m, dt: m.rotate(-0.9 * dt,
                                                about_point=C))

        lbl = moi_label(C + np.array([0, -2.7, 0]), size=34)
        self.play(Write(lbl), run_time=1.4)
        sub = small_label("how the mass is spread",
                          C + np.array([0, -3.4, 0]), size=22,
                          color="#8C98A6")
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(DUR - 3.4)
        disk.clear_updaters()
