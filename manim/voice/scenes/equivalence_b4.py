from manim import *
import numpy as np
from equivalence_helpers import small_label, big_text, INERT, GRAV, INK

# "There's no reason these should be the same number. Resistance to a
#  push, and the strength of a pull — different questions."
DUR = 10.3


class EquivalenceS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        left = small_label("inertial mass", [-3.4, 0.0, 0],
                           color=INERT, size=34)
        right = small_label("gravitational mass", [3.4, 0.0, 0],
                            color=GRAV, size=34)
        self.play(FadeIn(left, shift=RIGHT * 0.2),
                  FadeIn(right, shift=LEFT * 0.2), run_time=1.2)
        self.wait(0.5)
        eq = big_text("=", [0, 0, 0], size=64, color=INK)
        self.play(Write(eq), run_time=0.8)
        q = big_text("?", [0, 0.95, 0], size=56, color="#E2B85A")
        self.play(FadeIn(q, scale=0.6), run_time=0.9)
        # the two sub-questions surface beneath
        s1 = small_label("resistance to a push", [-3.4, -1.0, 0],
                         color=INERT, size=22)
        s2 = small_label("strength of a pull", [3.4, -1.0, 0],
                         color=GRAV, size=22)
        self.play(FadeIn(s1), FadeIn(s2), run_time=1.0)
        self.play(q.animate.scale(1.12), run_time=0.8,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 5.7)
