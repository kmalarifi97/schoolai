from manim import *
import numpy as np
from equivalence_helpers import (make_block, make_hand, frictionless_plane,
                                 push_arrow, small_label, INERT)

# "One is stubbornness. Push a thing; how hard is it to get moving?
#  That's inertial mass."
DUR = 7.7


class EquivalenceS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        plane = frictionless_plane(y=-1.4, x0=-6.4, x1=6.4)
        self.add(plane)
        block = make_block([-0.4, -0.75, 0], w=1.4, h=1.1)
        self.play(FadeIn(block), run_time=0.9)
        self.wait(0.4)
        hand = make_hand([-2.4, -0.75, 0], facing=RIGHT)
        arr = push_arrow([-1.55, -0.75, 0], length=0.85)
        self.play(FadeIn(hand), GrowArrow(arr), run_time=1.0)
        # the block resists: tiny shove, big effort
        self.play(hand.animate.shift(RIGHT * 0.55),
                  arr.animate.shift(RIGHT * 0.55),
                  block.animate.shift(RIGHT * 0.30),
                  run_time=1.8, rate_func=rate_functions.ease_out_quad)
        lbl = small_label("inertial mass", [0.0, 1.0, 0],
                          color=INERT, size=32)
        self.play(FadeIn(lbl, shift=UP * 0.2), run_time=1.0)
        self.wait(DUR - 5.1)
