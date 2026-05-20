from manim import *
import numpy as np
from gfield_helpers import (make_earth, radial_field, make_rock,
                            field_arrow_at, g_label)

# "The rock doesn't reach out to the Earth. It just responds to the
#  field it's sitting in. Right here. Locally."
DUR = 9.0


class GfieldS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-2.0, 0, 0])
        earth = make_earth(C).scale(1.9)
        field = radial_field(C, body_radius=0.72, n_rings=3,
                             n_per_ring=13, ring_step=1.0)
        glbl = g_label([-2.0, 3.0, 0], size=44)
        self.add(earth, field, glbl)
        self.wait(0.6)

        pos = np.array([2.6, 1.2, 0])
        rock = make_rock(13, scale=0.32).move_to(pos)
        self.play(FadeIn(rock, scale=0.7), run_time=1.0)
        # local field arrow at the rock — start just outside the rock
        u = (C - pos) / np.linalg.norm(C - pos)
        tail = pos + u * 0.42
        head = tail + u * 1.25
        local = Arrow(tail, head, color="#7FB8E8", stroke_width=5,
                      buff=0, max_tip_length_to_length_ratio=0.26)
        ring = Circle(radius=0.50, color="#7FB8E8", stroke_width=2,
                      fill_opacity=0).move_to(pos).set_opacity(0.6)
        self.play(Create(ring), GrowArrow(local), run_time=1.2)
        # it follows the local arrow
        self.play(rock.animate.shift(u * 0.9),
                  ring.animate.shift(u * 0.9),
                  run_time=1.4, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 4.8)
