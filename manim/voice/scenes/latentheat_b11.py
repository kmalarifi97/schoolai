from manim import *
import numpy as np
from latentheat_helpers import heating_curve, small_label

# "A full heating curve, then, has flats and slopes. Slopes warm it.
#  Flats rebuild it."
DUR = 7.3


class LatentheatS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hc = heating_curve(origin=(-5.0, -2.2, 0), w=10.0, h=4.0)
        ax_v, ax_h, curve, melt_seg, boil_seg = hc
        self.play(Create(ax_v), Create(ax_h), run_time=0.9)
        self.play(Create(curve), run_time=2.0)

        # flats rebuild (orange), slopes warm (red)
        g1 = melt_seg.copy().set_stroke("#F2A24E", width=11, opacity=0.9)
        g2 = boil_seg.copy().set_stroke("#F2A24E", width=11, opacity=0.9)
        self.play(Create(g1), Create(g2), run_time=1.0)

        sl = small_label("slopes warm", [-3.4, 1.4, 0],
                         color="#E8615A", size=24)
        fl = small_label("flats rebuild", [1.2, -1.6, 0],
                         color="#F2A24E", size=24)
        self.play(FadeIn(sl), FadeIn(fl), run_time=0.9)
        self.wait(DUR - 4.8)
