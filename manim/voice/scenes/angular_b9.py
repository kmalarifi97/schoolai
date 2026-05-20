from manim import *
import numpy as np
from angular_helpers import cascade, small_label, GLOW_COL

# "Notice the shape of this. Position becomes angle. Velocity becomes
#  rate of angle. Acceleration becomes rate of that rate. The same trio
#  as straight-line motion, just turned in a circle."
DUR = 15.3


class AngularS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        lin = cascade(("x", "v", "a"), [-2.4, 1.6, 0], dx=2.4)
        ang = cascade(("θ", "ω", "α"), [-2.4, -1.6, 0], dx=2.4)
        lin_terms, lin_arrows = lin
        ang_terms, ang_arrows = ang

        ltag = small_label("straight line", [-4.6, 1.6, 0],
                           color="#8C98A6", size=22)
        atag = small_label("turning", [-4.6, -1.6, 0],
                           color="#8C98A6", size=22)

        self.play(Write(lin_terms[0]), FadeIn(ltag), run_time=1.0)
        self.play(GrowArrow(lin_arrows[0]), Write(lin_terms[1]),
                  run_time=1.0)
        self.play(GrowArrow(lin_arrows[1]), Write(lin_terms[2]),
                  run_time=1.0)
        self.wait(0.6)

        self.play(Write(ang_terms[0]), FadeIn(atag), run_time=1.0)
        self.play(GrowArrow(ang_arrows[0]), Write(ang_terms[1]),
                  run_time=1.0)
        self.play(GrowArrow(ang_arrows[1]), Write(ang_terms[2]),
                  run_time=1.0)
        self.wait(0.5)

        # the parallel structure glows
        links = VGroup(*[
            DashedLine(lin_terms[k].get_bottom() + DOWN * 0.05,
                       ang_terms[k].get_top() + UP * 0.05,
                       color=GLOW_COL, stroke_width=2.5,
                       dash_length=0.12).set_opacity(0.6)
            for k in range(3)])
        self.play(LaggedStart(*[Create(l) for l in links],
                              lag_ratio=0.3, run_time=1.6))
        self.play(VGroup(lin_terms, ang_terms).animate.set_color(GLOW_COL),
                  run_time=1.0, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 12.2)
