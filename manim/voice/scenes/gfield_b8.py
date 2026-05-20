from manim import *
import numpy as np
from gfield_helpers import make_earth, radial_field

# "Closer to the Earth, the arrows crowd together. The field is
#  stronger."
DUR = 6.2


class GfieldS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, -0.4, 0]
        earth = make_earth(C).scale(1.9)
        field = radial_field(C, body_radius=0.72, n_rings=3,
                             n_per_ring=16, ring_step=1.0)
        self.add(earth)
        self.play(LaggedStart(*[GrowArrow(a) for a in field],
                              lag_ratio=0.01, run_time=2.2))
        # pulse the dense inner ring to stress "stronger"
        inner = VGroup(*field[:16])
        self.play(inner.animate.set_opacity(1.0).scale(1.05),
                  run_time=1.0, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.6)
