from manim import *
import numpy as np
from centerofmass_helpers import make_L_shape, com_crosshair, small_label

# "It isn't always in the middle of the object. It isn't even always
#  inside the object."
DUR = 6.9


class CenterofmassS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        Lsh, com = make_L_shape(scale=0.95, center=[-0.4, -0.4, 0])
        self.play(FadeIn(Lsh), run_time=1.0)
        self.wait(0.5)
        ch = com_crosshair(com, scale=1.05)
        self.play(Create(ch), run_time=1.1)
        # stress that it sits in the empty notch, outside the metal
        self.play(ch.animate.scale(1.18), run_time=0.7,
                  rate_func=rate_functions.there_and_back)
        lbl = small_label("outside the metal", [com[0] + 2.4, com[1], 0],
                          size=26)
        self.play(FadeIn(lbl, shift=LEFT * 0.2), run_time=1.0)
        self.wait(DUR - 4.8)
