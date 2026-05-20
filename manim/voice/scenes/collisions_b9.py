from manim import *
import numpy as np
from collisions_helpers import split_bar, make_split_fills, title

# "The energy was never destroyed. It left the motion and became
#  heat, deformation, noise."
DUR = 7.26


class CollisionsS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ttl = title("total energy — conserved", [0, 2.4, 0], size=30,
                    color="#EAE4D5")
        sb = split_bar([0, 0, 0], width=6.4, height=0.62,
                       useful_frac=0.95)
        self.add(ttl)
        self.play(FadeIn(sb), run_time=1.0)
        self.wait(0.6)

        # useful motion shrinks; lost grows by the same amount
        for f in (0.7, 0.45, 0.25):
            nl, nr = make_split_fills(sb, f)
            self.play(Transform(sb[1], nl), Transform(sb[2], nr),
                      run_time=0.9,
                      rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 4.9)
