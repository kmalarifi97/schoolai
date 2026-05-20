from manim import *
import numpy as np
from fictitious_helpers import rotating_disk, frame_label, BALL_COL

# "Now a harder one. Stand at the center of a spinning platform and
#  roll a ball straight to a friend at the edge."
DUR = 9.6


class FictitiousS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.2, 0])
        disk = rotating_disk(C, radius=2.7, n_spokes=8)
        self.play(FadeIn(disk, scale=0.85), run_time=1.2)

        # the thrower at center, the friend at the edge
        thrower = Dot(point=C, radius=0.16, color=BALL_COL)
        friend = Dot(point=C + np.array([2.55, 0, 0]), radius=0.18,
                     color="#E8C46A")
        fl = frame_label("friend", C + np.array([2.55, 0.55, 0]),
                         size=22)
        self.play(FadeIn(thrower), FadeIn(friend), FadeIn(fl),
                  run_time=1.0)

        # slow rotation begins
        self.play(Rotate(disk, angle=PI * 0.6, about_point=C),
                  run_time=2.6, rate_func=rate_functions.linear)
        self.wait(DUR - 4.8)
