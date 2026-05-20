from manim import *
import numpy as np
from specificheat_helpers import pot, burner, clock, label

# "Same flame. Same time. Under one pot of water — and one pot of cooking oil."
DUR = 6.8


class SpecificheatS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        pw = pot([-3.0, 0.7, 0], "water", width=2.2, height=1.4)
        bw = burner([-3.0, -0.55, 0], width=2.4, n_flames=3)
        po = pot([3.0, 0.7, 0], "oil", width=2.2, height=1.4)
        bo = burner([3.0, -0.55, 0], width=2.4, n_flames=3)
        ck = clock([0, 1.3, 0], scale=0.85)
        lw = label("water", [-3.0, -1.6, 0], size=26)
        lo = label("oil", [3.0, -1.6, 0], size=26)
        self.play(FadeIn(bw), FadeIn(bo), run_time=1.0)
        self.play(FadeIn(pw), FadeIn(po), run_time=1.0)
        self.play(FadeIn(ck), FadeIn(lw), FadeIn(lo), run_time=0.9)
        self.wait(DUR - 2.9)
