from manim import *
import numpy as np
from tempvsthermal_helpers import particle_swarm, jiggle, small_label

# "Zoom in. Heat is really the jiggling of countless particles. Always
#  moving, always bumping."
DUR = 8.1


class TempvsthermalS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ring = Circle(radius=3.0, color="#5A6E80", stroke_width=2
                      ).set_opacity(0.5)
        self.play(Create(ring), run_time=1.0)
        swarm = particle_swarm([0, 0, 0], n=24, radius=2.6, hot=False,
                               seed=5, dot_r=0.10)
        self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in swarm],
                              lag_ratio=0.03, run_time=1.6))
        self.add(small_label("countless particles, always moving",
                             [0, 3.4, 0], size=24))
        jiggle(self, swarm, amp=0.20, steps=7, run_time=DUR - 4.0, seed=5)
