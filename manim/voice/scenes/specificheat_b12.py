from manim import *
import numpy as np
from specificheat_helpers import label, INK, ENERGY_COL

# "Computing the heat needed from the specific heat, the mass, and the
#  temperature change — that's yours."
DUR = 7.9


class SpecificheatS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eq = label("heat = (specific heat) × mass × (temperature change)",
                   [0, 0.4, 0], size=34, color=INK)
        eq.scale_to_fit_width(11).move_to([0, 0.4, 0])
        sub = label("values left open", [0, -1.3, 0], size=24,
                    color="#9AA0A6")
        self.play(Write(eq), run_time=2.0)
        self.play(FadeIn(sub), run_time=1.0)
        self.wait(DUR - 3.0)
