from manim import *
import numpy as np
from thermalbudget_helpers import (callback_transfer,
                                   callback_stuck_thermo,
                                   small_label)

# "And the spoon, the churning pot, the Sun across empty space — three
#  ways heat ever arrives? And the thermometer that stuck at zero while
#  the ice quietly drank it all?"
DUR = 13.5


class ThermalbudgetS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        # the conduction/convection/radiation triptych
        tri = callback_transfer([0, 0.5, 0], scale=1.4, opacity=0.0)
        self.play(tri.animate.set_opacity(0.9), run_time=1.6)
        self.wait(2.4)
        t1 = small_label("three ways heat arrives", [0, -1.6, 0],
                         color="#8C8576", size=22)
        self.play(FadeIn(t1), run_time=1.0)
        self.wait(1.4)
        self.play(tri.animate.set_opacity(0.0),
                  t1.animate.set_opacity(0.0), run_time=1.0)

        # then the thermometer stuck at 0 while the ice drinks it all
        st = callback_stuck_thermo([0, 0.2, 0], scale=1.5,
                                   opacity=0.0)
        self.play(st.animate.set_opacity(0.9), run_time=1.4)
        self.wait(DUR - 9.6)
