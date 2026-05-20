from manim import *
import numpy as np
from centerofmass_helpers import (
    make_wrench, com_dot, com_crosshair, parabola_path, make_L_shape,
    make_block, ground_line, plumb_line, base_bracket, wide_shape,
    tall_shape, make_figure, make_load, small_label, com_label,
)


class CenterofmassTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        wr = make_wrench(scale=0.5).rotate(0.5).move_to([-4.6, 2.0, 0])
        cd = com_dot([-4.6, 2.0, 0], scale=0.8)

        arc = parabola_path([-6.2, -1.0, 0], [-2.8, -1.0, 0], 1.4)
        cd2 = com_dot([-4.5, -0.1, 0])

        Lsh, lcom = make_L_shape(scale=0.55, center=[-0.4, 1.6, 0])
        lc = com_crosshair(lcom, scale=0.8)

        blk = make_block(width=1.0, height=1.6, center=[2.4, 1.6, 0])
        bc = com_dot([2.4, 1.6, 0], scale=0.7)
        pl = plumb_line([2.4, 1.6, 0], 0.0)
        bb = base_bracket(1.9, 2.9, 0.0)

        ws = wide_shape(center=[4.6, 1.4, 0])
        ts = tall_shape(center=[4.9, -1.2, 0])

        fig = make_figure(center=[-2.2, -2.2, 0], scale=0.9, lean=-0.35)
        ld = make_load(fig.hand, scale=0.9)

        gl = ground_line(y=-3.3)
        lbl = small_label("center of mass", [0.0, -3.6, 0], size=22)

        self.add(wr, cd, arc, cd2, Lsh, lc, blk, bc, pl, bb,
                 ws, ts, fig, ld, gl, lbl)
        self.wait(0.4)
