from manim import *
import numpy as np
from gfield_helpers import make_earth, radial_field, g_label

# "The field is the map of the influence. Computing the field strength
#  at a given distance from a mass, and the force it puts on an object
#  placed there — that's yours."
DUR = 12.7


class GfieldS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, -0.2, 0]
        earth = make_earth(C).scale(2.0)
        field = radial_field(C, body_radius=0.78, n_rings=4,
                             n_per_ring=15, ring_step=0.98)
        glbl = g_label([0, 3.0, 0], size=52)
        self.play(FadeIn(earth), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in field],
                              lag_ratio=0.008, run_time=2.4))
        self.play(Write(glbl), run_time=1.2)
        # the full map holds, then stills
        self.wait(DUR - 4.6)
