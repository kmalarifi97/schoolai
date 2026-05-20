from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, make_moon, gravity_arrow,
                              straight_arrow, closed_circle_path)

# "And the moon, left alone, only wants to go straight. An orbit is
#  those two, matched."
DUR = 7.5


class OrbitlabS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        mpos = c + np.array([0.0, 1.9, 0])
        moon = make_moon(mpos, r=0.16)
        self.add(moon)

        # straight-line tendency first
        sa = straight_arrow(mpos, [1, 0, 0], length=1.1,
                            color="#E8C46B")
        self.play(GrowArrow(sa), run_time=1.0)
        self.wait(0.4)
        # inward pull
        ga = gravity_arrow(mpos, c, length=0.95, color="#D98C5F")
        self.play(GrowArrow(ga), run_time=1.0)
        self.wait(0.4)
        # the two combine tangentially into a closed curve
        circ = closed_circle_path(c, r=1.9, color="#9BD6B0", width=4)
        self.play(Create(circ), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 5.0)
