from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, bent_beam,
                               small_label)

# "Energy stored not by height — but by shape. By stretch, by squeeze,
#  by bend."
DUR = 7.0


class ElasticpeS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # stretched spring (left)
        w1 = wall_block([-5.2, 1.3, 0], h=1.1)
        s1 = make_spring([-5.05, 1.3, 0], [-3.2, 1.3, 0], coils=9, amp=0.26)
        l1 = small_label("stretch", [-4.1, -0.0, 0], size=24)

        # compressed spring (mid)
        w2 = wall_block([-1.7, 1.3, 0], h=1.1)
        s2 = make_spring([-1.55, 1.3, 0], [-0.4, 1.3, 0], coils=9, amp=0.20)
        l2 = small_label("squeeze", [-1.0, -0.0, 0], size=24)

        # bent ruler (right)
        r1 = bent_beam([2.4, 2.3, 0], [2.4, 0.3, 0], bend=0.55)
        l3 = small_label("bend", [3.4, 1.3, 0], size=24)

        for grp in ([w1, s1, l1], [w2, s2, l2], [r1, l3]):
            self.play(*[FadeIn(m) for m in grp], run_time=0.9)
            self.wait(0.3)
        self.wait(DUR - 4.5)
