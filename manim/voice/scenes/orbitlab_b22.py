from manim import *
import numpy as np
from orbitlab_helpers import callback_field, small_label

# "And the Earth that changed the space around it — arrows crowding
#  inward, everywhere, whether anything was there to feel them or not?"
DUR = 11.0


class OrbitlabS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.0)
        field = callback_field([0, 0.1, 0], scale=1.8, opacity=0.0)
        arrows, earth = field[0], field[1]
        self.play(field.animate.set_opacity(0.9), run_time=1.6)
        self.wait(0.4)
        # the field arrows pulse inward — present everywhere
        self.play(arrows.animate.set_opacity(0.45), run_time=1.0)
        self.play(arrows.animate.set_opacity(0.9), run_time=1.0)
        cap = small_label("the space itself — changed",
                          [0, -2.6, 0], color="#8C8576", size=22)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 6.8)
