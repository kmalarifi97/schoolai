from manim import *
import numpy as np
from thermalbudget_helpers import efc_layout, small_label

# "Before she touches the heater again — she builds it where she can
#  see every line of the budget."
DUR = 8.3


class ThermalbudgetS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        t = small_label("before she touches the heater again",
                        [0, 2.6, 0], color="#8C8576", size=24)
        self.play(Write(t), run_time=1.4)

        efc = efc_layout([0, -0.4, 0], scale=1.0, heat=0.0,
                         melt=0.0, chunks=False)
        # resolve into the sim, piece by piece
        self.play(FadeIn(efc.heater), run_time=0.9)
        self.play(Create(efc.beaker), FadeIn(efc.water),
                  run_time=1.1)
        self.play(FadeIn(efc.ice, shift=DOWN * 0.1), run_time=0.9)
        self.play(FadeIn(efc.thermo), run_time=0.9)
        self.wait(DUR - 5.2)
