from manim import *
import numpy as np
from angular_helpers import make_disk, hub_dot, rim_dot

# "Two children on a merry-go-round. One near the center. One out at
#  the edge."
DUR = 7.0


class AngularS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        disk = make_disk(C, radius=2.6)
        hub = hub_dot(C, radius=2.6, frac=0.30)
        rim = rim_dot(C, radius=2.6, frac=0.92)
        self.play(FadeIn(disk, scale=0.9), run_time=1.4)
        self.play(FadeIn(hub, scale=0.5), run_time=0.8)
        self.play(FadeIn(rim, scale=0.5), run_time=0.8)
        grp = VGroup(disk, hub, rim)
        self.play(Rotate(grp, angle=PI / 5, about_point=C),
                  run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 5.0)
