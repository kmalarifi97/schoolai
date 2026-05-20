from manim import *
import numpy as np
from collisionlab_helpers import (make_noura, make_cart, cl_track,
                                  cl_puck, momentum_arrow, ke_readout)

# "Before she argues another minute — she rebuilds the crash where she
#  can measure it."
DUR = 7.5


class CollisionlabS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the table carts
        c1 = make_cart([-1.2, 1.2, 0], scale=1.0, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([1.0, 1.2, 0], scale=1.0, color="#E8C46B",
                       dented=True, facing=-1)
        no = make_noura([-3.8, 1.5, 0], scale=0.9)
        self.add(c1, c2, no)
        self.wait(0.6)

        # the scene resolves into the Collision Lab layout
        self.play(FadeOut(no), run_time=0.8)
        tr = cl_track([0, -0.4, 0], w=7.0)
        p1 = cl_puck([-2.0, -0.4, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([1.6, -0.4, 0], color="#E8C46B", mass="1")
        self.play(
            Transform(c1, p1), Transform(c2, p2),
            FadeIn(tr), run_time=1.8)
        a1 = momentum_arrow([-2.0, -0.4, 0], 0.9, color="#E8C46B")
        ke = ke_readout([0, 2.0, 0], scale=0.8)
        self.play(GrowArrow(a1), FadeIn(ke), run_time=1.4)
        self.wait(DUR - 5.0)
