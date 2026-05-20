from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, particle_swarm, jiggle,
                                   make_thermometer, small_label)

# "In the match flame, each particle jiggles like mad. Very high
#  temperature."
DUR = 6.8


class TempvsthermalS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([-5.0, 0.0, 0], scale=0.75)
        self.add(match)
        # a few ferocious hot particles
        swarm = particle_swarm([-0.6, 0.3, 0], n=7, radius=1.3,
                               hot=True, seed=7, dot_r=0.13)
        self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in swarm],
                              lag_ratio=0.05, run_time=1.0))
        therm = make_thermometer([4.0, -0.1, 0], scale=0.95,
                                 fill_frac=0.04)
        self.play(FadeIn(therm), run_time=0.6)
        therm_hi = make_thermometer([4.0, -0.1, 0], scale=0.95,
                                    fill_frac=0.95)
        self.play(Transform(therm, therm_hi), run_time=1.0)
        self.add(small_label("very high temperature", [0, 3.2, 0],
                             size=24, color="#FF7A3C"))
        jiggle(self, swarm, amp=0.42, steps=6, run_time=DUR - 3.6, seed=7)
