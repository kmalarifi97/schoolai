from manim import *
import numpy as np
from collisions_helpers import (steel_ball, energy_bar, make_energy_fill,
                                small_label)

# "Two steel balls click and bounce apart, lively as before."
DUR = 5.53


class CollisionsS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b1 = steel_ball([-4.0, 0.4, 0])
        b2 = steel_ball([4.0, 0.4, 0])
        eb = energy_bar([5.4, 0.0, 0], frac=0.95, label="motion energy")
        self.add(eb)
        self.play(FadeIn(b1), FadeIn(b2), run_time=0.8)

        self.play(b1.animate.move_to([-0.5, 0.4, 0]),
                  b2.animate.move_to([0.5, 0.4, 0]),
                  run_time=1.1, rate_func=rate_functions.linear)
        click = Text("click", font="sans", font_size=24, color="#EAE4D5"
                     ).move_to([0, 1.4, 0])
        self.play(FadeIn(click, shift=UP * 0.2), run_time=0.3)
        # rebound — nearly all motion kept
        new_fill = make_energy_fill(eb, 0.88)
        self.play(b1.animate.move_to([-3.6, 0.4, 0]),
                  b2.animate.move_to([3.6, 0.4, 0]),
                  Transform(eb[1], new_fill),
                  FadeOut(click),
                  run_time=1.3, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 3.5)
