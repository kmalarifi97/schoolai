from manim import *
import numpy as np
from heattransfer_helpers import (make_spoon, make_particle_chain,
                                  small_label, heat_tint)

# "Heat passed by contact, particle to particle, the material itself
#  staying put. That's conduction."
DUR = 8.5


class HeattransferS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the whole handle, relay completed -> warm along its length
        sp, handle = make_spoon([2.0, 2.4, 0], [-1.6, -2.2, 0], scale=1.1)
        n = len(handle)
        self.add(sp)
        self.wait(0.5)

        anims = [seg.animate.set_color(heat_tint(0.45 + 0.55 *
                 (1.0 - i / (n - 1)))) for i, seg in enumerate(handle)]
        self.play(LaggedStart(*anims, lag_ratio=0.10, run_time=2.0))

        # a faint particle hint near the handle (material stays put)
        chain, parts, bonds = make_particle_chain(
            [-4.6, 1.6, 0], [-1.6, 1.6, 0], n=6, r=0.13)
        chain.set_opacity(0.55)
        self.play(FadeIn(chain), run_time=0.8)

        lbl = small_label("conduction — by contact", [0, -3.2, 0],
                          color=heat_tint(0.8), size=30)
        self.play(Write(lbl), run_time=1.4)
        self.wait(DUR - 5.7)
