from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             greek_label, small_label, RIM_COL)

# "And the bridge between the two worlds is the radius. Same angular
#  speed, bigger radius, faster through space."
DUR = 8.6


class AngularS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-0.6, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        spoke = rigid_spoke(C, radius=R, hub_frac=0.30, rim_frac=0.92)
        self.add(disk, hub, rim, spoke)
        self.wait(0.5)

        # radius bracket along the spoke from center to rim dot
        rline = Line(C, C + np.array([R * 0.92, 0, 0]),
                     color="#EAE4D5", stroke_width=4)
        rlbl = greek_label("r", C + np.array([R * 0.46, 0.42, 0]),
                           size=40)
        self.play(Create(rline), Write(rlbl), run_time=1.2)

        sweep = TAU * 0.7
        rim_arc = Arc(radius=R * 0.92, start_angle=0, angle=sweep,
                      arc_center=C, color=RIM_COL, stroke_width=6)
        grp = VGroup(hub, rim, spoke, rline, rlbl)
        self.play(Rotate(grp, angle=sweep, about_point=C),
                  Create(rim_arc),
                  run_time=3.0, rate_func=rate_functions.linear)
        lbl = small_label("bigger r  ->  faster through space",
                          C + np.array([0.6, -3.0, 0]),
                          color="#EAE4D5", size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.6)
