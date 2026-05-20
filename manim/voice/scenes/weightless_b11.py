from manim import *
import numpy as np
from weightless_helpers import (make_earth, make_station, make_astronaut,
                                orbit_circle, point_on_circle, small_label)

# "That's an orbit. The station isn't escaping gravity. It's falling
#  around the Earth, forever, missing the ground."
DUR = 9.0


class WeightlessS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        earth = make_earth(C).scale(3.2)
        self.play(FadeIn(earth), run_time=1.0)

        R = 2.6
        orbit = orbit_circle(C, R, dashed=True)
        self.play(Create(orbit), run_time=1.4)

        th = PI / 2
        station = make_station(point_on_circle(C, R, th), scale=0.34)
        astro = make_astronaut(point_on_circle(C, R, th) + np.array([0, 0.0, 0]),
                               scale=0.26)
        grp = VGroup(station, astro)
        self.play(FadeIn(grp), run_time=0.8)
        self.add(small_label("falling around — never landing",
                             C + np.array([0, -R - 0.7, 0]), size=22))

        # the station "falls around" the Earth along the orbit
        def updater(m, alpha):
            a = th - alpha * TAU * 0.75
            m.move_to(point_on_circle(C, R, a))
        self.play(UpdateFromAlphaFunc(grp, updater), run_time=4.2,
                  rate_func=rate_functions.linear)
        self.wait(DUR - 7.4)
