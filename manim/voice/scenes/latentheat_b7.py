from manim import *
import numpy as np
from latentheat_helpers import heating_curve, small_label

# "That hidden energy — paid to change state, not to change temperature
#  — is the latent heat."
DUR = 7.8


class LatentheatS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hc = heating_curve(origin=(-5.0, -2.2, 0), w=10.0, h=4.0)
        ax_v, ax_h, curve, melt_seg, boil_seg = hc
        self.play(Create(ax_v), Create(ax_h), run_time=1.0)
        self.play(Create(curve), run_time=1.8)
        self.wait(0.3)

        # highlight the flat melting segment
        glow = melt_seg.copy().set_stroke("#F2A24E", width=12,
                                          opacity=0.9)
        self.play(Create(glow), run_time=1.0)
        lbl = small_label("latent heat — hidden, no temp change",
                          [0.2, -1.8, 0], color="#F2A24E", size=26)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 5.0)
