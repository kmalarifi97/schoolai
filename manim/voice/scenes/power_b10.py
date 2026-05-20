from manim import *
import numpy as np
from power_helpers import (value_bar, big_label, small_label, horse_motif,
                           simple_car, POWER_COL)

# "The unit honors the man who measured engines against horses. The
#  watt."
DUR = 6.5


class PowerS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        horse = horse_motif([-2.6, 1.4, 0], scale=1.5)
        eng = simple_car([2.6, 1.4, 0], scale=1.1)
        eng.set_opacity(0.30)
        vs = small_label("vs", [0, 1.4, 0], size=30).set_opacity(0.45)
        self.play(FadeIn(horse), FadeIn(eng), FadeIn(vs), run_time=1.0)

        pb = value_bar(2.0, width=1.4, color=POWER_COL,
                       anchor=[0, -2.7, 0])
        self.play(GrowFromEdge(pb.bar, DOWN), run_time=0.9)
        self.wait(0.3)
        watt = big_label("watt", [0, -0.7, 0], size=58, color=POWER_COL)
        self.play(FadeIn(watt, scale=1.2), run_time=0.9)
        self.wait(max(0.3, DUR - 4.1))
