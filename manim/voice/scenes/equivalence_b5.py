from manim import *
import numpy as np
from equivalence_helpers import make_ball, small_label

# "And yet. Galileo's old observation: drop a heavy thing and a light
#  thing together —"
DUR = 7.5


class EquivalenceS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        y0 = 2.6
        heavy = make_ball([-1.8, y0, 0], radius=0.46, big=True)
        light = make_ball([1.8, y0, 0], radius=0.30, big=False)
        self.play(FadeIn(heavy, shift=DOWN * 0.2),
                  FadeIn(light, shift=DOWN * 0.2), run_time=1.2)
        lh = small_label("heavy", [-1.8, y0 + 0.85, 0], size=22)
        ll = small_label("light", [1.8, y0 + 0.85, 0], size=22)
        self.play(FadeIn(lh), FadeIn(ll), run_time=0.8)
        self.wait(0.7)
        # released together — start of the fall, paused mid-drop
        self.play(heavy.animate.shift(DOWN * 1.0),
                  light.animate.shift(DOWN * 1.0),
                  lh.animate.shift(DOWN * 1.0),
                  ll.animate.shift(DOWN * 1.0),
                  run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 4.3)
