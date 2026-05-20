from manim import *
import numpy as np
from torque_helpers import make_bolt, force_arrow, small_label

# "Turning depends on three things together: how hard, how far from the
#  pivot, and which way."
DUR = 7.98


class TorqueS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # three small icons across the frame
        # 1) how hard — a force arrow
        c1 = np.array([-4.0, 0.4, 0])
        a1 = force_arrow(c1 + np.array([0, -0.8, 0]), [0, 1.6, 0], width=9)
        l1 = small_label("how hard", c1 + np.array([0, -1.5, 0]), size=24)

        # 2) how far — a distance bracket from a pivot
        c2 = np.array([0.0, 0.4, 0])
        piv = make_bolt(c2 + np.array([-1.3, 0, 0]), radius=0.22)
        dist = DoubleArrow(c2 + np.array([-1.3, -0.8, 0]),
                           c2 + np.array([1.3, -0.8, 0]),
                           color="#C8CCD2", stroke_width=4,
                           buff=0, tip_length=0.18)
        l2 = small_label("how far", c2 + np.array([0, -1.5, 0]), size=24)

        # 3) which way — an angle
        c3 = np.array([4.0, 0.0, 0])
        base = Line(c3, c3 + np.array([1.1, 0, 0]),
                    color="#C8CCD2", stroke_width=4)
        ray = Line(c3, c3 + np.array([0.85, 0.85, 0]),
                   color="#E8965A", stroke_width=4)
        arc = Arc(radius=0.45, start_angle=0, angle=PI / 4,
                  arc_center=c3, color="#7FB8E8", stroke_width=3)
        l3 = small_label("which way", c3 + np.array([0, -1.1, 0]), size=24)

        self.play(GrowArrow(a1), FadeIn(l1), run_time=1.0)
        self.play(FadeIn(piv), GrowArrow(dist), FadeIn(l2), run_time=1.0)
        self.play(Create(base), Create(ray), Create(arc), FadeIn(l3),
                  run_time=1.0)
        self.wait(DUR - 4.2)
