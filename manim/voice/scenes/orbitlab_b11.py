from manim import *
import numpy as np
from orbitlab_helpers import curved_ground_inset, small_label

# "It is the same thing as throwing a ball so fast the ground keeps
#  curving away beneath it."
DUR = 7.9


class OrbitlabS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        inset = curved_ground_inset([0, -0.6, 0], scale=1.5)
        ground, arc, ball = inset
        self.play(Create(ground), run_time=1.2)
        self.wait(0.3)
        self.play(MoveAlongPath(ball, arc),
                  Create(arc),
                  run_time=2.6,
                  rate_func=rate_functions.ease_in_out_sine)
        cap = small_label("the ground keeps curving away",
                          [0, -2.6, 0], color="#8C8576", size=22)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 4.9)
