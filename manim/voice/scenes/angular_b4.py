from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             small_label, SPOKE_COL)

# "But in another sense, they move together. Same start, same finish,
#  same instant. They never separate."
DUR = 8.4


class AngularS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        self.add(disk, hub, rim)
        self.wait(0.5)
        self.play(Create(spoke), run_time=1.0)
        lbl = small_label("rigid — never separate",
                          C + np.array([0, -3.0, 0]),
                          color=SPOKE_COL, size=24)
        self.play(FadeIn(lbl), run_time=0.8)
        grp = VGroup(disk, hub, rim, spoke)
        self.play(Rotate(grp, angle=TAU * 0.6, about_point=C),
                  run_time=3.4, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 5.7)
