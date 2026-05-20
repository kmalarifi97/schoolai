from manim import *
import numpy as np
from equivalence_helpers import make_ball, frictionless_plane, small_label

# "— they land at the same instant. Always. Every time anyone has ever
#  checked."
DUR = 7.0


class EquivalenceS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground_y = -2.7
        ground = frictionless_plane(y=ground_y, x0=-6.4, x1=6.4)
        ground[2].set_opacity(0)  # hide the 'frictionless' tag here
        self.add(ground)
        y0 = 2.4
        heavy = make_ball([-1.8, y0, 0], radius=0.46, big=True)
        light = make_ball([1.8, y0, 0], radius=0.30, big=False)
        self.add(heavy, light)
        self.wait(0.5)
        # both reach the ground on the exact same frame
        rest_h = ground_y + 0.46
        rest_l = ground_y + 0.30
        self.play(heavy.animate.move_to([-1.8, rest_h, 0]),
                  light.animate.move_to([1.8, rest_l, 0]),
                  run_time=1.5, rate_func=rate_functions.ease_in_quad)
        flash = Line([-1.8, ground_y, 0], [1.8, ground_y, 0],
                     color="#EAE4D5", stroke_width=3).set_opacity(0.0)
        self.play(flash.animate.set_opacity(0.7), run_time=0.4,
                  rate_func=rate_functions.there_and_back)
        lbl = small_label("same instant", [0, 1.4, 0],
                          color="#EAE4D5", size=30)
        self.play(FadeIn(lbl), run_time=0.9)
        self.wait(DUR - 3.8)
