from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             greek_label, small_label)

# "Speed it up — the angle grows faster and faster. That change is
#  angular acceleration."
DUR = 7.8


class AngularS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        self.add(disk, hub, rim, spoke)
        al = greek_label("α", C + np.array([0, 3.0, 0]), size=52)
        self.play(Write(al), run_time=0.8)

        grp = VGroup(hub, rim, spoke)
        # accelerating spin: rate_func ramps speed up
        self.play(Rotate(grp, angle=TAU * 2.4, about_point=C),
                  run_time=4.2,
                  rate_func=rate_functions.rush_into)
        lbl = small_label("angular acceleration",
                          C + np.array([0, -3.0, 0]),
                          color="#EAE4D5", size=26)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.9)
