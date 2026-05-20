from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_shelf, shelf_top_y, floor_line,
                            energy_bar, WORK_COL, small_label)

# "Higher means more stored. Lift it twice as high, it arrives carrying
#  twice as much."
DUR = 7.1


class GravpeS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        # low shelf (left) and high shelf (right, twice the height)
        lo = make_shelf([-3.4, -0.7, 0], width=1.9)
        hi = make_shelf([0.3, 2.0, 0], width=1.9)
        bk_lo = make_book(scale=0.85).move_to(
            [-3.4, shelf_top_y(lo) + 0.14, 0])
        bk_hi = make_book(scale=0.85).move_to(
            [0.3, shelf_top_y(hi) + 0.14, 0])
        self.add(fl, lo, hi, bk_lo, bk_hi)

        # stored bars sized to height above floor
        bar_lo = energy_bar([-1.6, -3.2, 0], height=1.1, color=WORK_COL)
        bar_hi = energy_bar([4.4, -3.2, 0], height=2.2, color=WORK_COL)
        self.play(GrowFromEdge(bar_lo[1], DOWN), Create(bar_lo[0]),
                  GrowFromEdge(bar_hi[1], DOWN), Create(bar_hi[0]),
                  run_time=1.4)
        self.add(small_label("stored", [-1.6, -3.55, 0], color=WORK_COL),
                 small_label("stored (2x)", [4.4, -3.55, 0], color=WORK_COL))
        self.wait(0.5)

        # both fall to compare
        self.play(bk_lo.animate.move_to([-3.4, -3.0, 0]),
                  bk_hi.animate.move_to([0.3, -3.0, 0]),
                  run_time=1.5, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 3.9)
