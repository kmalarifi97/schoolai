from manim import *
import numpy as np
from gfield_helpers import make_earth, radial_field

# "— the Earth changes the space around it. Everywhere. Whether anything
#  is there to feel it or not."
DUR = 7.8


class GfieldS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, 0, 0]).scale(2.2)
        self.add(earth)
        field = radial_field([0, 0, 0], body_radius=0.84, n_rings=3,
                              n_per_ring=14, ring_step=1.05)
        self.wait(0.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in field],
                              lag_ratio=0.012, run_time=2.6))
        self.wait(DUR - 3.1)
