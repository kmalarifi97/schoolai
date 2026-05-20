from manim import *
import numpy as np
from collisions_helpers import (clay_blob, fused_blob, energy_bar,
                                make_energy_fill, shimmer, title)

# "The clay lost most of it — to heat, to sound, to bending.
#  An inelastic collision."
DUR = 7.12


class CollisionsS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        before = energy_bar([-3.6, -0.2, 0], frac=0.92, label="before")
        after = energy_bar([-1.2, -0.2, 0], frac=0.01, label="after")
        self.add(before, after)
        c1 = clay_blob([1.6, 1.5, 0], seed=3, r=0.34)
        c2 = clay_blob([3.0, 1.5, 0], seed=7, r=0.34)
        self.play(FadeIn(before), FadeIn(c1), FadeIn(c2), run_time=0.9)

        lump = fused_blob([2.3, 1.5, 0], seed=9, r=0.46)
        grown = make_energy_fill(after, 0.16)
        sh = shimmer(np.array([2.3, 1.5, 0]), spread=1.3, n=14)
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(lump),
                  Transform(after[1], grown), run_time=0.6)
        self.play(LaggedStartMap(Create, sh, lag_ratio=0.05),
                  run_time=1.2)
        lbl = title("inelastic", [2.3, -1.0, 0], size=42, color="#C8654A")
        self.play(Write(lbl), run_time=0.9)
        self.wait(DUR - 3.6)
