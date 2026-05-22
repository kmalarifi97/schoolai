from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, make_scale, divider, label,
                                qmark, make_equation_g, CHALK, DIM, RED)

# "How could anyone weigh the entire Earth? You can't lift it. You can't
#  put it on a scale. It seems impossible."
DUR = 9.3


class WeighearthS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # g-equation dimmed on the scoreboard.
        eq = make_equation_g([3.3, 0.5, 0], scale=1.2)
        eq.set_color(DIM)
        self.add(eq)

        # A giant scale, tilted hard under the Earth's weight.
        scale = make_scale([-3.5, -0.3, 0], scale=1.4, tilt=-0.32)
        self.play(FadeIn(scale), run_time=1.0)

        # The Earth sits on the (lower) left pan.
        earth = make_earth(scale.left_pan.get_center() + np.array([0, 0.55, 0]),
                           r=0.6)
        self.play(FadeIn(earth, scale=0.8), run_time=1.0)
        self.wait(0.6)

        # A large '?'.
        q = qmark([-2.2, 1.6, 0], size=110, color=RED, opacity=0.9)
        self.play(FadeIn(q, scale=0.6), run_time=1.0)

        imp = label("seems impossible", [-3.5, -2.6, 0], size=24, color=DIM)
        self.play(FadeIn(imp), run_time=0.8)
        self.wait(max(0.3, DUR - 4.4))
