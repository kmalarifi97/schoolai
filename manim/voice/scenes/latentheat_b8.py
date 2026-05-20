from manim import *
import numpy as np
from latentheat_helpers import heating_curve, small_label

# "The same pause happens again at boiling. Energy floods in to tear
#  liquid into vapor — temperature holds flat."
DUR = 9.0


class LatentheatS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hc = heating_curve(origin=(-5.0, -2.2, 0), w=10.0, h=4.0)
        ax_v, ax_h, curve, melt_seg, boil_seg = hc
        self.add(ax_v, ax_h, curve)
        # recall the melt plateau faintly
        m = melt_seg.copy().set_stroke("#F2A24E", width=8, opacity=0.45)
        self.add(m)
        self.wait(0.5)

        # highlight the SECOND flat plateau (boiling)
        glow = boil_seg.copy().set_stroke("#F2A24E", width=12,
                                          opacity=0.95)
        self.play(Create(glow), run_time=1.2)
        lbl = small_label("boiling — flat again", [2.1, 0.7, 0],
                          color="#F2A24E", size=24)
        self.play(FadeIn(lbl), run_time=0.9)

        # rolling-boil bubbles below the curve
        rng = np.random.default_rng(7)
        bubs = VGroup()
        for _ in range(7):
            x = rng.uniform(-2.0, 3.0)
            b = Circle(radius=rng.uniform(0.06, 0.13), color="#5E86A8",
                       fill_opacity=0.5, stroke_width=1.5)
            b.move_to([x, -3.1, 0])
            bubs.add(b)
        self.play(LaggedStart(*[b.animate.shift(UP * 0.6) for b in bubs],
                              lag_ratio=0.1, run_time=1.4))
        self.wait(DUR - 5.0)
