from manim import *
import numpy as np
from thermolaws_helpers import (energy_bar, never_stamp, small_label,
                                WORK, WASTE)

# "Nothing in the first rule forbids the reverse. Energy would still
#  balance. Yet it never happens."
DUR = 7.7


class ThermolawsS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the reverse process — energy still balances perfectly
        left = energy_bar([0, 1.4, 0], total_width=5.0, height=0.45,
                          fracs=[0.38, 0.62], cols=[WORK, WASTE],
                          labels=["work", "waste"])
        eq = small_label("=", [0, 0.55, 0], size=30, color="#EAE4D5")
        right = energy_bar([0, -0.3, 0], total_width=5.0, height=0.45,
                           fracs=[1.0], cols=["#E07B4C"],
                           labels=["heat back"])
        cap = small_label("energy still balances", [0, -1.4, 0], size=24,
                          color="#7FC8A0")
        self.play(FadeIn(left), run_time=1.0)
        self.play(FadeIn(eq), FadeIn(right), run_time=1.2)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(0.6)
        # ...yet stamped never
        nv = never_stamp([0, -2.7, 0], scale=1.1)
        self.play(FadeIn(nv, scale=1.3), run_time=1.0)
        self.wait(DUR - 5.6)
