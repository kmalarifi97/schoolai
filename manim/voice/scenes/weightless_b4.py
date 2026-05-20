from manim import *
import numpy as np
from weightless_helpers import (make_elevator, make_person, make_scale,
                                make_cable, small_label)

# "Go back to Earth. An elevator. You stand on a scale. It reads your
#  weight."
DUR = 6.1


class WeightlessS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box_c = np.array([0, -0.4, 0])
        elev = make_elevator(2.6, 3.4).move_to(box_c)
        cable = make_cable([0, 3.6, 0], [0, 1.3, 0])
        self.play(Create(cable), FadeIn(elev), run_time=1.3)

        scale = make_scale(1.0).move_to(box_c + np.array([0, -1.5, 0]))
        person = make_person(0.95).move_to(box_c + np.array([0, -0.78, 0]))
        self.play(FadeIn(scale), run_time=0.6)
        self.play(FadeIn(person, shift=DOWN * 0.15), run_time=0.9)

        readout = small_label("70 kg", box_c + np.array([2.4, -1.5, 0]),
                              color="#EAE4D5", size=30)
        self.play(FadeIn(readout, scale=0.7), run_time=0.8)
        self.wait(DUR - 3.6)
