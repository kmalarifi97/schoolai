from manim import *
from specificheat_helpers import (
    burner, pot, clock, Thermometer, energy_bar, sponge, gram_cube,
    bar_chart, coast_cell, engine_block, water_bottle, standing_figure,
    dial, label, WATER_COL, OIL_COL, METAL_COL, SAND_COL,
)


class SpecificheatTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        p1 = pot([-5.6, 2.4, 0], "water", width=1.5, height=1.0)
        b1 = burner([-5.6, 1.5, 0], width=1.6, n_flames=2)
        p2 = pot([-3.9, 2.4, 0], "oil", width=1.5, height=1.0)
        ck = clock([-2.4, 2.6, 0], scale=0.7)
        t1 = Thermometer([-1.2, 2.2, 0], height=1.7, level=0.25)
        t2 = Thermometer([-0.3, 2.2, 0], height=1.7, level=0.8)
        eb = energy_bar([2.0, 2.6, 0], length=2.0, frac=0.8)
        sp = sponge([4.6, 2.3, 0], w=1.4, h=1.1)
        gc = gram_cube([-5.5, -0.6, 0], side=0.6, glow=0.5)
        bc = bar_chart([-2.6, -1.2, 0], [("water", 4.18, WATER_COL),
                                         ("oil", 2.0, OIL_COL),
                                         ("sand", 0.8, SAND_COL),
                                         ("iron", 0.45, METAL_COL)],
                       max_h=1.8, bar_w=0.4, gap=0.3)
        cc = coast_cell([2.4, -1.3, 0], w=3.0, h=1.8)
        en = engine_block([5.2, -0.4, 0], scale=0.6)
        wb = water_bottle([6.2, -1.6, 0], scale=0.5)
        fg = standing_figure([4.6, -2.2, 0], scale=0.7)
        dl = dial([0.4, -2.7, 0], "mass", frac=0.6, scale=0.7)
        self.add(p1, b1, p2, ck, t1, t2, eb, sp, gc, bc, cc, en, wb, fg, dl)
        self.add(label("specific heat", [-3.5, -3.4, 0], size=22))
        self.wait(0.1)
