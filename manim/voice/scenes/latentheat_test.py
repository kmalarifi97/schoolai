from manim import *
import numpy as np
from latentheat_helpers import (make_glass, make_flame, make_thermometer,
                                energy_arrows, heating_curve, make_lattice,
                                energy_bar, make_skin, droplet, steam_curl,
                                small_label)


class LatentheatTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        glass = make_glass([-5.0, 1.4, 0], scale=0.7, ice_frac=1.0)
        flame = make_flame([-5.0, -0.6, 0], scale=0.8)
        therm = make_thermometer([-3.4, 1.2, 0], scale=0.7, level=0.0)
        arr = energy_arrows([-5.0, 1.4, 0], n=4, length=0.5, spread=1.0,
                            y=-2.0)

        lat = make_lattice([-0.5, 1.6, 0], rows=3, cols=3, gap=0.45,
                            part_r=0.12)
        crv = heating_curve(origin=(-1.8, -2.6, 0), w=4.0, h=2.2)

        bar1 = energy_bar([3.0, 1.6, 0], 0.9, "steam", max_h=1.6, w=0.5)
        bar2 = energy_bar([4.0, 1.6, 0], 0.3, "water", max_h=1.6, w=0.5)

        skin = make_skin([3.4, -1.8, 0], w=3.0, h=0.6)
        dp = droplet([3.0, -1.4, 0], r=0.12)
        st = steam_curl([4.4, -1.6, 0], scale=0.7)

        lbl = small_label("latent heat", [0, 3.4, 0], size=28)

        self.add(glass, flame, therm, arr, lat, crv, bar1, bar2,
                 skin, dp, st, lbl)
        self.wait(0.4)
