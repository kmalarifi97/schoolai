from manim import *
import numpy as np
from tempvsthermal_helpers import make_bathtub, jiggle, small_label

# "The tub is only mildly warm — but it's a vast crowd of particles, all
#  jiggling a little."
DUR = 7.8


class TempvsthermalS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tub = make_bathtub([0, -2.3, 0], scale=1.05, steam=False)
        self.add(tub)

        # a vast, dense crowd of cool particles filling the upper field
        rng = np.random.default_rng(9)
        crowd = VGroup()
        for _ in range(150):
            x = rng.uniform(-5.6, 5.6)
            y = rng.uniform(-1.0, 3.0)
            d = Dot([x, y, 0], radius=0.055, color="#8FB8D8")
            d.set_fill("#8FB8D8", opacity=0.9)
            crowd.add(d)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in crowd],
                              lag_ratio=0.002, run_time=2.0))
        self.add(small_label("a vast crowd — each jiggling a little",
                             [0, 3.5, 0], size=24, color="#8FB8D8"))
        jiggle(self, crowd, amp=0.07, steps=5, run_time=DUR - 4.6, seed=9)
