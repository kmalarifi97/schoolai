from manim import *
import numpy as np
from collisions_helpers import steel_ball, clay_blob, qmark, small_label

# "But momentum doesn't tell the whole story of the crash.
#  Listen to the difference."
DUR = 7.26


class CollisionsS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # left case: steel pair frozen at impact
        s1 = steel_ball([-3.9, 0.3, 0])
        s2 = steel_ball([-3.0, 0.3, 0])
        lblL = small_label("steel", [-3.45, -1.4, 0], size=24)
        # right case: clay pair frozen at impact
        c1 = clay_blob([3.0, 0.3, 0], seed=3)
        c2 = clay_blob([3.9, 0.3, 0], seed=7)
        lblR = small_label("clay", [3.45, -1.4, 0], size=24)

        self.play(FadeIn(s1), FadeIn(s2), FadeIn(c1), FadeIn(c2),
                  run_time=1.1)
        self.play(FadeIn(lblL), FadeIn(lblR), run_time=0.6)
        q = qmark([0, 0.3, 0], size=80)
        self.play(Write(q), run_time=0.8)
        self.play(q.animate.scale(1.12), run_time=0.6,
                  rate_func=there_and_back)
        self.wait(DUR - 3.1)
