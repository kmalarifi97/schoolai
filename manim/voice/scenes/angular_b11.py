from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             greek_label, small_label, RIM_COL, HUB_COL)

# "So the child at the edge really is faster — and yet they turn at the
#  very same rate. No contradiction."
DUR = 7.8


class AngularS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        self.add(disk, hub, rim, spoke)

        rg = Circle(radius=0.30, color=RIM_COL, stroke_width=3,
                    fill_opacity=0).move_to(rim.get_center())
        hg = Circle(radius=0.30, color=HUB_COL, stroke_width=3,
                    fill_opacity=0).move_to(hub.get_center())
        om = greek_label("ω", C + np.array([0, 3.0, 0]), size=48)
        self.play(Create(rg), Create(hg), Write(om), run_time=1.0)

        grp = VGroup(hub, rim, spoke, rg, hg)
        self.play(Rotate(grp, angle=TAU * 0.7, about_point=C),
                  run_time=3.2, rate_func=rate_functions.linear)
        lbl = small_label("faster — same rate. no contradiction.",
                          C + np.array([0, -3.0, 0]),
                          color="#EAE4D5", size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.1)
