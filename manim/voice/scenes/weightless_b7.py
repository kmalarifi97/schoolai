from manim import *
import numpy as np
from weightless_helpers import (make_elevator, make_person, make_scale,
                                small_label)

# "That's weightlessness. Not the absence of gravity. The absence of
#  anything pushing back."
DUR = 7.8


class WeightlessS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        box_c = np.array([-1.6, 0.4, 0])
        elev = make_elevator(2.6, 3.4)
        scale = make_scale(1.0).move_to([0, -1.5, 0])
        person = make_person(0.95).move_to([0, -0.78, 0])
        car = VGroup(elev, scale, person).move_to(box_c)
        self.add(car)

        # gravity still acts (down arrow), but no normal force from floor
        g_arr = Arrow(box_c + np.array([0, 1.4, 0]),
                      box_c + np.array([0, 0.2, 0]),
                      color="#7FB8E8", stroke_width=5, buff=0,
                      max_tip_length_to_length_ratio=0.24)
        self.play(GrowArrow(g_arr), run_time=0.9)
        self.add(small_label("gravity: still on",
                             box_c + np.array([0, 1.9, 0]), size=20))

        phrase = Text("no push back", font="sans", font_size=40,
                      color="#EAE4D5").move_to([3.0, 0.3, 0])
        self.play(FadeIn(phrase), run_time=1.0)
        self.play(car.animate.shift(DOWN * 0.8),
                  g_arr.animate.shift(DOWN * 0.8),
                  run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.play(phrase.animate.set_opacity(0.25), run_time=1.0)
        self.wait(DUR - 5.5)
