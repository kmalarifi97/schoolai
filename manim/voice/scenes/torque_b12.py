from manim import *
import numpy as np
from torque_helpers import (make_bolt, force_arrow, line_of_action,
                            perp_foot, lever_arm, right_angle_mark,
                            tau_label, small_label)

# "Computing the torque from a given force and distance — and finding
#  equilibrium when multiple torques act — that's yours."
DUR = 10.14


class TorqueS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-1.4, -0.4, 0])
        bolt = make_bolt(P, radius=0.40)

        fdir = np.array([0, 1.0, 0])
        appl = P + np.array([2.6, -0.2, 0])
        loa = line_of_action(appl, fdir, half_len=3.2)
        f = force_arrow(appl, [0, 1.7, 0], width=8)
        foot = perp_foot(P, appl, fdir)
        la = lever_arm(P, foot, width=8)
        ram = right_angle_mark(foot, P - foot, fdir, size=0.18)

        flbl = small_label("F", appl + np.array([0.35, 0.9, 0]),
                           color="#E8965A", size=30)
        rlbl = small_label("lever arm",
                           (P + foot) / 2 + np.array([0, -0.45, 0]),
                           color="#F2D74E", size=24)
        tau = tau_label(P + np.array([0.2, 1.7, 0]), size=52)

        self.play(FadeIn(bolt), run_time=0.8)
        self.play(Create(loa), GrowArrow(f), FadeIn(flbl), run_time=1.2)
        self.play(Create(la), Create(ram), FadeIn(rlbl), run_time=1.2)
        self.play(FadeIn(tau, scale=0.7), run_time=0.9)
        # the clean diagram holds and stills
        self.wait(DUR - 4.1)
