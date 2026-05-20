from manim import *
import numpy as np
from rotke_helpers import (axis_pin, rim_element, speed_zero_tag,
                           small_label)

# "Look closer. The center is still — but every other bit of the disk
#  is racing in a circle."
DUR = 7.9


class RotkeS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -0.2, 0])
        R = 2.2
        ring = Circle(radius=R, stroke_color="#7FB8E8", stroke_width=2.5,
                      fill_opacity=0).move_to(C)
        self.play(Create(ring), FadeIn(axis_pin(C, scale=1.2)),
                  run_time=1.0)

        n = 8
        elems = VGroup(*[rim_element(TAU * k / n, C, R) for k in range(n)])
        self.play(LaggedStart(*[FadeIn(e, scale=0.5) for e in elems],
                              lag_ratio=0.06, run_time=1.0))

        tag = speed_zero_tag(C)
        self.play(FadeIn(tag), run_time=0.8)
        self.add(small_label("racing in a circle",
                             C + np.array([0, -R - 0.55, 0]),
                             size=24, color="#8C98A6"))

        # the rim elements race around; center tag stays put
        grp = VGroup(ring, elems)
        grp.add_updater(lambda m, dt: m.rotate(-1.6 * dt, about_point=C))
        self.wait(DUR - 2.8)
        grp.clear_updaters()
