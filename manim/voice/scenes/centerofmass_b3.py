from manim import *
import numpy as np
from centerofmass_helpers import make_wrench, com_dot, com_label

# "That point moves as if all the mass were squeezed into it.
#  The center of mass."
DUR = 7.0


class CenterofmassS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        P = [0, 0.4, 0]
        wr = make_wrench(scale=0.72).rotate(0.4).move_to(P)
        cd = com_dot(P, scale=1.1)
        self.add(wr, cd)
        self.wait(0.6)
        # the rest of the wrench dims; the point stays
        self.play(wr.animate.set_opacity(0.18), run_time=1.6)
        self.play(cd.animate.scale(1.15), run_time=0.8,
                  rate_func=rate_functions.there_and_back)
        lbl = com_label([0, -1.4, 0], size=30)
        self.play(Write(lbl), run_time=1.2)
        self.wait(DUR - 4.8)
