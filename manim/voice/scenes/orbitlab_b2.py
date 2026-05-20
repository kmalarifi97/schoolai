from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, dotted_circle,
                              spiral_in_path, escape_path)

# "One goal. One full lap. Not into the planet. Not off into the dark."
DUR = 6.3


class OrbitlabS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        ring = dotted_circle(c, r=1.9)
        self.play(Create(ring), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.4)
        # two failure ghosts, very faint
        sp = spiral_in_path(c, r0=2.4, r_end=0.85).set_opacity(0.22)
        esc = escape_path(c, r0=1.7).set_opacity(0.22)
        self.play(FadeIn(sp), FadeIn(esc), run_time=1.4)
        self.wait(DUR - 3.4)
