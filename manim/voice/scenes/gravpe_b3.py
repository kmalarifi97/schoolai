from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_shelf, shelf_top_y, floor_line,
                            set_bar, SPEED_COL, small_label)

# "Nudge it off the edge and you find out. It falls - and arrives moving
#  fast."
DUR = 6.3


class GravpeS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        shelf = make_shelf([-1.0, 1.7, 0], width=2.4)
        rest_y = shelf_top_y(shelf) + 0.16
        book = make_book(scale=1.0).move_to([-1.0, rest_y, 0])
        self.add(fl, shelf, book)

        # growing speed bar on the right tied to fall
        anchor = np.array([4.6, -3.2, 0])
        bar_frame = Rectangle(width=0.34, height=2.4, stroke_color=SPEED_COL,
                              stroke_width=2.0, fill_opacity=0)
        bar_frame.move_to(anchor + np.array([0, 1.2, 0]))
        fill = set_bar(None, 0.0, anchor, color=SPEED_COL)
        slbl = small_label("speed", anchor + np.array([0, 2.9, 0]),
                           color=SPEED_COL)
        self.add(bar_frame, fill, slbl)

        self.wait(0.5)
        # nudge off edge
        self.play(book.animate.shift(RIGHT * 0.55), run_time=0.6)

        y0, y1 = rest_y, -2.95
        tracker = ValueTracker(0.0)

        def upd_book(m):
            p = tracker.get_value()
            m.move_to([-0.45, y0 + (y1 - y0) * (p * p), 0])
        book.add_updater(upd_book)

        def upd_fill(m):
            p = tracker.get_value()
            m.become(set_bar(None, 2.3 * p, anchor, color=SPEED_COL))
        fill.add_updater(upd_fill)

        self.play(tracker.animate.set_value(1.0), run_time=1.6,
                  rate_func=rate_functions.linear)
        book.clear_updaters()
        fill.clear_updaters()
        self.wait(DUR - 4.3)
