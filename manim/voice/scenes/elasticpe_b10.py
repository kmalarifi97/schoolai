from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, spring_mass,
                               make_bar, small_label)

# "Push too far and it won't return — the material gives, and the
#  stored energy doesn't come back."
DUR = 8.3


class ElasticpeS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wx = -4.6
        wall = wall_block([wx, 0.6, 0], h=1.6)
        spring = make_spring([wx + 0.15, 0.6, 0], [-1.6, 0.6, 0],
                             coils=10, amp=0.28)
        mass = spring_mass([-1.3, 0.6, 0], r=0.28)
        bar = make_bar([3.8, 0.6, 0], max_h=2.4, frac=0.85,
                       color="#7FB8E8", label="stored")
        self.add(wall, spring, mass, bar["group"])
        self.wait(0.6)

        # overstretched: coils pulled apart unevenly, stays slack/bent
        over = make_spring([wx + 0.15, 0.6, 0], [2.4, 0.6, 0],
                           coils=10, amp=0.10)
        over.set_stroke(color="#E08A6A")
        over_mass = spring_mass([2.7, 0.6, 0], r=0.28)
        empty = make_bar([3.8, 0.6, 0], max_h=2.4, frac=0.0,
                         color="#7FB8E8")
        self.play(Transform(spring, over),
                  Transform(mass, over_mass),
                  Transform(bar["fill"], empty["fill"]),
                  run_time=1.6, rate_func=rate_functions.ease_out_quad)
        # it does not snap back — stays deformed
        gl = small_label("doesn't return", [0.4, -1.2, 0],
                         color="#E08A6A", size=24)
        self.play(FadeIn(gl), run_time=1.0)
        self.wait(DUR - 4.8)
