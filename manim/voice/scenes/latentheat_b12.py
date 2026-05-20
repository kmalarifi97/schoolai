from manim import *
import numpy as np
from latentheat_helpers import heating_curve, small_label

# "Computing the heat absorbed during melting and boiling from the mass
#  and the latent heat — that's yours."
DUR = 9.0


class LatentheatS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hc = heating_curve(origin=(-5.0, -2.2, 0), w=10.0, h=4.0)
        ax_v, ax_h, curve, melt_seg, boil_seg = hc
        self.play(Create(ax_v), Create(ax_h), run_time=0.9)
        self.play(Create(curve), run_time=2.0)

        g1 = melt_seg.copy().set_stroke("#F2A24E", width=11, opacity=0.9)
        g2 = boil_seg.copy().set_stroke("#F2A24E", width=11, opacity=0.9)
        self.play(Create(g1), Create(g2), run_time=1.0)

        l1 = small_label("melting:  Q = ?", [-1.6, -1.7, 0],
                         color="#8C98A6", size=24)
        l2 = small_label("boiling:  Q = ?", [2.4, 1.0, 0],
                         color="#8C98A6", size=24)
        self.play(FadeIn(l1), FadeIn(l2), run_time=1.0)
        # the curve holds, equations left open
        self.wait(DUR - 4.9)
