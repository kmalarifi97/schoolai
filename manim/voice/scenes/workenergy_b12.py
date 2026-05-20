from manim import *
import numpy as np
from workenergy_helpers import big_label, small_label

# "Computing the net work on an object and equating it to the change in
#  its kinetic energy to find a final speed — that's yours."
DUR = 9.6


class WorkenergyS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        eq = big_label("net work  =  change in energy of motion",
                       [0, 0.5, 0], color="#EAE4D5", size=34)
        eq.scale_to_fit_width(11.0)
        self.play(Write(eq), run_time=1.6)
        self.wait(0.8)

        hint = small_label("solve for the final speed — that's yours",
                           [0, -1.6, 0], color="#8C98A6", size=26)
        self.play(FadeIn(hint, run_time=1.0))
        self.wait(DUR - 4.4)
