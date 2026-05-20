from manim import *
import numpy as np
from collisionlab_helpers import callback_lake_throw

# "And the figure on the frozen lake, who threw a bag and slid backward
#  — giving nothing away that the ice could keep?"
DUR = 9.8


class CollisionlabS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(0.8)
        # faint callback: frozen-lake figure + thrown bag
        lt = callback_lake_throw([0.0, 0.0, 0], scale=2.4,
                                 opacity=0.0)
        self.play(lt.animate.set_opacity(0.85), run_time=1.6)
        # the recoil: the whole scene drifts left a touch (figure slides
        # back as the bag goes forward)
        self.play(lt.animate.shift(LEFT * 0.4), run_time=1.6,
                  rate_func=rate_functions.ease_out_sine)
        self.wait(1.8)
        self.play(lt.animate.set_opacity(0.55), run_time=1.4)
        self.wait(DUR - 7.2)
