from manim import *
import numpy as np
from centerofmass_helpers import (make_block, com_dot, ground_line,
                                  base_bracket, plumb_line, small_label)

# "Locating the center of mass of a given shape, and finding the maximum
#  tilt before its vertical line leaves the base — that's yours."
DUR = 11.4

GY = -2.0


class CenterofmassS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)
        W, H = 1.8, 2.8
        cx = 0.0
        blk = make_block(width=W, height=H, center=[cx, GY + H / 2, 0])
        bb = base_bracket(cx - W / 2, cx + W / 2, GY - 0.18)
        com = com_dot([cx, GY + H / 2, 0], scale=0.9)
        pl = plumb_line([cx, GY + H / 2, 0], GY)

        self.play(FadeIn(blk), FadeIn(bb), run_time=1.0)
        self.play(Create(com), run_time=0.9)
        self.play(Create(pl), run_time=0.9)

        # mark the open question: the maximum tilt, left for the student
        q = small_label("max tilt = ?", [cx + 2.6, GY + 1.4, 0],
                        size=28, color="#EAE4D5")
        arc = Arc(radius=0.9, start_angle=PI / 2,
                  angle=-0.4, color="#7FB8E8", stroke_width=3
                  ).move_arc_center_to(np.array([cx + W / 2, GY, 0]))
        self.play(FadeIn(q, shift=LEFT * 0.2), Create(arc), run_time=1.2)
        # holds — handed back to the student
        self.wait(DUR - 4.0)
