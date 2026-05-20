from manim import *
import numpy as np
from elasticpe_helpers import (make_spring, wall_block, spring_mass,
                               small_label)

# "Finding how the stored elastic energy depends on the spring's
#  stiffness and how far it's deformed — that's yours."
DUR = 9.6


class ElasticpeS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wx = -3.4
        wall = wall_block([wx, 0.2, 0], h=1.7)
        rest_x = -1.0
        stretched_x = 1.8
        spring = make_spring([wx + 0.15, 0.2, 0], [rest_x, 0.2, 0],
                             coils=11, amp=0.30)
        mass = spring_mass([rest_x + 0.3, 0.2, 0], r=0.30)
        self.play(FadeIn(wall), Create(spring), FadeIn(mass),
                  run_time=1.3)
        self.wait(0.3)

        # deform by x, leave x as an open symbol
        new_spring = make_spring([wx + 0.15, 0.2, 0],
                                 [stretched_x, 0.2, 0],
                                 coils=11, amp=0.30)
        new_mass = spring_mass([stretched_x + 0.3, 0.2, 0], r=0.30)
        self.play(Transform(spring, new_spring),
                  Transform(mass, new_mass),
                  run_time=1.4, rate_func=rate_functions.ease_in_out_sine)

        brace = DoubleArrow([rest_x + 0.3, -0.9, 0],
                            [stretched_x + 0.3, -0.9, 0],
                            color="#8C98A6", stroke_width=3,
                            buff=0, tip_length=0.16)
        x_sym = Text("x", font="sans", font_size=42, color="#EAE4D5",
                     slant=ITALIC).move_to([1.05, -1.5, 0])
        self.play(GrowFromCenter(brace), FadeIn(x_sym), run_time=1.1)
        # holds, clean
        self.wait(DUR - 5.1)
