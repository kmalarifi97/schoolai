from manim import *
import numpy as np
from angular_helpers import (make_disk, hub_dot, rim_dot, rigid_spoke,
                             angle_wedge, greek_label, small_label,
                             cascade)


class AngularTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-3.4, 0.4, 0])
        disk = make_disk(C, radius=2.0)
        hub = hub_dot(C, radius=2.0)
        rim = rim_dot(C, radius=2.0)
        spoke = rigid_spoke(C, radius=2.0)
        wedge = angle_wedge(C, radius=1.2, start_ang=0.0, sweep=PI / 2.5)
        th = greek_label("θ", C + np.array([1.0, 0.9, 0]), size=40)
        lbl = small_label("rim", C + np.array([1.9, -1.2, 0]))

        casc = cascade(("x", "v", "a"), [1.6, 1.6, 0], dx=1.6)
        casc2 = cascade(("θ", "ω", "α"), [1.6, -1.6, 0],
                        dx=1.6)

        self.add(disk, wedge, spoke, hub, rim, th, lbl, casc, casc2)
        self.wait(0.4)
