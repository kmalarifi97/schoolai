from manim import *
import numpy as np
from specificheat_helpers import coast_cell, label, WATER_COL, SAND_COL
from specificheat_helpers import HOT_COL, COLD_COL

# "That's why the sea is mild while the desert sand next to it bakes by noon
#  and freezes by night."
DUR = 7.9


class SpecificheatS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cc = coast_cell([0, 0.2, 0], w=6.4, h=3.4)
        ls = label("sea — mild", [-1.6, -1.9, 0], size=24, color=WATER_COL)
        ld = label("sand — swings", [1.6, -1.9, 0], size=24, color=SAND_COL)
        self.play(FadeIn(cc), run_time=1.0)
        self.play(FadeIn(ls), FadeIn(ld), run_time=0.7)
        # noon: sun crosses, sand bakes hot, sea steady
        sand, sun = cc.sand, cc.sun
        self.play(
            sun.animate.move_to([cc.frame.get_x(),
                                 cc.frame.get_top()[1] - 0.5, 0]),
            sand.animate.set_fill(HOT_COL),
            run_time=1.7)
        self.wait(0.4)
        # night: sun gone, sand freezes, sea still steady
        self.play(
            sun.animate.move_to(cc.frame.get_right() + RIGHT * 0.6 +
                                DOWN * 1.2).set_opacity(0.0),
            sand.animate.set_fill(COLD_COL),
            run_time=1.7)
        self.wait(DUR - 6.5)
