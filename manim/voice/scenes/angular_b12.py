from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             angle_wedge, greek_label)

# "Angle, rate of angle, change of that rate. Computing angular
#  velocity and acceleration, then converting them to linear speed
#  through the radius — that's yours."
DUR = 12.9


class AngularS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.2, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        spoke.rotate(PI / 3, about_point=C)
        hub = hub_dot(C, radius=R, frac=0.30).rotate(PI / 3,
                                                     about_point=C)
        rim = rim_dot(C, radius=R, frac=0.92).rotate(PI / 3,
                                                     about_point=C)
        wedge = angle_wedge(C, radius=1.4, start_ang=0.0, sweep=PI / 3)
        self.play(FadeIn(disk, scale=0.92), run_time=1.0)
        self.play(FadeIn(wedge), Create(spoke),
                  FadeIn(hub), FadeIn(rim), run_time=1.2)

        th = greek_label("θ", C + np.array([1.0, 0.8, 0]), size=40)
        om = greek_label("ω", C + np.array([-2.7, 2.0, 0]), size=40)
        al = greek_label("α", C + np.array([2.7, 2.0, 0]), size=40)
        rl = greek_label("r", C + np.array([1.05, -0.55, 0]), size=36)
        self.play(LaggedStart(Write(th), Write(om), Write(al), Write(rl),
                              lag_ratio=0.4, run_time=2.4))
        # clean labeled disk holds, silent
        self.wait(DUR - 6.6)
