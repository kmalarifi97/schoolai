from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, dotted_circle,
                              radial_fall_path, moon_dot)

# "He releases it gently. It falls straight in and hits the planet."
DUR = 6.1


class OrbitlabS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        ring = dotted_circle(c, r=1.9)
        self.add(ring)
        start = c + np.array([2.6, 0.7, 0])
        moon = moon_dot(start)
        self.add(moon)
        self.wait(0.6)
        path = radial_fall_path(start, c, planet_r=0.85, color="#C98A6B")
        self.play(MoveAlongPath(moon, path), run_time=1.8,
                  rate_func=rate_functions.ease_in_quad)
        self.play(Flash(moon, color="#C98A6B", flash_radius=0.4),
                  run_time=0.6)
        self.play(moon.animate.set_opacity(0.0), run_time=0.4)
        self.wait(DUR - 3.4)
