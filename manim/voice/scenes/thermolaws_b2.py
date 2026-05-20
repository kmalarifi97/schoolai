from manim import *
import numpy as np
from thermolaws_helpers import (stone_tablet, tablet_inscribe, energy_bar,
                                FUEL, MOTION, HEAT)

# "First rule. Energy is never created and never destroyed.
#  It only changes form, or moves."
DUR = 7.4


class ThermolawsS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # energy total bar — a FIXED outer length throughout
        bar_a = energy_bar([0, 1.4, 0], total_width=5.4, height=0.55,
                           fracs=[0.70, 0.20, 0.10],
                           cols=[FUEL, MOTION, HEAT],
                           labels=["fuel", "motion", "heat"])
        self.play(FadeIn(bar_a), run_time=1.2)
        self.wait(0.5)
        # energy only changes FORM — same total length, shifting split
        bar_b = energy_bar([0, 1.4, 0], total_width=5.4, height=0.55,
                           fracs=[0.20, 0.45, 0.35],
                           cols=[FUEL, MOTION, HEAT],
                           labels=["fuel", "motion", "heat"])
        self.play(Transform(bar_a, bar_b), run_time=1.8)
        self.wait(0.4)
        # inscribe the first tablet
        t1 = stone_tablet([0, -1.5, 0], scale=0.95, faint=False)
        ins = tablet_inscribe(t1, "energy is\nconserved", "I")
        self.play(FadeIn(t1), run_time=0.8)
        self.play(Write(ins), run_time=1.4)
        self.wait(DUR - 6.5)
