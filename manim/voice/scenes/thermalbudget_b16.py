from manim import *
import numpy as np
from thermalbudget_helpers import (efc_layout, temp_energy_curve,
                                   play_button)

# "Then she presses play. And she watches the energy chunks and the
#  flat stretch, not the ice."
DUR = 8.1


class ThermalbudgetS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        efc = efc_layout([-3.0, 0.2, 0], scale=0.75, heat=0.7,
                         melt=0.15, chunks=True)
        self.add(efc)
        crv = temp_energy_curve([2.4, 0.0, 0], scale=0.8,
                                progress=1.0)
        self.add(crv.axes, crv.curve)

        pb = play_button([-3.0, -2.7, 0], r=0.4)
        self.add(pb)
        # press play
        self.play(pb.animate.scale(0.85).set_color("#9BD6B0"),
                  run_time=0.5)
        self.play(pb.animate.scale(1.0 / 0.85), run_time=0.4)

        # rising energy chunks
        anims = []
        for c in efc.chunks:
            anims.append(c.animate.shift(UP * 0.7
                         + RIGHT * np.random.uniform(-0.1, 0.1)))
        self.play(*anims, run_time=1.6,
                  rate_func=rate_functions.linear)

        # the flat melting plateau lights up — camera "holds" on it
        self.play(Create(crv.plateau_seg), run_time=1.2)
        self.wait(DUR - 4.9)
