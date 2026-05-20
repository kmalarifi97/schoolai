from manim import *
import numpy as np
from torque_helpers import (make_bolt, force_arrow, line_of_action,
                            perp_foot, lever_arm, right_angle_mark,
                            rot_arrow, small_label)

# "That perpendicular reach has a name. The lever arm. Lengthen it, and
#  the same force turns harder."
DUR = 8.48


class TorqueS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-1.0, -0.6, 0])
        bolt = make_bolt(P, radius=0.40)
        self.add(bolt)

        # a vertical force whose line of action sits to the right;
        # lever arm is the horizontal perpendicular from P
        fdir = np.array([0, 1.0, 0])
        appl = P + np.array([2.2, -0.4, 0])
        loa = line_of_action(appl, fdir, half_len=3.4)
        f = force_arrow(appl, [0, 1.6, 0], width=8)
        foot = perp_foot(P, appl, fdir)
        la = lever_arm(P, foot, width=8)
        ram = right_angle_mark(foot, P - foot, fdir, size=0.18)
        lbl = small_label("lever arm", (P + foot) / 2 + np.array([0, -0.45, 0]),
                          color="#F2D74E", size=26)
        self.play(Create(loa), GrowArrow(f), run_time=1.1)
        self.play(Create(la), Create(ram), FadeIn(lbl), run_time=1.1)
        ra = rot_arrow(P, radius=0.7, start_angle=-PI / 5, sweep=PI * 0.55)
        self.play(Create(ra), run_time=0.7)
        self.wait(0.4)

        # lengthen the lever arm -> bigger rotation
        appl2 = P + np.array([4.0, -0.4, 0])
        loa2 = line_of_action(appl2, fdir, half_len=3.4)
        f2 = force_arrow(appl2, [0, 1.6, 0], width=8)
        foot2 = perp_foot(P, appl2, fdir)
        la2 = lever_arm(P, foot2, width=8)
        ram2 = right_angle_mark(foot2, P - foot2, fdir, size=0.18)
        lbl2 = small_label("lever arm",
                           (P + foot2) / 2 + np.array([0, -0.45, 0]),
                           color="#F2D74E", size=26)
        ra2 = rot_arrow(P, radius=1.15, start_angle=-PI / 3, sweep=PI * 1.05)
        self.play(Transform(loa, loa2), Transform(f, f2),
                  Transform(la, la2), Transform(ram, ram2),
                  Transform(lbl, lbl2), Transform(ra, ra2),
                  run_time=1.8)
        self.wait(DUR - 6.1)
