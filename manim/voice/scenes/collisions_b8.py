from manim import *
import numpy as np
from collisions_helpers import (clay_blob, fused_blob, energy_bar,
                                make_energy_fill, shimmer, title)

# "And the extreme: when they stick and move off as one.
#  Perfectly inelastic. The most energy lost."
DUR = 8.12


class CollisionsS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eb = energy_bar([-5.0, 0.2, 0], frac=0.9, label="motion energy")
        self.add(eb)
        c1 = clay_blob([-1.2, 0.4, 0], seed=3)
        c2 = clay_blob([1.2, 0.4, 0], seed=7)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)

        self.play(c1.animate.move_to([-0.45, 0.4, 0]),
                  c2.animate.move_to([0.45, 0.4, 0]),
                  run_time=1.1, rate_func=rate_functions.linear)
        lump = fused_blob([0, 0.4, 0], seed=9, r=0.66)
        drained = make_energy_fill(eb, 0.08)
        sh = shimmer(np.array([0, 0.4, 0]), spread=1.7, n=18)
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(lump),
                  Transform(eb[1], drained), run_time=0.5)
        self.play(LaggedStartMap(Create, sh, lag_ratio=0.04),
                  run_time=1.3)
        self.play(lump.animate.shift(RIGHT * 1.4),
                  sh.animate.shift(RIGHT * 1.4).set_opacity(0.0),
                  run_time=1.5, rate_func=rate_functions.ease_out_quad)
        lbl = title("perfectly inelastic", [0, -2.3, 0], size=38,
                    color="#C8654A")
        self.play(Write(lbl), run_time=1.0)
        self.wait(DUR - 6.5)
