from manim import *
import numpy as np
from heattransfer_helpers import (make_spoon, make_pot_on_flame,
                                  convection_loop, make_sun_void,
                                  make_earth, radiation_rays,
                                  small_label, heat_tint)

# "Three paths for one thing. Touch. Flow. Across nothing at all."
DUR = 6.0


class HeattransferS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # left: conduction (spoon)
        sp, handle = make_spoon([-3.5, 1.7, 0], [-4.6, -1.6, 0],
                                scale=0.62)
        n = len(handle)
        for i, seg in enumerate(handle):
            seg.set_color(heat_tint(0.4 + 0.6 * (1 - i / (n - 1))))

        # middle: convection (pot loop)
        pot, water, flame = make_pot_on_flame([0, 0.4, 0], scale=0.62)
        loop = convection_loop([0, 0.3, 0], w=1.5, h=1.0)

        # right: radiation (Sun rays)
        sun = make_sun_void([3.0, 1.2, 0], scale=0.62)
        earth = make_earth([5.6, 0.2, 0], scale=0.55)
        rays = radiation_rays([3.5, 1.1, 0], [5.3, 0.25, 0], n=3,
                              spread=0.32, amp=0.10, cycles=5.0)

        self.play(FadeIn(sp), FadeIn(pot), FadeIn(flame),
                  FadeIn(sun), FadeIn(earth), run_time=1.2)
        self.play(Create(loop), *[Create(r) for r in rays],
                  run_time=1.6)

        l1 = small_label("touch", [-4.0, -2.6, 0],
                         color=heat_tint(0.8), size=24)
        l2 = small_label("flow", [0, -2.6, 0],
                         color="#E0552B", size=24)
        l3 = small_label("across nothing", [4.0, -2.6, 0],
                         color="#F2C14E", size=24)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(l3), run_time=1.2)
        self.wait(DUR - 4.0)
