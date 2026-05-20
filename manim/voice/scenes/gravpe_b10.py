from manim import *
import numpy as np
from gravpe_helpers import make_book, floor_line, dashed_ref, label

# "That chosen line has a name. The reference level. You pick it. The
#  physics doesn't care which."
DUR = 7.5


class GravpeS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        book = make_book(scale=1.0).move_to([-1.4, 1.6, 0])
        self.add(fl, book)
        self.wait(0.4)

        ref_y = ValueTracker(-0.6)
        ref = always_redraw(
            lambda: dashed_ref(ref_y.get_value(), color="#8C98A6"))
        name = always_redraw(
            lambda: label("reference level",
                          [3.6, ref_y.get_value() + 0.32, 0],
                          color="#8C98A6", size=26))
        self.play(Create(ref), run_time=0.9)
        self.play(Write(name), run_time=1.1)
        self.wait(0.6)
        # slides freely up and down
        self.play(ref_y.animate.set_value(2.0), run_time=1.3)
        self.play(ref_y.animate.set_value(-2.9), run_time=1.5)
        self.wait(DUR - 5.8)
