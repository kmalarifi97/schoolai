from manim import *
import numpy as np
from equivalence_helpers import sealed_box, small_label, big_text, INK

# "From inside, you cannot tell. Gravity and acceleration feel exactly
#  the same. That's the equivalence principle."
DUR = 9.5


class EquivalenceS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box1, p1 = sealed_box([-3.2, 0.1, 0], size=2.6,
                              with_flame=False)
        box2, p2 = sealed_box([3.2, 0.1, 0], size=2.6, with_flame=True)
        self.add(box1, box2)
        self.wait(0.7)
        # the two boxes slide together and overlay into one
        self.play(box1.animate.move_to([0, 0.1, 0]),
                  box2.animate.move_to([0, 0.1, 0]),
                  run_time=1.8, rate_func=rate_functions.ease_in_out_sine)
        # the rocket-flame difference dissolves away
        self.play(FadeOut(p2["flame"]), run_time=0.8)
        self.play(box2.animate.set_opacity(0.0), run_time=0.7)
        self.play(Indicate(box1[2], color="#FFE08A", scale_factor=1.1),
                  run_time=0.9)
        lbl = big_text("equivalence", [0, -2.4, 0], size=44,
                       color="#FFE08A")
        self.play(FadeIn(lbl, shift=UP * 0.2), run_time=1.0)
        self.wait(DUR - 6.9)
