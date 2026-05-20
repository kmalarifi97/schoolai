from manim import *
import numpy as np
from tempvsthermal_helpers import (make_match, make_bathtub,
                                   make_thermometer, small_label)

# "The flame is far hotter. Hundreds of degrees against a mild forty."
DUR = 6.3


class TempvsthermalS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        match = make_match([-5.0, -0.2, 0], scale=0.85)
        tub = make_bathtub([4.4, -0.7, 0], scale=0.62, steam=True)
        self.add(match, tub)

        t_match = make_thermometer([-2.0, -0.1, 0], scale=0.9,
                                   fill_frac=0.04, label="match")
        t_tub = make_thermometer([1.6, -0.1, 0], scale=0.9,
                                 fill_frac=0.04, label="tub")
        self.play(FadeIn(t_match), FadeIn(t_tub), run_time=1.0)

        # rise the columns to their readings
        hi = make_thermometer([-2.0, -0.1, 0], scale=0.9,
                              fill_frac=0.95, label="match")
        lo = make_thermometer([1.6, -0.1, 0], scale=0.9,
                              fill_frac=0.30, label="tub")
        self.play(Transform(t_match, hi), Transform(t_tub, lo),
                  run_time=1.6)
        self.add(small_label("hundreds of degrees", [-2.0, 2.3, 0],
                             color="#FF7A3C", size=22),
                 small_label("a mild forty", [1.6, 1.4, 0],
                             color="#8FB8D8", size=22))
        self.wait(DUR - 4.1)
