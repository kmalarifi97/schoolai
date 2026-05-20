from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, dotted_circle, moon_dot)

# "So he throws it harder. Now it tears away in a straight line and
#  never comes back."
DUR = 7.4


class OrbitlabS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        ring = dotted_circle(c, r=1.9)
        self.add(ring)
        start = c + np.array([0.0, 1.9, 0])
        moon = moon_dot(start)
        self.add(moon)
        self.wait(0.5)
        # a near-straight escape: barely bends, then leaves frame
        pts = []
        for i in range(61):
            t = i / 60
            ang = PI / 2 - 0.55 * t
            r = 1.9 * (1.0 + 3.0 * t * t)
            pts.append(c + np.array([r * np.cos(ang),
                                     r * np.sin(ang), 0]))
        path = VMobject().set_points_smoothly(pts)
        path.set_stroke("#C98A6B", width=4)
        self.add(path)
        self.play(MoveAlongPath(moon, path), run_time=2.6,
                  rate_func=rate_functions.ease_in_quad)
        self.play(moon.animate.set_opacity(0.0), run_time=0.4)
        self.wait(DUR - 4.0)
