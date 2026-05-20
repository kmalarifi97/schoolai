from manim import *
import numpy as np
from gravpe_helpers import (make_book, floor_line, dashed_ref,
                            height_bracket, small_label)

# "Computing the gravitational potential energy from mass, gravity, and
#  height above your chosen reference - that's yours."
DUR = 10.1


class GravpeS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        ref = dashed_ref(-1.6, color="#8C98A6")
        book = make_book(scale=1.0).move_to([-0.8, 1.8, 0])
        self.add(fl)
        self.play(Create(ref), run_time=1.0)
        self.play(FadeIn(book, shift=DOWN * 0.15), run_time=1.0)

        hb = height_bracket(1.4, -1.6, 1.8, color="#8C98A6", label="h")
        self.play(GrowFromEdge(hb, DOWN), run_time=1.0)
        m = small_label("m", book.get_left() + LEFT * 0.4,
                        color="#EAE4D5", size=28)
        rlbl = small_label("chosen reference", [3.6, -1.6, 0],
                           color="#8C98A6", size=22)
        self.play(FadeIn(m), FadeIn(rlbl), run_time=1.0)
        # clean hold
        self.wait(DUR - 5.0)
