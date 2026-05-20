from manim import *
import numpy as np
from specificheat_helpers import dial, label, ENERGY_COL, WATER_COL
from specificheat_helpers import OIL_COL, HOT_COL

# "Heat needed depends on three things: the substance, how much of it, and
#  how big a rise you want."
DUR = 7.9


class SpecificheatS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        d1 = dial([-3.6, 0.6, 0], "substance", frac=0.6, scale=1.0,
                  color=WATER_COL)
        d2 = dial([0, 0.6, 0], "mass", frac=0.45, scale=1.0, color=OIL_COL)
        d3 = dial([3.6, 0.6, 0], "temp. change", frac=0.7, scale=1.0,
                  color=HOT_COL)
        heat = label("heat", [0, -2.3, 0], size=40, color=ENERGY_COL)
        box = SurroundingRectangle(heat, color=ENERGY_COL, buff=0.3,
                                   stroke_width=3)
        self.play(FadeIn(d1), run_time=0.8)
        self.play(FadeIn(d2), run_time=0.8)
        self.play(FadeIn(d3), run_time=0.8)
        a1 = Arrow(d1.get_bottom(), box.get_corner(UL), buff=0.1,
                   color="#9AA0A6", stroke_width=3)
        a2 = Arrow(d2.get_bottom(), box.get_top(), buff=0.1,
                   color="#9AA0A6", stroke_width=3)
        a3 = Arrow(d3.get_bottom(), box.get_corner(UR), buff=0.1,
                   color="#9AA0A6", stroke_width=3)
        self.play(GrowArrow(a1), GrowArrow(a2), GrowArrow(a3), run_time=1.0)
        self.play(Write(heat), Create(box), run_time=1.0)
        self.wait(DUR - 5.2)
