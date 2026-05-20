from manim import *
import numpy as np
from heattransfer_helpers import (make_spoon, make_pot_on_flame,
                                  convection_loop, make_sun_void,
                                  make_earth, radiation_rays,
                                  small_label, heat_tint)

# "Which path dominates where, and how fast each moves heat — that's
#  the thinking we hand to you."
DUR = 8.3


class HeattransferS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        sp, handle = make_spoon([-3.5, 1.6, 0], [-4.6, -1.4, 0],
                                scale=0.60)
        n = len(handle)
        for i, seg in enumerate(handle):
            seg.set_color(heat_tint(0.4 + 0.6 * (1 - i / (n - 1))))

        pot, water, flame = make_pot_on_flame([0, 0.4, 0], scale=0.60)
        loop = convection_loop([0, 0.3, 0], w=1.5, h=1.0)

        sun = make_sun_void([3.0, 1.1, 0], scale=0.60)
        earth = make_earth([5.6, 0.2, 0], scale=0.52)
        rays = radiation_rays([3.5, 1.0, 0], [5.3, 0.25, 0], n=3,
                              spread=0.30, amp=0.10, cycles=5.0)

        self.add(sp, pot, flame, loop, sun, earth, rays)
        self.wait(1.0)

        q = small_label("which? how fast?", [0, -2.4, 0],
                        color="#C9A24A", size=30)
        self.play(Write(q), run_time=1.6)
        self.wait(0.8)
        hand = small_label("that's yours", [0, -3.3, 0],
                           color="#8C98A6", size=24)
        self.play(FadeIn(hand), run_time=1.2)
        self.wait(DUR - 4.6)
