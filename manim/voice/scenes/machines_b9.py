from manim import *
import numpy as np
from machines_helpers import (icon_screw, icon_wheel_axle, icon_pulley,
                              make_bicycle, small_label)

# "Stack them together and you get a compound machine — a bicycle, a
#  pair of scissors, an engine."
DUR = 8.0


class MachinesS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sc = icon_screw([-4.4, 1.4, 0], 0.7)
        wa = icon_wheel_axle([0.0, 1.9, 0], 0.7)
        pl = icon_pulley([4.4, 1.4, 0], 0.7)
        self.play(FadeIn(sc), FadeIn(wa), FadeIn(pl), run_time=1.0)
        self.wait(0.5)

        bike = make_bicycle([0, -0.6, 0], scale=1.05)
        # the icons converge into the compound machine
        self.play(sc.animate.scale(0.3).move_to([0, -0.6, 0]).set_opacity(0),
                  wa.animate.scale(0.3).move_to([0, -0.6, 0]).set_opacity(0),
                  pl.animate.scale(0.3).move_to([0, -0.6, 0]).set_opacity(0),
                  run_time=1.6, rate_func=rate_functions.ease_in_sine)
        self.play(Create(bike), run_time=1.8)
        self.add(small_label("compound machine", [0, -2.9, 0],
                             color="#EAE4D5", size=30))
        self.wait(DUR - 6.7)
