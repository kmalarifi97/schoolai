from manim import *
import numpy as np
from angular_helpers import make_disk, hub_dot, rim_dot

# "Who's moving faster?"
DUR = 4.0


class AngularS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.3, 0])
        disk = make_disk(C, radius=2.6)
        hub = hub_dot(C, radius=2.6, frac=0.30)
        rim = rim_dot(C, radius=2.6, frac=0.92)
        grp = VGroup(disk, hub, rim)
        self.add(grp)
        q = Text("?", font="sans", font_size=72, color="#EAE4D5"
                 ).move_to([0, 2.8, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.8)
        self.play(Rotate(grp, angle=PI / 4, about_point=C),
                  run_time=2.0, rate_func=rate_functions.linear)
        self.wait(DUR - 2.8)
