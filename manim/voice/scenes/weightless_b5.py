from manim import *
import numpy as np
from weightless_helpers import (make_elevator, make_person, make_scale,
                                make_cable, small_label)

# "Now cut the cable. Elevator, scale, and you — all falling together."
DUR = 6.0


class WeightlessS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box_c = np.array([0, 1.4, 0])
        elev = make_elevator(2.6, 3.4)
        scale = make_scale(1.0).move_to([0, -1.5, 0])
        person = make_person(0.95).move_to([0, -0.78, 0])
        car = VGroup(elev, scale, person).move_to(box_c)
        cable_intact = make_cable([0, 5.0, 0], box_c + np.array([0, 1.7, 0]))
        self.add(car, cable_intact)
        self.wait(0.5)

        # snap the cable
        cable_broken = make_cable([0, 5.0, 0], box_c + np.array([0, 1.7, 0]),
                                  broken=True)
        self.play(Transform(cable_intact, cable_broken), run_time=0.5)
        self.add(small_label("cut", [1.4, 3.0, 0], color="#C8807F",
                             size=24))
        # everything falls together, accelerating
        self.play(car.animate.shift(DOWN * 4.4),
                  cable_intact.animate.shift(DOWN * 0.3),
                  run_time=2.6, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 3.6)
