from manim import *
import numpy as np
from heattransfer_helpers import make_pot_on_flame, convection_loop

# "Now a pot of water on a flame. The bottom heats first. But the whole
#  pot warms — and the water churns."
DUR = 8.8


class HeattransferS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, 0.2, 0]
        pot, water, flame = make_pot_on_flame(C, scale=1.15)
        self.play(FadeIn(pot), run_time=1.0)
        self.play(LaggedStart(*[GrowFromCenter(f) for f in flame],
                              lag_ratio=0.04, run_time=1.4))
        self.wait(0.4)

        # bottom heats first: tint the water warmer
        self.play(water.animate.set_fill(color="#5E6E7E"), run_time=1.0)
        self.play(water.animate.set_fill(color="#7A6E62"), run_time=1.0)

        # the water churns
        loop = convection_loop(np.array(C) + np.array([0, -0.10, 0]),
                               w=2.4, h=1.4)
        self.play(LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow)
                                else Create(a) for a in loop],
                              lag_ratio=0.05, run_time=2.0))
        self.wait(DUR - 6.8)
