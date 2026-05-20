from manim import *
import numpy as np
from collisionlab_helpers import callback_cars_wall

# "And if this felt familiar — it should. Do you remember the two cars
#  at the wall, one that crumpled slowly and one that didn't?"
DUR = 10.6


class CollisionlabS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        # faint callback: two cars at a wall, crumple vs rigid
        cw = callback_cars_wall([0.4, 0.0, 0], scale=2.4,
                                opacity=0.0)
        self.play(cw.animate.set_opacity(0.85), run_time=1.6)
        # a small shudder at the wall — the crumple settling
        self.play(cw.animate.shift(LEFT * 0.10), run_time=0.5,
                  rate_func=rate_functions.there_and_back)
        self.wait(2.6)
        self.play(cw.animate.set_opacity(0.55), run_time=1.4)
        self.wait(DUR - 7.4)
