from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_shelf, shelf_top_y, floor_line,
                            glow, label, small_label)

# "Energy held by position. Owed motion, not yet collected. Potential
#  energy."
DUR = 6.1


class GravpeS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        shelf = make_shelf([0, 1.2, 0], width=2.6)
        book = make_book(scale=1.0).move_to([0, shelf_top_y(shelf) + 0.16, 0])
        self.add(fl, shelf, book)
        self.wait(0.5)

        gl = glow(book)
        self.play(FadeIn(gl), run_time=1.4)
        self.play(gl.animate.scale(1.06).set_opacity(1.0),
                  run_time=1.2, rate_func=rate_functions.there_and_back)

        sub = small_label("stored", [0, shelf_top_y(shelf) + 0.95, 0],
                          color="#F2D27A")
        big = label("potential energy", [0, -2.7, 0], size=34)
        self.play(FadeIn(sub), Write(big), run_time=1.3)
        self.wait(DUR - 4.4)
