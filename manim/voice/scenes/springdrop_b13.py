from manim import *
import numpy as np
from springdrop_helpers import (make_spring, hold_hand,
                                masses_springs_panel, small_label)

# "Here is the real job. Not releasing the spring. Predicting — before
#  he does."
DUR = 7.0


class SpringdropS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        panel = masses_springs_panel([0.4, -0.1, 0], stiffness=0.6,
                                      mass=0.5, elastic=0.85,
                                      kinetic=0.0, grav=0.0,
                                      scale=0.9)
        self.add(panel)

        # a hand deliberately holding the compressed spring
        hand = hold_hand([-3.0, -1.5, 0], scale=1.0)
        self.play(FadeIn(hand, shift=LEFT * 0.2), run_time=1.2)
        cap = small_label("predict — before releasing",
                          [0.4, 2.8, 0], size=24, color="#EAE4D5")
        self.play(FadeIn(cap), run_time=1.0)
        self.wait(DUR - 2.2)
