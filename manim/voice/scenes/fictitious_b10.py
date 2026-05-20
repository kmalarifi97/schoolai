from manim import *
import numpy as np
from fictitious_helpers import (rotating_disk, big_label, frame_label,
                                PATH_COL)

# "That apparent deflection has a name. The Coriolis effect — the
#  signature of doing physics on a turning floor."
DUR = 8.6


class FictitiousS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0.3, 0])
        R = 2.1
        disk = rotating_disk(C, radius=R, n_spokes=8)
        self.add(disk)

        # the curved disk-frame path
        omega = PI * 0.7
        pts = []
        for k in range(61):
            a = k / 60.0
            th = -omega * a
            p = np.array([0, R * a, 0])
            x = p[0] * np.cos(th) - p[1] * np.sin(th)
            y = p[0] * np.sin(th) + p[1] * np.cos(th)
            pts.append(C + np.array([x, y, 0]))
        curve = VMobject().set_points_smoothly(pts)
        curve.set_stroke(color=PATH_COL, width=5)
        self.play(Create(curve), run_time=1.8)

        name = big_label("Coriolis effect", [0, -2.6, 0],
                         color=PATH_COL, size=44)
        sub = frame_label("physics on a turning floor", [0, -3.3, 0],
                          size=23)
        self.play(Write(name), run_time=1.4)
        self.play(FadeIn(sub), run_time=0.9)
        self.wait(DUR - 4.6)
