from manim import *
import numpy as np
from thermolaws_helpers import coffee_mug, cross_out, small_label

# "A hot coffee always cools to the room. The room never
#  spontaneously reheats the coffee."
DUR = 7.3


class ThermolawsS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hot = coffee_mug([-3.0, 0, 0], scale=1.0, temp=1.0)
        rlbl = small_label("room", [-3.0, -1.6, 0], size=22,
                           color="#5C8AB0")
        self.play(FadeIn(hot), FadeIn(rlbl), run_time=1.0)
        self.wait(0.5)
        # cool toward the room
        cool = coffee_mug([-3.0, 0, 0], scale=1.0, temp=0.0)
        self.play(Transform(hot, cool), run_time=2.0)
        self.wait(0.4)
        # the reverse — room reheating the coffee — struck through
        rev = coffee_mug([3.0, 0, 0], scale=1.0, temp=1.0
                         ).set_opacity(0.45)
        rl2 = small_label("the reverse", [3.0, 1.9, 0], size=22,
                          color="#9B958A").set_opacity(0.6)
        self.play(FadeIn(rev), FadeIn(rl2), run_time=0.8)
        self.play(Create(cross_out(rev)), run_time=0.8)
        self.wait(DUR - 5.5)
