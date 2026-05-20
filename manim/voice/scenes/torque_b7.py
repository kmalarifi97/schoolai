from manim import *
import numpy as np
from torque_helpers import force_arrow, rot_arrow, tau_label, small_label

# "Bundle them into one quantity. The turning effect of a force.
#  Torque."
DUR = 6.47


class TorqueS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # three icons drift in from their positions and merge to center
        a1 = force_arrow([-4.0, 0.4, 0], [0, 1.4, 0], width=8)
        d2 = DoubleArrow([-1.3, -1.4, 0], [1.3, -1.4, 0],
                         color="#C8CCD2", stroke_width=4, buff=0,
                         tip_length=0.18)
        ar3 = Arc(radius=0.5, start_angle=0, angle=PI / 4,
                  arc_center=[4.0, 0.2, 0], color="#7FB8E8",
                  stroke_width=4)
        self.play(GrowArrow(a1), GrowArrow(d2), Create(ar3),
                  run_time=1.0)
        self.wait(0.5)
        C = np.array([0, 0.2, 0])
        self.play(a1.animate.move_to(C).scale(0.4).set_opacity(0.0),
                  d2.animate.move_to(C).scale(0.4).set_opacity(0.0),
                  ar3.animate.move_to(C).scale(0.4).set_opacity(0.0),
                  run_time=1.3)
        ra = rot_arrow(C, radius=1.1, start_angle=-PI / 3,
                       sweep=PI * 1.1, width=9)
        self.play(Create(ra), run_time=1.1)
        tau = tau_label(C + np.array([0, 0, 0]), size=64)
        self.play(FadeIn(tau, scale=0.6), run_time=0.8)
        self.wait(DUR - 4.7)
