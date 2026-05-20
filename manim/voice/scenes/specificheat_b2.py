from manim import *
import numpy as np
from specificheat_helpers import Thermometer, energy_bar, label, HOT_COL

# "Equal heat poured into each. But the oil is scorching while the water is
#  merely warm."
DUR = 7.2


class SpecificheatS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eb1 = energy_bar([-2.6, 2.6, 0], length=2.6, frac=0.0)
        eb2 = energy_bar([2.6, 2.6, 0], length=2.6, frac=0.0)
        l1 = label("equal heat in", [-2.6, 3.2, 0], size=22)
        l2 = label("equal heat in", [2.6, 3.2, 0], size=22)
        tw = Thermometer([-2.6, -0.4, 0], height=2.8, level=0.12)
        to = Thermometer([2.6, -0.4, 0], height=2.8, level=0.12)
        lw = label("water", [-2.6, -2.3, 0], size=26)
        lo = label("oil", [2.6, -2.3, 0], size=26)
        self.add(eb1, eb2, l1, l2, tw, to, lw, lo)
        self.wait(0.5)
        self.play(eb1.fill.animate.scale([1, 1, 1]), run_time=0.1)
        self.play(
            eb1.fill.animate.stretch_to_fit_width(2.6).move_to(
                eb1.frame.get_left() + RIGHT * 1.3),
            eb2.fill.animate.stretch_to_fit_width(2.6).move_to(
                eb2.frame.get_left() + RIGHT * 1.3),
            run_time=1.2)
        self.play(
            UpdateFromAlphaFunc(tw, lambda m, a: m.set_level(0.12 + 0.30 * a)),
            UpdateFromAlphaFunc(to, lambda m, a: m.set_level(0.12 + 0.80 * a)),
            run_time=2.0)
        self.wait(DUR - 5.8)
