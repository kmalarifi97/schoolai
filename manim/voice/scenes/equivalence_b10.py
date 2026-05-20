from manim import *
import numpy as np
from equivalence_helpers import (sealed_box, frictionless_plane,
                                 small_label, big_text, INK)

# "His thought: stand in a sealed box. The floor presses your feet.
#  Are you on Earth — or in a rocket accelerating through empty space?"
DUR = 11.0


class EquivalenceS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box1, p1 = sealed_box([-3.4, -0.3, 0], size=2.6,
                              with_flame=False)
        self.play(Create(box1[0]), run_time=1.0)
        self.play(FadeIn(box1[1]), FadeIn(box1[2]), run_time=0.8)
        ground = frictionless_plane(y=-1.65, x0=-6.4, x1=-0.6)
        ground[2].set_opacity(0)
        self.play(FadeIn(ground), run_time=0.7)
        q1 = small_label("on Earth?", [-3.4, 1.5, 0], size=26)
        self.play(FadeIn(q1), run_time=0.7)

        box2, p2 = sealed_box([3.4, -0.3, 0], size=2.6, with_flame=True)
        self.play(Create(box2[0]), FadeIn(box2[1]), FadeIn(box2[2]),
                  run_time=1.0)
        self.play(GrowFromCenter(p2["flame"]), run_time=0.6)
        # gentle upward thrust shudder
        self.play(box2.animate.shift(UP * 0.10), run_time=0.7,
                  rate_func=rate_functions.there_and_back)
        q2 = small_label("accelerating rocket?", [3.4, 1.5, 0], size=26)
        self.play(FadeIn(q2), run_time=0.7)
        self.wait(DUR - 7.0)
