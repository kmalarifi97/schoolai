from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_shelf, shelf_top_y, floor_line,
                            energy_bar, small_label)

# "But you spent work lifting it. If the work goes somewhere - where did
#  it go? The book isn't moving."
DUR = 8.1


class GravpeS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        shelf = make_shelf([1.4, 1.7, 0], width=2.4)
        book = make_book(scale=1.0).move_to([1.4, shelf_top_y(shelf) + 0.16, 0])
        self.add(fl, shelf, book)
        self.wait(0.5)

        # the work you did, as a bar on the left
        bar = energy_bar([-4.4, -3.2, 0], height=2.0)
        wlbl = small_label("work you did", [-4.4, 0.0, 0])
        self.play(GrowFromEdge(bar[1], DOWN), Create(bar[0]),
                  FadeIn(wlbl), run_time=1.4)

        # arrow pointing at the still book + question mark
        arr = Arrow([-2.6, 1.0, 0], book.get_left() + LEFT * 0.15,
                    color="#8C98A6", stroke_width=4, buff=0.1)
        q = Text("?", font="sans", font_size=60, color="#EAE4D5"
                 ).move_to([-0.5, 1.0, 0])
        self.play(GrowArrow(arr), run_time=1.0)
        self.play(FadeIn(q, scale=0.6), run_time=0.9)
        self.wait(DUR - 3.8)
