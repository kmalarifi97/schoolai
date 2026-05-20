from manim import *
import numpy as np
from latentheat_helpers import make_lattice, energy_arrows, small_label

# "Zoom in. In ice, particles are locked in a rigid lattice. The
#  incoming energy isn't speeding them up —"
DUR = 8.6


class LatentheatS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        lat = make_lattice([0, 0.2, 0], rows=4, cols=4, gap=0.72,
                            part_r=0.17)
        bonds, parts = lat[0], lat[1]
        self.play(Create(bonds), run_time=1.4)
        self.play(LaggedStart(*[GrowFromCenter(p) for p in parts],
                              lag_ratio=0.04, run_time=1.4))
        lbl = small_label("rigid lattice", [0, -2.4, 0],
                          color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=0.8)

        arrows = energy_arrows([0, 0.2, 0], n=4, length=0.6,
                               spread=1.6, y=-2.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.1, run_time=1.2))
        # tiny jitter only — NOT speeding up
        self.play(parts.animate.shift(UP * 0.04), run_time=0.4)
        self.play(parts.animate.shift(DOWN * 0.04), run_time=0.4)
        self.wait(DUR - 6.0)
