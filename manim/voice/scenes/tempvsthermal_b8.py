from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, particle_swarm, jiggle,
                                   small_label)

# "But there are almost none of them. A tiny flame holds very little
#  jiggling in total."
DUR = 7.5


class TempvsthermalS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([0, -0.4, 0], scale=1.1)
        swarm = particle_swarm([0, 1.7, 0], n=7, radius=0.55,
                               hot=True, seed=8, dot_r=0.12)
        self.add(match, swarm)
        jiggle(self, swarm, amp=0.30, steps=3, run_time=1.4, seed=8)

        # zoom out: everything shrinks, the handful looks sparse
        grp = VGroup(match, swarm)
        self.play(grp.animate.scale(0.42).move_to([0, -0.2, 0]),
                  run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
        self.add(small_label("just a sparse handful — little in total",
                             [0, 2.6, 0], size=24, color="#FF7A3C"))
        self.wait(DUR - 5.4)
