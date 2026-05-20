from manim import *
import numpy as np
from orbitlab_helpers import callback_thrown, small_label

# "And the ball thrown so fast the ground curved away beneath it —
#  falling, and never landing?"
DUR = 8.1


class OrbitlabS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        # build at full faint opacity, then fade in via FadeIn (which
        # animates a copy's alpha, not set_opacity on the closed arc)
        thrown = callback_thrown([0, 0.1, 0], scale=1.7, opacity=0.9)
        earth, arc, ball = thrown[0], thrown.arc, thrown.ball
        self.play(FadeIn(earth), Create(arc), run_time=1.6)
        self.add(ball)
        self.wait(0.3)
        # the ball runs its closing arc — falling, never landing
        self.play(MoveAlongPath(ball, arc), run_time=2.8,
                  rate_func=rate_functions.linear)
        cap = small_label("falling — and never landing",
                          [0, -2.6, 0], color="#8C8576", size=22)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 6.3)
