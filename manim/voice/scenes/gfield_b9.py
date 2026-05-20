from manim import *
import numpy as np
from gfield_helpers import make_earth, radial_field

# "Far away, they thin out. Never quite zero. Just fainter, and
#  fainter."
DUR = 6.0


class GfieldS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, 0, 0]
        earth = make_earth(C).scale(1.6)
        field = radial_field(C, body_radius=0.60, n_rings=4,
                             n_per_ring=15, ring_step=0.95)
        grp = VGroup(earth, field)
        self.add(grp)
        self.wait(0.6)
        # camera pulls back: shrink everything, far arrows persist faint
        self.play(grp.animate.scale(0.5).move_to([0, 0, 0]),
                  run_time=2.4, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 3.0)
