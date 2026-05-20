from manim import *
import numpy as np
from collisionlab_helpers import (cl_track, cl_puck, momentum_arrow,
                                  small_label)

# "Given what each cart does after — work backward. What speed must each
#  have had before, so the total momentum balances?"
DUR = 10.0


class CollisionlabS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tr = cl_track([0, 0.8, 0], w=6.8)
        # "after" state shown: pucks moving apart
        p1 = cl_puck([-1.6, 0.8, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([1.6, 0.8, 0], color="#E8C46B", mass="1")
        a1 = momentum_arrow([-1.6, 0.8, 0], -0.5, color="#7FB8E8")
        a2 = momentum_arrow([1.6, 0.8, 0], 0.9, color="#E8C46B")
        self.add(tr, p1, p2, a1, a2)
        aft = small_label("after — known", [3.4, 0.8, 0],
                          color="#8C8576", size=20)
        self.play(FadeIn(aft), run_time=1.0)

        # two "before speed = ?" blanks
        b1 = small_label("before speed = ?", [-2.6, -0.8, 0],
                         color="#EAE4D5", size=22)
        b2 = small_label("before speed = ?", [2.6, -0.8, 0],
                         color="#EAE4D5", size=22)
        self.play(FadeIn(b1), FadeIn(b2), run_time=1.4)

        rel = small_label("Σp before = Σp after", [0, -2.2, 0],
                          color="#7FB8E8", size=26)
        self.play(Write(rel), run_time=1.6)
        # the relation pulses once — the constraint that pins it down
        self.play(rel.animate.scale(1.08), run_time=0.5)
        self.play(rel.animate.scale(1 / 1.08), run_time=0.5)
        self.wait(DUR - 6.0)
