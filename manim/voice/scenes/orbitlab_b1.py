from manim import *
import numpy as np
from orbitlab_helpers import make_planet, make_moon, dotted_circle

# "Sami wants a moon to circle his planet. Just once, clean, and come
#  back around."
DUR = 7.2


class OrbitlabS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.play(FadeIn(planet, scale=0.9), run_time=1.4)
        moon = make_moon(c + np.array([3.0, 0.6, 0]), r=0.16)
        self.play(FadeIn(moon, shift=LEFT * 0.2), run_time=1.0)
        ring = dotted_circle(c, r=1.9)
        self.play(Create(ring), run_time=1.8,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 4.2)
