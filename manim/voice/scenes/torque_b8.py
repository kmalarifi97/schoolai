from manim import *
import numpy as np
from torque_helpers import (make_bolt, make_wrench, force_arrow,
                            line_of_action, perp_foot, lever_arm,
                            right_angle_mark, small_label)

# "The distance that actually counts isn't the whole handle — it's the
#  perpendicular distance from the pivot to where the force pushes."
DUR = 11.0


class TorqueS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = np.array([-3.0, -1.4, 0])
        ang = PI / 6  # handle tilts clearly up to the right
        bolt = make_bolt(P, radius=0.38)
        wr = make_wrench(P, length=4.6, angle=ang)
        self.add(bolt, wr)
        self.wait(0.6)

        # force applied at the handle end, pushing up & to the right
        u = np.array([np.cos(ang), np.sin(ang), 0])
        appl = P + u * (0.38 + 4.6)
        fdir = np.array([0.18, 1.0, 0]); fdir = fdir / np.linalg.norm(fdir)
        f = force_arrow(appl, fdir * 1.7, width=8)
        self.play(GrowArrow(f), run_time=1.0)

        # "the whole handle" measure, faint, then dismissed
        whole = DashedLine(P, appl, color="#5A6E80", stroke_width=3,
                           dash_length=0.12).set_opacity(0.55)
        wl = small_label("not the whole handle",
                         (P + appl) / 2 + np.array([-0.3, -0.7, 0]),
                         size=23)
        self.play(Create(whole), FadeIn(wl), run_time=1.1)
        self.wait(0.5)

        # extend the force's line of action; drop the perpendicular
        loa = line_of_action(appl, fdir, half_len=4.2)
        self.play(Create(loa), FadeOut(whole), FadeOut(wl), run_time=1.0)
        foot = perp_foot(P, appl, fdir)
        la = lever_arm(P, foot, width=8)
        ram = right_angle_mark(foot, P - foot, fdir, size=0.20)
        self.play(Create(la), Create(ram), run_time=1.2)
        # label placed below the bolt, well clear of the lever arm
        lbl = small_label("perpendicular distance",
                          P + np.array([1.6, -1.7, 0]),
                          color="#F2D74E", size=24)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 7.3)
