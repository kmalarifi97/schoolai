from manim import *
import numpy as np
from workenergy_helpers import (make_figure, make_wall, sweat_drop,
                                make_cart, force_arrow, displacement_arrow,
                                work_region, EnergyBar, small_label,
                                big_label, zero_tag)


class WorkenergyTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fig = make_figure([-5.2, -0.4, 0], scale=0.9, straining=True,
                          facing=1)
        wall = make_wall([-3.9, 0, 0])
        drop = sweat_drop([-4.7, 0.9, 0])
        zt = zero_tag([-3.9, 1.8, 0], size=44)

        cart = make_cart([-1.2, -1.6, 0], scale=0.8)
        fa = force_arrow([-2.4, -1.3, 0], length=1.1, direction=RIGHT)
        da = displacement_arrow([-2.4, -2.4, 0], length=2.2)

        rect, rlbl = work_region([0.6, -2.4, 0], w=2.6, h=1.0)

        bar = EnergyBar([4.3, -0.2, 0], height=2.6)
        bar.set_level(0.6)

        t1 = small_label("net work = change in motion", [1.7, 2.6, 0],
                         size=24)
        t2 = big_label("Work–Energy", [1.7, 3.3, 0], size=34)

        self.add(fig, wall, drop, zt, cart, fa, da, rect, rlbl, bar,
                 t1, t2)
        self.wait(0.4)
