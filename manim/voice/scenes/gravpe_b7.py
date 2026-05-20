from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_table, table_top_y, floor_line,
                            small_label)

# "Now a subtle question. The book on the table - does it have potential
#  energy?"
DUR = 6.7


class GravpeS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        table = make_table([0, -0.6, 0], top_width=3.0, leg_height=2.5)
        book = make_book(scale=1.0).move_to([0, table_top_y(table) + 0.16, 0])
        self.add(fl, table, book)
        self.wait(0.6)

        self.add(small_label("floor", [-5.2, -3.05, 0]))
        q = Text("?", font="sans", font_size=66, color="#EAE4D5"
                 ).move_to([2.6, 0.4, 0])
        self.play(FadeIn(q, scale=0.6), run_time=1.0)
        self.play(book.animate.shift(UP * 0.08), run_time=1.2,
                  rate_func=rate_functions.there_and_back)
        self.wait(DUR - 3.0)
