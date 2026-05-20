from manim import *
import numpy as np
from gravpe_helpers import make_book, make_shelf, shelf_top_y, floor_line

# "Lift a book onto a high shelf. It just sits there. Still. Doing nothing."
DUR = 6.5


class GravpeS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        shelf = make_shelf([0, 1.7, 0], width=2.6)
        self.add(fl, shelf)
        rest_y = shelf_top_y(shelf) + 0.16
        book = make_book(scale=1.0).move_to([0, -2.85, 0])
        self.play(FadeIn(book, shift=UP * 0.2), run_time=0.9)
        self.play(book.animate.move_to([0, rest_y, 0]),
                  run_time=2.0, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 3.6)
