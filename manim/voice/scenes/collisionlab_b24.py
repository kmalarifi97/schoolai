from manim import *
import numpy as np
from collisionlab_helpers import callback_steel_clay, small_label

# "And the steel that bounced, and the clay that just stopped — same
#  momentum, different energy?"
DUR = 8.2


class CollisionlabS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        # faint callback: steel rebounding vs clay fusing
        sc = callback_steel_clay([0.0, 0.0, 0], scale=2.6,
                                 opacity=0.0)
        self.play(sc.animate.set_opacity(0.85), run_time=1.6)
        self.wait(2.4)
        self.play(sc.animate.set_opacity(0.55), run_time=1.4)
        self.wait(DUR - 6.2)
