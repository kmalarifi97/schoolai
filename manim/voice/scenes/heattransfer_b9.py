from manim import *
import numpy as np
from heattransfer_helpers import (make_sun_void, make_earth,
                                  radiation_rays, small_label)

# "It came as light. Heat that travels as radiation needs no material
#  at all."
DUR = 6.8


class HeattransferS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sun = make_sun_void([-5.4, 0.4, 0], scale=1.15)
        earth = make_earth([5.3, -0.2, 0], scale=0.85)
        self.add(sun, earth)
        self.wait(0.4)

        rays = radiation_rays([-4.4, 0.4, 0], [4.85, -0.2, 0], n=4,
                              spread=0.5, amp=0.16, cycles=7.0)
        self.play(LaggedStart(*[Create(r) for r in rays],
                              lag_ratio=0.12, run_time=2.4))

        lbl = small_label("radiation — by waves", [0, -2.6, 0],
                          color="#F2C14E", size=30)
        self.play(Write(lbl), run_time=1.4)
        self.wait(DUR - 4.6)
