from manim import *
import numpy as np
from centerofmass_helpers import (make_block, com_dot, ground_line,
                                  base_bracket, small_label)

# "That's the whole rule of stability. Center of mass over the base of
#  support — it returns. Beyond it — it falls."
DUR = 9.6

GY = -1.9


class CenterofmassS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)
        W, H = 1.4, 2.2

        # ---- LEFT: stable (line inside base) ----
        lx = -3.2
        blkL = make_block(width=W, height=H, center=[lx, GY + H / 2, 0])
        bbL = base_bracket(lx - W / 2, lx + W / 2, GY - 0.16)
        comL = com_dot([lx, GY + H / 2, 0], scale=0.78)
        pivL = np.array([lx + W / 2, GY, 0])
        grpL = VGroup(blkL, comL)
        grpL.rotate(-0.18, about_point=pivL)
        comL.move_to(blkL.get_center())
        cpL = comL[0].get_center()
        plumbL = DashedLine(cpL, [cpL[0], GY, 0], color="#E8B04A",
                            stroke_width=2.4, dash_length=0.13)
        tagL = small_label("stable", [lx, GY - 0.7, 0], size=26,
                           color="#7FB8E8")

        # ---- RIGHT: toppling (line outside base) ----
        rx = 3.2
        blkR = make_block(width=W, height=H, center=[rx, GY + H / 2, 0])
        bbR = base_bracket(rx - W / 2, rx + W / 2, GY - 0.16)
        comR = com_dot([rx, GY + H / 2, 0], scale=0.78)
        pivR = np.array([rx + W / 2, GY, 0])
        grpR = VGroup(blkR, comR)
        grpR.rotate(-0.62, about_point=pivR)
        comR.move_to(blkR.get_center())
        cpR = comR[0].get_center()
        plumbR = DashedLine(cpR, [cpR[0], GY, 0], color="#E8B04A",
                            stroke_width=2.4, dash_length=0.13)
        tagR = small_label("topples", [rx, GY - 0.7, 0], size=26,
                           color="#C98A4A")

        self.add(gl)
        self.play(FadeIn(VGroup(blkL, bbL, comL)),
                  FadeIn(VGroup(blkR, bbR, comR)), run_time=1.0)
        self.play(Create(plumbL), Create(plumbR), run_time=1.2)
        self.play(FadeIn(tagL, shift=UP * 0.15),
                  FadeIn(tagR, shift=UP * 0.15), run_time=1.0)
        self.wait(DUR - 3.2)
