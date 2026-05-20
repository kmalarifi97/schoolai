from manim import *
import numpy as np
from thermolaws_helpers import (engine_box, energy_bar, small_label,
                                HEAT, WORK, WASTE)

# "Heat into an engine becomes work out, plus heat dumped away.
#  Add it all back: nothing missing. Ever."
DUR = 8.6


class ThermolawsS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eng = engine_box([0, 0.6, 0], scale=1.0, show_waste=True)
        self.play(FadeIn(eng), run_time=1.4)
        self.wait(0.6)
        # the accounting: input bar == work + waste, same total length
        inp = energy_bar([0, -2.6, 0], total_width=5.0, height=0.42,
                         fracs=[1.0], cols=[HEAT], labels=["heat in"])
        self.play(FadeIn(inp), run_time=1.0)
        self.wait(0.4)
        out = energy_bar([0, -2.6, 0], total_width=5.0, height=0.42,
                         fracs=[0.38, 0.62], cols=[WORK, WASTE],
                         labels=["work", "waste"])
        eq = small_label("=", [0, -2.05, 0], size=30, color="#EAE4D5")
        self.play(Transform(inp, out), run_time=1.8)
        self.play(FadeIn(eq), run_time=0.6)
        self.wait(DUR - 6.4)
