from manim import *
import numpy as np
from gfield_helpers import make_earth, radial_field, g_label

# "That invisible influence has a name. The gravitational field. A
#  property of the space, not of the rock."
DUR = 8.6


class GfieldS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, 0, 0]).scale(2.2)
        field = radial_field([0, 0, 0], body_radius=0.84, n_rings=3,
                              n_per_ring=14, ring_step=1.05)
        self.add(earth, field)
        self.wait(0.8)
        glbl = g_label([0, 3.0, 0], size=52)
        self.play(Write(glbl), run_time=1.2)
        self.play(field.animate.set_opacity(1.0), run_time=0.8,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.3)
