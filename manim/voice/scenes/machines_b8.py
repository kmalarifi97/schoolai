from manim import *
import numpy as np
from machines_helpers import (icon_screw, icon_wheel_axle, icon_pulley,
                              force_arrow, small_label)

# "So is a screw, an axle, a pulley. All of them: less force, more
#  distance, same job underneath."
DUR = 7.5


class MachinesS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sc = icon_screw([-3.6, 0.6, 0], 1.15)
        wa = icon_wheel_axle([0.0, 0.6, 0], 1.15)
        pl = icon_pulley([3.6, 0.6, 0], 1.15)
        self.play(FadeIn(sc, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(wa, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(pl, shift=UP * 0.2), run_time=0.8)

        for x, lbl in [(-3.6, "screw"), (0.0, "wheel & axle"),
                       (3.6, "pulley")]:
            self.add(small_label(lbl, [x, -1.0, 0], color="#8C98A6",
                                 size=24))
        self.wait(0.4)

        motif = small_label("less force  ·  more distance",
                            [0, -2.4, 0], color="#EAE4D5", size=28)
        self.play(FadeIn(motif), run_time=1.0)
        self.wait(DUR - 5.1)
