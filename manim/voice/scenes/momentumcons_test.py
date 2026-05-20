from manim import *
import numpy as np
from momentumcons_helpers import (
    frozen_lake, make_figure, make_bag, momentum_bar, zero_line,
    make_balance, isolated_boundary, make_rocket, exhaust_plume,
    make_cart, momentum_token, arrow_between, label, sign_tag,
    PLUS_COL, MINUS_COL,
)


class MomentumconsTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        lake = frozen_lake((0, 0, 0)).scale(0.9)
        fig = make_figure((-4.8, 1.8, 0), scale=0.7)
        bag = make_bag((-3.6, 1.8, 0), scale=0.7)

        zl = zero_line((-1.3, 1.7, 0), height=1.8)
        bp = momentum_bar(0.9, +1, origin=(-1.3, 1.7, 0), unit=1.0)
        bm = momentum_bar(0.9, -1, origin=(-1.3, 1.7, 0), unit=1.0)

        bal = make_balance((4.0, 1.6, 0), span=3.0).scale(0.8)

        bnd = isolated_boundary((-3.6, -1.8, 0), w=3.4, h=2.4)
        rk = make_rocket((-0.2, -1.6, 0), scale=0.7)
        ex = exhaust_plume((-0.2, -2.35, 0), scale=0.7)

        c1 = make_cart((2.8, -1.8, 0), scale=0.7, color=PLUS_COL)
        c2 = make_cart((4.3, -1.8, 0), scale=0.7, color=MINUS_COL)
        tok = momentum_token((5.6, -1.8, 0), scale=0.9)

        self.add(lake, fig, bag, zl, bp, bm, bal, bnd, rk, ex, c1, c2, tok)
        self.add(label("primitives", (0, 3.4, 0), size=24))
        self.wait(0.4)
