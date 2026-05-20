from manim import *
import numpy as np
from gfield_helpers import make_earth

# "So we change the picture. Instead of the Earth reaching out to grab
#  things —"
DUR = 6.2


class GfieldS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, 0, 0]).scale(2.2)
        self.play(FadeIn(earth, scale=0.85), run_time=1.4)
        self.play(earth.animate.scale(1.04), run_time=1.6,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.0)
