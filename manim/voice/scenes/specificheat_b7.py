from manim import *
import numpy as np
from specificheat_helpers import bar_chart, label, WATER_COL, OIL_COL
from specificheat_helpers import SAND_COL, METAL_COL

# "Water's is famously huge. It's one of the hardest common things to heat —
#  and to cool."
DUR = 7.3


class SpecificheatS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = label("specific heat", [0, 3.0, 0], size=30, color="#9AA0A6")
        bc = bar_chart([0, -1.4, 0],
                       [("water", 4.18, WATER_COL),
                        ("oil", 2.0, OIL_COL),
                        ("sand", 0.84, SAND_COL),
                        ("iron", 0.45, METAL_COL)],
                       max_h=3.6, bar_w=0.9, gap=0.7)
        self.play(FadeIn(title), run_time=0.7)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bc.bars],
                              lag_ratio=0.18, run_time=2.0))
        # caption the dominance
        cap = label("water", [bc.bars[0].get_x(),
                              bc.bars[0].get_top()[1] + 0.35, 0],
                    size=24, color=WATER_COL)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(DUR - 3.4)
