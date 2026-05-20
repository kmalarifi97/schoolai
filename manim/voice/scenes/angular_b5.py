from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             angle_wedge, small_label)

# "Both stories are true. We just need the right way to measure
#  turning — not distance along the ground, but angle swept."
DUR = 10.2


class AngularS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        self.add(disk, hub, rim, spoke)
        self.wait(0.6)

        sweep = PI / 2.2
        wedge = angle_wedge(C, radius=1.5, start_ang=0.0, sweep=0.001)
        self.add(wedge)
        grp = VGroup(hub, rim, spoke)

        def upd(m, dt):
            pass
        self.play(
            Rotate(grp, angle=sweep, about_point=C),
            UpdateFromAlphaFunc(
                wedge,
                lambda m, a: m.become(
                    angle_wedge(C, radius=1.5, start_ang=0.0,
                                sweep=max(0.001, a * sweep)))),
            run_time=3.0, rate_func=rate_functions.ease_in_out_sine)
        lbl = small_label("angle swept", C + np.array([1.3, 1.5, 0]),
                          color="#EAE4D5", size=26)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.5)
