from manim import *
import numpy as np
from collisions_helpers import (momentum_bar, energy_bar, small_label,
                                title)

# "Momentum was conserved in both. So the difference isn't there.
#  It's in the energy of motion."
DUR = 7.91


class CollisionsS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sL = small_label("steel", [-3.4, 3.0, 0], size=24, color="#8C95A1")
        sR = small_label("clay", [3.4, 3.0, 0], size=24, color="#B07A52")

        mL = momentum_bar([-3.4, 1.7, 0], width=3.4, frac=0.6,
                          label="total momentum")
        mR = momentum_bar([3.4, 1.7, 0], width=3.4, frac=0.6,
                          label="total momentum")
        self.add(sL, sR)
        self.play(FadeIn(mL), FadeIn(mR), run_time=1.0)
        same = small_label("same", [0, 1.7, 0], size=22, color="#7FC27F")
        self.play(FadeIn(same), run_time=0.5)
        self.wait(0.5)

        eL = energy_bar([-3.4, -1.4, 0], frac=0.9, label="motion energy")
        eR = energy_bar([3.4, -1.4, 0], frac=0.18, label="motion energy")
        self.play(FadeIn(eL, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(eR, shift=UP * 0.2), run_time=0.7)
        diff = small_label("different", [0, -1.4, 0], size=22,
                           color="#E8C24A")
        self.play(FadeIn(diff), run_time=0.5)
        self.wait(DUR - 4.6)
