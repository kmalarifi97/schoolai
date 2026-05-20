from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, moon_dot,
                              closed_circle_path)

# "Then he presses play. And he watches the trace, not the moon."
DUR = 5.9


class OrbitlabS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.7)
        self.add(planet)
        circ = closed_circle_path(c, r=1.9, color="#9BD6B0", width=4)
        moon = moon_dot(circ.point_from_proportion(0.0)).set_opacity(0.4)
        self.add(moon)
        self.wait(0.5)
        # the trace draws itself as the (faint) moon goes round
        self.play(MoveAlongPath(moon, circ),
                  Create(circ),
                  run_time=3.4,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 3.9)
