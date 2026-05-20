from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, make_bathtub, small_label)

# "Average jiggle versus the whole sum — and how many particles bridges
#  them. Quantifying that link is yours."
DUR = 9.1


class TempvsthermalS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([-4.4, 0.3, 0], scale=0.85)
        tub = make_bathtub([3.6, -0.4, 0], scale=0.78)
        self.play(FadeIn(match), FadeIn(tub), run_time=1.2)

        self.add(small_label("average jiggle", [-4.4, -2.2, 0],
                             size=22, color="#FF7A3C"),
                 small_label("whole sum", [3.6, -2.6, 0],
                             size=22, color="#E5A23C"))

        # the bridge: count of particles, left open
        bridge = DoubleArrow([-2.6, -0.2, 0], [1.4, -0.2, 0],
                             color="#8C98A6", stroke_width=4, buff=0.1)
        self.play(GrowFromCenter(bridge), run_time=0.9)
        self.add(small_label("how many particles?", [-0.6, 0.5, 0],
                             size=24, color="#EAE4D5"))
        self.add(small_label("quantifying the link is yours",
                             [0, 3.2, 0], size=24, color="#EAE4D5"))
        # holds
        self.wait(DUR - 2.1)
