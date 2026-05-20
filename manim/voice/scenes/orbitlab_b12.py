from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, make_moon, dotted_circle,
                              gravity_orbits_panel, small_label)

# "Before he clicks again — he builds it where he can see the pull and
#  the path."
DUR = 7.0


class OrbitlabS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        moon = make_moon(c + np.array([2.4, 0.6, 0]), r=0.16)
        ring = dotted_circle(c, r=1.9)
        self.add(planet, moon, ring)
        self.wait(0.6)

        # the sketch resolves into the PhET Gravity and Orbits layout
        panel = gravity_orbits_panel([0, -0.2, 0], scale=1.0)
        self.play(FadeOut(VGroup(planet, moon, ring)), run_time=1.0)
        self.play(FadeIn(panel.star, scale=0.9), run_time=1.0)
        self.play(FadeIn(panel.body), GrowArrow(panel.garrow),
                  run_time=1.0)
        self.play(Create(panel.trace), run_time=1.6)
        title = small_label("Gravity and Orbits", [0, 3.2, 0],
                            color="#8C8576", size=22)
        self.play(FadeIn(title), run_time=0.6)
        self.wait(DUR - 5.8)
