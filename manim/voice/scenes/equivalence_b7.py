from manim import *
import numpy as np
from equivalence_helpers import small_label, big_text, INERT, GRAV, INK

# "That only works if the stubbornness and the heaviness cancel
#  perfectly. The two masses are equal."
DUR = 8.5


class EquivalenceS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        left = small_label("inertial mass", [-3.4, 0.0, 0],
                           color=INERT, size=34)
        right = small_label("gravitational mass", [3.4, 0.0, 0],
                            color=GRAV, size=34)
        eq = big_text("=", [0, 0, 0], size=64, color=INK)
        q = big_text("?", [0, 0.95, 0], size=56, color="#E2B85A")
        self.add(left, right, eq, q)
        self.wait(0.8)
        # the '?' resolves into a firm '='
        self.play(FadeOut(q, shift=UP * 0.4, scale=0.5), run_time=1.0)
        self.play(eq.animate.set_color("#EAE4D5").scale(1.35),
                  run_time=0.9, rate_func=rate_functions.ease_out_back)
        self.play(Flash(eq, color="#EAE4D5", line_length=0.25,
                        num_lines=12, flash_radius=0.7), run_time=0.8)
        self.wait(DUR - 3.5)
