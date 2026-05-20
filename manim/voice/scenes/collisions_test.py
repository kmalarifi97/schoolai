from manim import *
import numpy as np
from collisions_helpers import (
    make_cart, steel_ball, clay_blob, fused_blob, momentum_bar,
    energy_bar, split_bar, shimmer, checklist, slider, qmark,
    speed_arrow, title, small_label)


class CollisionsTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(make_cart([-5.0, 2.4, 0]))
        self.add(steel_ball([-3.2, 2.4, 0]))
        self.add(clay_blob([-1.6, 2.4, 0], seed=3))
        self.add(fused_blob([0.6, 2.4, 0], seed=9))
        self.add(qmark([2.6, 2.4, 0]))
        self.add(speed_arrow([3.6, 2.4, 0], [1.2, 0, 0]))

        self.add(momentum_bar([-3.4, 0.6, 0]))
        self.add(energy_bar([1.2, 0.4, 0], frac=0.9))
        self.add(energy_bar([2.6, 0.4, 0], frac=0.3))
        self.add(split_bar([-3.0, -1.6, 0], useful_frac=0.4))
        self.add(shimmer(np.array([3.4, -1.0, 0]), spread=1.0))

        self.add(slider([-3.0, -3.0, 0], width=4.0, knob_frac=0.55))
        self.add(checklist([3.0, -2.6, 0], [
            ("momentum", True, "always"),
            ("kinetic", False, "elastic only"),
        ]))
        self.add(title("Collisions", [0, 3.6, 0], size=30))
        self.wait(0.3)
