from manim import *
import numpy as np
from springdrop_helpers import masses_springs_panel, small_label

# "Masses and Springs. He sets the spring stiffness and the mass.
#  Turns the energy bars on."
DUR = 7.8


class SpringdropS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        panel = masses_springs_panel([0.4, -0.1, 0], stiffness=0.35,
                                      mass=0.4, elastic=0.0,
                                      kinetic=0.0, grav=0.0,
                                      scale=0.95)
        title = small_label("Masses and Springs", [0, 3.0, 0],
                            size=26, color="#EAE4D5")
        self.add(panel)
        self.play(FadeIn(title), run_time=1.0)

        # nudge stiffness + mass sliders
        s1, s2 = panel[1], panel[2]
        self.play(s1.knob.animate.shift(RIGHT * 0.5),
                  s2.knob.animate.shift(RIGHT * 0.4), run_time=1.6)

        # bars come on
        lit = masses_springs_panel([0.4, -0.1, 0], stiffness=0.6,
                                    mass=0.6, elastic=0.7,
                                    kinetic=0.0, grav=0.0,
                                    scale=0.95)
        self.play(Transform(panel.bars, lit.bars), run_time=1.6)
        self.wait(DUR - 4.2)
