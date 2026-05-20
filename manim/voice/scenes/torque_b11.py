from manim import *
import numpy as np
from torque_helpers import pivot_dot, force_arrow, rot_arrow, small_label

# "When several torques act, the rotation goes to whichever side wins
#  the sum."
DUR = 6.9


class TorqueS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([0, 0.2, 0])
        bar = Line(P + np.array([-3.4, 0, 0]), P + np.array([3.4, 0, 0]),
                   color="#C8CCD2", stroke_width=8)
        piv = VGroup(
            Triangle(color="#7E848C", fill_opacity=1, stroke_width=0)
            .scale(0.4).next_to(P, DOWN, buff=0.0),
            pivot_dot(P),
        )
        self.add(bar, piv)
        self.wait(0.5)

        # left side: small downward force far out
        lpt = P + np.array([-2.6, 0, 0])
        fl = force_arrow(lpt + np.array([0, 1.3, 0]), [0, -1.0, 0],
                         width=6)
        # right side: bigger downward force, also out -> wins
        rpt = P + np.array([2.6, 0, 0])
        fr = force_arrow(rpt + np.array([0, 1.9, 0]), [0, -1.7, 0],
                         width=9)
        self.play(GrowArrow(fl), GrowArrow(fr), run_time=1.0)
        self.add(small_label("smaller", lpt + np.array([0, -0.7, 0]),
                             size=22),
                 small_label("bigger", rpt + np.array([0, -0.7, 0]),
                             size=22))
        self.wait(0.4)

        # right wins -> bar tips clockwise
        grp = VGroup(bar, fl, fr)
        ra = rot_arrow(P, radius=1.3, start_angle=PI * 0.9,
                       sweep=-PI * 0.5, color="#7FB8E8")
        self.play(Rotate(grp, angle=-PI * 0.16, about_point=P),
                  Create(ra),
                  run_time=1.6, rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 4.5)
