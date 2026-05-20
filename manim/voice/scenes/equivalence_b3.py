from manim import *
import numpy as np
from equivalence_helpers import (make_block, spring_scale, gravity_arrow,
                                 small_label, GRAV)

# "The other is heaviness. How strongly does gravity pull on it?
#  That's gravitational mass."
DUR = 7.8


class EquivalenceS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        spr, hp = spring_scale(top=np.array([0, 3.0, 0]), length=1.7)
        self.play(Create(spr), run_time=1.1)
        block = make_block(hp + np.array([0, -0.55, 0]), w=1.2, h=0.95)
        self.play(FadeIn(block, shift=DOWN * 0.2), run_time=0.8)
        # spring stretches a touch as it takes the weight
        self.play(block.animate.shift(DOWN * 0.22),
                  spr[1].animate.stretch(1.12, 1,
                      about_point=np.array([0, 3.0, 0])),
                  run_time=1.0, rate_func=rate_functions.ease_out_quad)
        arr = gravity_arrow(block.get_bottom() + np.array([0, -0.15, 0]),
                            length=1.0, color=GRAV)
        self.play(GrowArrow(arr), run_time=0.9)
        lbl = small_label("gravitational mass", [2.6, 0.2, 0],
                          color=GRAV, size=30)
        self.play(FadeIn(lbl), run_time=1.0)
        self.wait(DUR - 5.8)
