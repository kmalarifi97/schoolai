from manim import *
import numpy as np
from latentheat_helpers import (make_glass, make_flame, make_thermometer,
                                small_label)

# "Only once the last of the ice is freed does the thermometer start
#  climbing again."
DUR = 7.4


class LatentheatS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        flame = make_flame([-1.4, -1.9, 0], scale=1.0)
        glass = make_glass([-1.4, 0.7, 0], scale=1.0, ice_frac=1.0)
        therm = make_thermometer([2.4, 0.4, 0], scale=1.0, level=0.0)
        self.add(flame, glass, therm)
        self.wait(0.5)

        # last ice cube melts away (cubes are indices 2.. in the glass)
        cubes = VGroup(*[glass[k] for k in range(2, len(glass))])
        self.play(LaggedStart(*[FadeOut(c, scale=0.3) for c in cubes],
                              lag_ratio=0.25, run_time=2.0))

        # needle finally rises off zero
        therm_new = make_thermometer([2.4, 0.4, 0], scale=1.0,
                                     level=0.42)
        self.play(Transform(therm, therm_new), run_time=1.8,
                  rate_func=rate_functions.ease_in_out_sine)
        lbl = small_label("climbing again", [2.4, -2.4, 0],
                          color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=0.7)
        self.wait(DUR - 5.0)
