from manim import *
import numpy as np
from thermalbudget_helpers import (callback_match_tub,
                                   callback_water_oil,
                                   callback_transfer,
                                   callback_stuck_thermo,
                                   efc_layout, temp_energy_curve,
                                   small_label)

# "This melt was all four at once. That is the concept. Now you know
#  which videos to go back to."
# Visual: the four callbacks converge into the single beaker +
# flat-plateau curve image, then hold ~3s in silence.
DUR = 8.2


class ThermalbudgetS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # four faint callbacks in the corners
        c1 = callback_match_tub([-4.0, 2.2, 0], scale=0.55,
                                opacity=0.0)
        c2 = callback_water_oil([4.0, 2.2, 0], scale=0.55,
                                opacity=0.0)
        c3 = callback_transfer([-3.6, -2.4, 0], scale=0.5,
                               opacity=0.0)
        c4 = callback_stuck_thermo([4.2, -2.2, 0], scale=0.55,
                                   opacity=0.0)
        self.play(c1.animate.set_opacity(0.75),
                  c2.animate.set_opacity(0.75),
                  c3.animate.set_opacity(0.75),
                  c4.animate.set_opacity(0.75), run_time=1.6)
        self.wait(0.6)

        # they converge into one center: beaker + flat-plateau curve
        efc = efc_layout([-2.0, -0.1, 0], scale=0.75, heat=0.5,
                         melt=0.4, chunks=True)
        crv = temp_energy_curve([2.4, -0.1, 0], scale=0.7,
                                progress=1.0)
        center = VGroup(efc, crv).set_opacity(0.0)
        self.add(center)
        self.play(
            c1.animate.scale(0.2).move_to([0, 0, 0]).set_opacity(0),
            c2.animate.scale(0.2).move_to([0, 0, 0]).set_opacity(0),
            c3.animate.scale(0.2).move_to([0, 0, 0]).set_opacity(0),
            c4.animate.scale(0.2).move_to([0, 0, 0]).set_opacity(0),
            center.animate.set_opacity(1.0),
            run_time=1.8)

        t = small_label("all four at once", [0, 3.2, 0],
                        color="#EAE4D5", size=26)
        self.play(FadeIn(t), run_time=0.9)

        # hold ~3s in silence
        self.wait(DUR - 5.9)
