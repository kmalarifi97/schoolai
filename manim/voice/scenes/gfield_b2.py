from manim import *
import numpy as np
from gfield_helpers import make_earth, make_rock, small_label

# "But here's a strange question. How does the rock know the Earth is
#  there? They never touch."
DUR = 7.8


class GfieldS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, -2.6, 0]).scale(1.6)
        rock = make_rock(7, scale=0.34).move_to([0, 1.4, 0])
        self.add(earth, rock)
        self.wait(0.8)
        q = Text("?", font="sans", font_size=64, color="#EAE4D5"
                 ).move_to([0, -0.4, 0])
        self.play(FadeIn(q, scale=0.6), run_time=1.0)
        # gentle hover — paused mid-air
        self.play(rock.animate.shift(UP * 0.12), run_time=1.4,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.2)
