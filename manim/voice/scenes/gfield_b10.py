from manim import *
import numpy as np
from gfield_helpers import (make_earth, make_rock, field_arrow_at,
                            small_label)

# "Weight isn't a thing an object owns. It's the field, times the mass,
#  measured where the object happens to be."
DUR = 9.4


class GfieldS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -3.0, 0])
        earth = make_earth(C).scale(2.0)
        self.add(earth)

        low = np.array([-1.4, -0.6, 0])
        high = np.array([1.4, 2.0, 0])
        rock_lo = make_rock(7, scale=0.30).move_to(low)
        rock_hi = make_rock(7, scale=0.30).move_to(high)
        self.play(FadeIn(rock_lo), FadeIn(rock_hi), run_time=1.0)

        a_lo = field_arrow_at(C, low, body_radius=0.80)
        a_hi = field_arrow_at(C, high, body_radius=0.80)
        self.play(GrowArrow(a_lo), GrowArrow(a_hi), run_time=1.2)

        l1 = small_label("strong here", low + np.array([1.4, 0, 0]),
                         color="#8C98A6", size=22)
        l2 = small_label("weaker here", high + np.array([1.4, 0, 0]),
                         color="#8C98A6", size=22)
        self.play(FadeIn(l1), FadeIn(l2), run_time=1.0)
        self.wait(DUR - 4.2)
