from manim import *
import numpy as np
from heattransfer_helpers import (make_campfire, make_face, make_stove,
                                  radiation_rays)

# "You feel it from a campfire across the gap, and from a hot stove
#  before you ever touch it."
DUR = 8.0


class HeattransferS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fire = make_campfire([-3.6, -1.4, 0], scale=1.1)
        face = make_face([3.2, -1.0, 0], scale=1.05, facing=LEFT)
        self.play(FadeIn(fire), FadeIn(face), run_time=1.2)
        self.wait(0.4)

        rays = radiation_rays([-2.6, -0.7, 0], [2.55, -0.95, 0], n=3,
                              spread=0.5, amp=0.14, cycles=6.0)
        self.play(LaggedStart(*[Create(r) for r in rays],
                              lag_ratio=0.14, run_time=2.0))
        self.wait(0.4)

        # the glowing stove element, no contact
        stove = make_stove([0, 2.3, 0], scale=1.0)
        srays = radiation_rays([0, 2.0, 0], [0, 0.4, 0], n=3,
                               spread=0.45, amp=0.10, cycles=4.0)
        self.play(FadeIn(stove), run_time=0.9)
        self.play(LaggedStart(*[Create(r) for r in srays],
                              lag_ratio=0.14, run_time=1.4))
        self.wait(DUR - 6.3)
