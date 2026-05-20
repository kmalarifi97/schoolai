from manim import *
import numpy as np
from weightless_helpers import make_earth, make_astronaut, make_station

# "Astronauts float. The easy explanation: there's no gravity up there."
DUR = 6.3


class WeightlessS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, -5.4, 0]).scale(7.0)
        station = make_station([1.6, 1.7, 0], scale=0.85)
        astro = make_astronaut([-1.8, 0.9, 0], scale=0.85, tilt=0.25)
        self.play(FadeIn(earth, run_time=1.2))
        self.play(FadeIn(station, shift=DOWN * 0.2, run_time=1.0))
        self.play(FadeIn(astro, scale=0.8, run_time=1.0))
        # gentle weightless drift
        self.play(astro.animate.shift(UP * 0.35 + LEFT * 0.25).rotate(0.15),
                  run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 5.2)
