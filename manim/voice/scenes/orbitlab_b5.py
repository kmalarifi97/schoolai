from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, dotted_circle,
                              spiral_in_path, moon_dot)

# "He eases off. It curves, hope rises — then sags inward and crashes
#  anyway."
DUR = 6.8


class OrbitlabS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        ring = dotted_circle(c, r=1.9)
        self.add(ring)
        # a hopeful arc that bends in, then decays into the planet
        path = spiral_in_path(c, r0=2.2, turns=0.92, r_end=0.85,
                              color="#C98A6B", start_angle=PI / 2)
        moon = moon_dot(path.point_from_proportion(0.0))
        self.add(moon)
        self.wait(0.5)
        self.play(MoveAlongPath(moon, path), run_time=3.0,
                  rate_func=rate_functions.ease_in_sine)
        self.play(Flash(moon, color="#C98A6B", flash_radius=0.4),
                  run_time=0.5)
        self.play(moon.animate.set_opacity(0.0), run_time=0.4)
        self.wait(DUR - 4.4)
