from manim import *
import numpy as np
from collisions_helpers import (clay_blob, fused_blob, energy_bar,
                                make_energy_fill)

# "Two balls of clay hit and just — stop. Stuck together. Dead."
DUR = 5.46


class CollisionsS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c1 = clay_blob([-4.0, 0.4, 0], seed=3)
        c2 = clay_blob([4.0, 0.4, 0], seed=7)
        eb = energy_bar([5.4, 0.0, 0], frac=0.95, label="motion energy")
        self.add(eb)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.8)

        self.play(c1.animate.move_to([-0.45, 0.4, 0]),
                  c2.animate.move_to([0.45, 0.4, 0]),
                  run_time=1.2, rate_func=rate_functions.linear)
        lump = fused_blob([0, 0.4, 0], seed=9)
        new_fill = make_energy_fill(eb, 0.10)
        self.play(FadeOut(c1), FadeOut(c2), FadeIn(lump),
                  Transform(eb[1], new_fill),
                  run_time=0.5)
        # barely crawls
        self.play(lump.animate.shift(RIGHT * 0.5),
                  run_time=1.4, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 3.9)
