from manim import *
import numpy as np
from equivalence_helpers import (sealed_box, small_label, big_text,
                                 INK, INERT, GRAV)

# "Two views of the same equal masses — one calls it luck, one calls it
#  the door to a new theory. Which experiments would tell them apart?
#  That's the thinking we leave with you."
DUR = 14.0


class EquivalenceS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box1, p1 = sealed_box([-3.4, -0.2, 0], size=2.6,
                              with_flame=False)
        box2, p2 = sealed_box([3.4, -0.2, 0], size=2.6, with_flame=True)
        self.play(FadeIn(box1), FadeIn(box2), run_time=1.2)
        l1 = small_label("luck", [-3.4, 1.7, 0], color=GRAV, size=26)
        l2 = small_label("a new theory", [3.4, 1.7, 0],
                         color="#FFE08A", size=26)
        self.play(FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.wait(0.6)
        q = big_text("which experiment tells them apart?",
                     [0, -2.5, 0], size=30, color=INK)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=1.4)
        # holds, silent, the open question between them
        self.play(q.animate.set_opacity(0.85), run_time=0.8)
        self.wait(DUR - 6.0)
