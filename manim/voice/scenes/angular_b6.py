from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             angle_wedge, greek_label, small_label)

# "How much angle you've turned through: angular displacement."
DUR = 5.5


class AngularS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        spoke.rotate(PI / 2.2, about_point=C)
        hub = hub_dot(C, radius=R, frac=0.30).rotate(PI / 2.2,
                                                     about_point=C)
        rim = rim_dot(C, radius=R, frac=0.92).rotate(PI / 2.2,
                                                     about_point=C)
        wedge = angle_wedge(C, radius=1.5, start_ang=0.0, sweep=PI / 2.2)
        self.add(disk, wedge, spoke, hub, rim)
        self.wait(0.5)
        th = greek_label("θ", C + np.array([1.05, 1.0, 0]), size=52)
        self.play(Write(th), run_time=1.0)
        lbl = small_label("angular displacement",
                          C + np.array([0, -3.0, 0]),
                          color="#EAE4D5", size=26)
        self.play(FadeIn(lbl), run_time=1.0)
        self.wait(DUR - 3.0)
