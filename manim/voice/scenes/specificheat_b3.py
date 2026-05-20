from manim import *
import numpy as np
from specificheat_helpers import energy_bar, label, HOT_COL, WATER_COL, OIL_COL

# "Same energy in. Wildly different temperature out. Why does water resist
#  heating up?"
DUR = 7.1


class SpecificheatS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ein1 = energy_bar([-3.0, 2.2, 0], length=3.0, frac=1.0,
                          color="#F0902A")
        ein2 = energy_bar([3.0, 2.2, 0], length=3.0, frac=1.0,
                          color="#F0902A")
        le = label("same energy in", [0, 3.1, 0], size=26)
        # temperature-rise bars (vertical)
        riseW = Rectangle(width=0.7, height=0.7, stroke_width=0,
                          fill_color=WATER_COL, fill_opacity=1.0)
        riseW.move_to([-3.0, -1.7, 0], aligned_edge=DOWN)
        riseO = Rectangle(width=0.7, height=2.6, stroke_width=0,
                          fill_color=OIL_COL, fill_opacity=1.0)
        riseO.move_to([3.0, -1.7, 0], aligned_edge=DOWN)
        lw = label("water  ΔT", [-3.0, -2.2, 0], size=22)
        lo = label("oil  ΔT", [3.0, -2.2, 0], size=22)
        self.play(FadeIn(ein1), FadeIn(ein2), Write(le), run_time=1.2)
        self.play(GrowFromEdge(riseW, DOWN), GrowFromEdge(riseO, DOWN),
                  FadeIn(lw), FadeIn(lo), run_time=1.3)
        q = label("?", [0, -0.3, 0], size=80, color=HOT_COL)
        self.play(FadeIn(q, scale=0.6), run_time=0.8)
        self.wait(DUR - 3.3)
