from manim import *
import numpy as np
from springdrop_helpers import callback_pendulum, small_label

# "And the pendulum that never lost a thing — only kept trading it,
#  back and forth?"
DUR = 7.3


class SpringdropS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        pend = callback_pendulum([0, 1.4, 0], scale=1.9, opacity=0.0,
                                 theta=0.6)
        self.play(pend.animate.set_opacity(0.9), run_time=1.2)
        pivot = [0, 1.4 + 0.95 * 1.9 / 2, 0]
        # trade back and forth, losing nothing
        self.play(Rotate(pend, angle=-1.1, about_point=pivot),
                  run_time=1.3,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(Rotate(pend, angle=1.1, about_point=pivot),
                  run_time=1.3,
                  rate_func=rate_functions.ease_in_out_sine)
        cap = small_label("conservation — only traded",
                          [0, -1.8, 0], size=22, color="#8C8576")
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 5.4)
