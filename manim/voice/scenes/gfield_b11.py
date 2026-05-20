from manim import *
import numpy as np
from gfield_helpers import (make_earth, make_moon, make_rock,
                            field_arrow_at, small_label)

# "Same rock. Different field. Different weight. Move it to the Moon and
#  the arrows are weaker — the rock didn't change."
DUR = 9.4


class GfieldS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        EC = np.array([-3.4, -1.2, 0])
        MC = np.array([3.4, -1.2, 0])
        earth = make_earth(EC).scale(1.7)
        moon = make_moon(MC, scale=2.4)
        self.add(earth, moon)
        small_label("Earth", EC + np.array([0, 2.0, 0]),
                    color="#8C98A6", size=22)
        self.add(small_label("Earth", EC + np.array([0, 1.7, 0]),
                             color="#8C98A6", size=22),
                 small_label("Moon", MC + np.array([0, 1.7, 0]),
                             color="#8C98A6", size=22))

        rpos_e = EC + np.array([1.7, 1.0, 0])
        rock = make_rock(7, scale=0.30).move_to(rpos_e)
        a_e = field_arrow_at(EC, rpos_e, body_radius=0.65)
        self.play(FadeIn(rock), GrowArrow(a_e), run_time=1.2)
        self.wait(0.8)

        rpos_m = MC + np.array([-1.7, 1.0, 0])
        a_m = field_arrow_at(MC, rpos_m, body_radius=0.62)
        self.play(rock.animate.move_to(rpos_m), FadeOut(a_e),
                  run_time=1.8)
        self.play(GrowArrow(a_m), run_time=0.9)
        self.wait(DUR - 5.7)
