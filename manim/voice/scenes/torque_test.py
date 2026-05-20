from manim import *
import numpy as np
from torque_helpers import (make_bolt, pivot_dot, make_wrench, force_arrow,
                            rot_arrow, line_of_action, perp_foot, lever_arm,
                            right_angle_mark, make_door_topdown, tau_label,
                            small_label)


class TorqueTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-4.0, 1.6, 0])
        bolt = make_bolt(P)
        wr = make_wrench(P, length=2.2, angle=0.0)
        f = force_arrow(P + np.array([2.5, 0, 0]), [0, 1.1, 0])
        ra = rot_arrow(P, radius=0.9)
        self.add(bolt, wr, f, ra)

        # lever arm demo
        Q = np.array([1.6, 1.6, 0])
        boltQ = make_bolt(Q)
        appl = Q + np.array([2.2, 0.6, 0])
        fdir = np.array([0.3, 1.0, 0])
        loa = line_of_action(appl, fdir)
        fa = force_arrow(appl, fdir * 1.2)
        foot = perp_foot(Q, appl, fdir)
        la = lever_arm(Q, foot)
        ram = right_angle_mark(foot, Q - foot, fdir)
        self.add(boltQ, loa, fa, la, ram)
        self.add(small_label("lever arm", (Q + foot) / 2 + np.array([-0.2, -0.4, 0])))

        # door top-down
        H = np.array([-3.0, -2.0, 0])
        door = make_door_topdown(H, length=3.0, angle=0.5)
        self.add(door, small_label("door (top-down)", H + np.array([1.6, -0.7, 0])))

        self.add(tau_label([3.6, -1.8, 0]))
        self.wait(0.4)
