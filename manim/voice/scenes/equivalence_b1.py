from manim import *
import numpy as np
from equivalence_helpers import split_word_mass, small_label

# "The word mass hides two completely different ideas."
DUR = 5.2


class EquivalenceS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        whole, left, right = split_word_mass([0, 0, 0], size=80)
        self.play(FadeIn(whole, scale=0.85), run_time=1.2)
        self.wait(0.8)
        # split cleanly into two
        self.add(left, right)
        self.remove(whole)
        self.play(left.animate.shift(LEFT * 2.2),
                  right.animate.shift(RIGHT * 2.2),
                  run_time=1.4, rate_func=rate_functions.ease_out_cubic)
        self.wait(DUR - 3.4)
