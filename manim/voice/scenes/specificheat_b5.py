from manim import *
import numpy as np
from specificheat_helpers import energy_bar, Thermometer, gram_cube, label
from specificheat_helpers import OIL_COL, METAL_COL

# "Others heat fast — a little energy sends their temperature shooting up."
DUR = 6.8


class SpecificheatS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eb1 = energy_bar([-3.2, 2.4, 0], length=1.4, frac=1.0)
        l1 = label("a little energy", [-3.2, 3.0, 0], size=22)
        to = Thermometer([-3.2, -0.2, 0], height=2.6, level=0.12)
        lo = label("oil", [-3.2, -2.1, 0], size=24)

        eb2 = energy_bar([3.0, 2.4, 0], length=1.4, frac=1.0)
        l2 = label("a little energy", [3.0, 3.0, 0], size=22)
        tm = Thermometer([3.0, -0.2, 0], height=2.6, level=0.12)
        lm = label("metal", [3.0, -2.1, 0], size=24)

        self.add(eb1, l1, to, lo, eb2, l2, tm, lm)
        self.wait(0.4)
        self.play(
            UpdateFromAlphaFunc(to, lambda m, a: m.set_level(0.12 + 0.70 * a)),
            run_time=1.6)
        self.play(
            UpdateFromAlphaFunc(tm, lambda m, a: m.set_level(0.12 + 0.82 * a)),
            run_time=1.1)
        self.wait(DUR - 3.1)
