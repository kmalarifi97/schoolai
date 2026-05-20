from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, small_label,
                             RIM_COL, HUB_COL)

# "The one at the edge sweeps a huge circle. The one near the center
#  barely moves. So — different speeds."
DUR = 8.8


class AngularS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        R = 2.6
        disk = make_disk(C, radius=R)
        hub = hub_dot(C, radius=R, frac=0.30)
        rim = rim_dot(C, radius=R, frac=0.92)
        self.add(disk, hub, rim)
        self.wait(0.5)

        sweep = PI * 0.9
        rim_arc = Arc(radius=R * 0.92, start_angle=0, angle=sweep,
                      arc_center=C, color=RIM_COL, stroke_width=6)
        hub_arc = Arc(radius=R * 0.30, start_angle=0, angle=sweep,
                      arc_center=C, color=HUB_COL, stroke_width=6)

        self.play(Rotate(VGroup(disk, hub, rim), angle=sweep,
                          about_point=C),
                  Create(rim_arc), Create(hub_arc),
                  run_time=3.0, rate_func=rate_functions.linear)
        l1 = small_label("huge circle", C + np.array([0.2, -3.0, 0]),
                         color=RIM_COL, size=24)
        l2 = small_label("barely moves", C + np.array([-1.5, 0.6, 0]),
                         color=HUB_COL, size=22)
        self.play(FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.wait(DUR - 4.5)
