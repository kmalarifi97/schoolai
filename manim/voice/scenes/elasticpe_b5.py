from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, spring_mass,
                               wants_return_arrow, small_label)

# "Elastic potential energy. The energy a material holds while it's
#  deformed and trying to spring back."
DUR = 8.7


class ElasticpeS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = wall_block([-4.4, 0.4, 0], h=1.5)
        spring = make_spring([-4.25, 0.4, 0], [1.4, 0.4, 0],
                             coils=11, amp=0.30)
        mass = spring_mass([1.7, 0.4, 0], r=0.30)
        self.play(FadeIn(wall), Create(spring), FadeIn(mass),
                  run_time=1.4)
        self.wait(0.4)
        lbl = small_label("elastic potential energy", [-1.4, 2.1, 0],
                          color="#7FB8E8", size=34)
        self.play(Write(lbl), run_time=1.3)
        wr = wants_return_arrow([1.4, -0.5, 0], [-2.2, -0.5, 0],
                                color="#7FB8E8")
        wl = small_label("wants to return", [-0.5, -1.5, 0],
                         color="#8C98A6", size=24)
        self.play(Create(wr), FadeIn(wl), run_time=1.4)
        self.wait(DUR - 4.5)
