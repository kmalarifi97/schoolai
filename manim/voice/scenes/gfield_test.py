from manim import *
import numpy as np
from gfield_helpers import (make_earth, make_rock, make_moon, radial_field,
                            field_arrow_at, g_label, down_arrow, small_label)


class GfieldTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([-3.2, 0, 0])
        field = radial_field([-3.2, 0, 0], body_radius=0.38, n_rings=3)
        glbl = g_label([-3.2, 2.4, 0])

        rock = make_rock(7, scale=0.32).move_to([1.2, 1.2, 0])
        arr = field_arrow_at([-3.2, 0, 0], [1.2, 1.2, 0], body_radius=0.38)

        moon = make_moon([3.8, -1.6, 0])
        mfield = radial_field([3.8, -1.6, 0], body_radius=0.26, n_rings=2,
                              ring_step=0.7)

        da = down_arrow([3.8, 1.8, 0], length=1.0)
        lbl = small_label("test", [3.8, 2.4, 0])

        self.add(earth, field, glbl, rock, arr, moon, mfield, da, lbl)
        self.wait(0.5)
