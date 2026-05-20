from manim import *
import numpy as np
from centerofmass_helpers import (make_block, wide_shape, com_dot,
                                  ground_line, base_bracket, plumb_line,
                                  small_label)

# "Lower the center, widen the base, keep it over support — that's
#  balance, with no magic in it."
DUR = 8.1

GY = -1.6


class CenterofmassS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # --- panel 1: lower the center ---
        x1 = -4.0
        b1 = make_block(width=1.0, height=2.0, center=[x1, GY + 1.0, 0])
        c1 = com_dot([x1, GY + 0.55, 0], scale=0.7)
        arrow1 = Arrow([x1, GY + 1.3, 0], [x1, GY + 0.55, 0],
                       color="#7FB8E8", buff=0, stroke_width=4,
                       max_tip_length_to_length_ratio=0.3)
        t1 = small_label("lower the center", [x1, GY - 0.55, 0], size=22)

        # --- panel 2: widen the base ---
        x2 = 0.0
        b2 = wide_shape(center=[x2, GY + 0.55, 0])
        bb2 = base_bracket(x2 - 1.7, x2 + 1.7, GY - 0.15, color="#7FB8E8")
        c2 = com_dot([x2, GY + 0.45, 0], scale=0.7)
        t2 = small_label("widen the base", [x2, GY - 0.55, 0], size=22)

        # --- panel 3: keep it over support ---
        x3 = 4.0
        b3 = make_block(width=1.1, height=1.9, center=[x3, GY + 0.95, 0])
        c3 = com_dot([x3, GY + 0.95, 0], scale=0.7)
        pl3 = plumb_line([x3, GY + 0.95, 0], GY)
        bb3 = base_bracket(x3 - 0.55, x3 + 0.55, GY - 0.15, color="#7FB8E8")
        t3 = small_label("over support", [x3, GY - 0.55, 0], size=22)

        gl = ground_line(y=GY, x_half=6.4)
        self.add(gl)
        self.play(FadeIn(VGroup(b1, c1, arrow1, t1)), run_time=1.0)
        self.play(FadeIn(VGroup(b2, bb2, c2, t2)), run_time=1.0)
        self.play(FadeIn(VGroup(b3, c3, pl3, bb3, t3)), run_time=1.0)
        self.wait(DUR - 3.0)
