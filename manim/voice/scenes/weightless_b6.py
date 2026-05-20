from manim import *
import numpy as np
from weightless_helpers import (make_elevator, make_person, make_scale,
                                big_label, small_label)

# "The scale reads zero. Not because gravity stopped. Because the floor
#  is falling away exactly as fast as you are."
# visual: ... Bold 'ZERO'. [Hold 2s in silence]  -> after the action, the
# final frame is held an extra ~2s of stillness (NOT rendered as text).
BASE = 9.6
HOLD = 2.0
DUR = BASE + HOLD


class WeightlessS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box_c = np.array([-2.4, 0.6, 0])
        elev = make_elevator(2.6, 3.4)
        scale = make_scale(1.0).move_to([0, -1.5, 0])
        person = make_person(0.95).move_to([0, -0.78, 0])
        car = VGroup(elev, scale, person).move_to(box_c)
        self.add(car)
        self.wait(0.5)

        # person and floor fall in perfect lockstep — no relative motion
        # inside the car, so the scale never gets pressed.
        self.play(car.animate.shift(DOWN * 0.9 + RIGHT * 0.0),
                  run_time=1.8, rate_func=rate_functions.ease_in_quad)

        # scale readout placed clearly outside the elevator car
        readout = big_label("0", [0.4, -1.5, 0],
                            color="#EAE4D5", size=40)
        rlead = Line([-0.3, -1.6, 0], [0.1, -1.5, 0],
                     color="#7A828E", stroke_width=2).set_opacity(0.6)
        self.add(rlead)
        zero = big_label("ZERO", [2.7, 0.4, 0], color="#EAE4D5", size=66)
        self.play(FadeIn(readout, scale=0.6), run_time=0.7)
        self.play(Write(zero), run_time=1.1)
        self.add(small_label("floor falls with you",
                             [2.7, -0.8, 0], size=24))

        # remaining narration time
        self.wait(BASE - 4.6)
        # [Hold 2s in silence] — stillness on the final frame
        self.wait(HOLD)
