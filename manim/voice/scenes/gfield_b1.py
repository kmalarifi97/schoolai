from manim import *
import numpy as np
from gfield_helpers import make_earth, make_rock, down_arrow

# "Drop something. It falls. We say the Earth pulls it."
DUR = 5.5


class GfieldS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, -2.6, 0]).scale(1.6)
        rock = make_rock(7, scale=0.34).move_to([0, 2.2, 0])
        self.play(FadeIn(earth, run_time=1.0), FadeIn(rock, run_time=1.0))
        self.wait(0.6)
        arr = down_arrow([0, 1.55, 0], length=0.9)
        self.play(GrowArrow(arr), run_time=0.8)
        self.play(rock.animate.move_to([0, -1.55, 0]),
                  run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 4.0)
