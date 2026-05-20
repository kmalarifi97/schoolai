from manim import *
import numpy as np
from gravpe_helpers import (make_book, floor_line, dashed_ref,
                            height_bracket, small_label)

# "So potential energy isn't an absolute. It's always measured from a
#  line you choose."
DUR = 7.1


class GravpeS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        book = make_book(scale=1.0).move_to([-1.2, 2.0, 0])
        self.add(fl, book)
        self.wait(0.4)

        ref_y = ValueTracker(-1.0)
        ref = always_redraw(
            lambda: dashed_ref(ref_y.get_value(), color="#8C98A6"))
        hb = always_redraw(
            lambda: height_bracket(1.6, ref_y.get_value(),
                                    book.get_center()[1], label="h"))
        self.play(Create(ref), run_time=0.9)
        self.play(GrowFromEdge(hb, DOWN), run_time=0.9)
        self.wait(0.5)
        # the chosen line moves -> the measured height changes
        self.play(ref_y.animate.set_value(-2.8), run_time=1.4)
        self.play(ref_y.animate.set_value(0.4), run_time=1.4)
        self.wait(DUR - 5.5)
