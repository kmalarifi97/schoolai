from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             angle_wedge, greek_label, small_label)

# "How fast that angle grows: angular velocity. Measured the same for
#  every point on the disk."
DUR = 8.4


class AngularS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        wedge = angle_wedge(C, radius=1.5, start_ang=0.0, sweep=0.001)
        self.add(disk, wedge, spoke, hub, rim)
        om = greek_label("ω", C + np.array([0, 3.0, 0]), size=52)
        self.play(Write(om), run_time=0.9)

        total = TAU * 0.75
        grp = VGroup(hub, rim, spoke)
        self.play(
            Rotate(grp, angle=total, about_point=C),
            UpdateFromAlphaFunc(
                wedge,
                lambda m, a: m.become(
                    angle_wedge(
                        C, radius=1.5,
                        start_ang=(a * total) % TAU - PI / 2.5,
                        sweep=PI / 2.5))),
            run_time=4.0, rate_func=rate_functions.linear)
        lbl = small_label("same ω for every point",
                          C + np.array([0, -3.0, 0]),
                          color="#EAE4D5", size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.8)
