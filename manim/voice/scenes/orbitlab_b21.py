from manim import *
import numpy as np
from orbitlab_helpers import callback_rocks, small_label

# "And if this felt familiar — it should. Do you remember the two
#  rocks that pulled each other across empty space, with nothing in
#  between?"
DUR = 11.3


class OrbitlabS1B21(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.0)
        rocks = callback_rocks([0, 0.0, 0], scale=1.7, opacity=0.0)
        self.play(rocks.animate.set_opacity(0.9), run_time=1.6)
        self.wait(0.6)
        # the two rocks ease toward each other along the force line
        big, small = rocks[1], rocks[2]
        self.play(big.animate.shift(RIGHT * 0.35),
                  small.animate.shift(LEFT * 0.35),
                  run_time=1.8,
                  rate_func=rate_functions.ease_in_out_sine)
        cap = small_label("two rocks — nothing in between",
                          [0, -2.4, 0], color="#8C8576", size=22)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 6.8)
