from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball,
                                masses_springs_panel)

# "Before he presses again — he builds it where he can see the energy
#  move."
DUR = 6.7


class SpringdropS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-3.0, -2.2, 0], height=1.6, compress=0.3)
        ball = make_ball(sp["top"] + UP * 0.22, r=0.24)
        self.add(sp["group"], ball)
        self.wait(0.6)

        panel = masses_springs_panel([0.4, -0.1, 0], stiffness=0.5,
                                      mass=0.5, elastic=0.6,
                                      kinetic=0.2, grav=0.1,
                                      scale=0.95)
        self.play(FadeOut(sp["group"]), FadeOut(ball), run_time=1.2)
        self.play(FadeIn(panel, shift=UP * 0.15), run_time=1.8)
        self.wait(DUR - 3.6)
