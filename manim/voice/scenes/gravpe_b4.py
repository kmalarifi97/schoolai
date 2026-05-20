from manim import *
import numpy as np
from gravpe_helpers import (make_book, floor_line, energy_bar, set_bar,
                            WORK_COL, SPEED_COL, small_label)

# "The motion it didn't have up top, it has now. The work you did was
#  stored, waiting, the whole time."
DUR = 7.5


class GravpeS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        self.add(fl)

        # the earlier work bar (blue, left), full
        work = energy_bar([-4.4, -3.2, 0], height=2.3, color=WORK_COL)
        wlbl = small_label("work you did", [-4.4, -0.4, 0], color=WORK_COL)
        # the falling book's speed bar (amber, right), empty
        sp_anchor = np.array([4.4, -3.2, 0])
        sp_frame = Rectangle(width=0.34, height=2.6, stroke_color=SPEED_COL,
                             stroke_width=2.0, fill_opacity=0)
        sp_frame.move_to(sp_anchor + np.array([0, 1.3, 0]))
        sp_fill = set_bar(None, 0.0, sp_anchor, color=SPEED_COL)
        slbl = small_label("motion now", [4.4, -0.4, 0], color=SPEED_COL)
        book = make_book(scale=1.0).move_to([0.4, 1.4, 0])
        self.add(work, wlbl, sp_frame, sp_fill, slbl, book)
        self.wait(0.6)

        # work pours into speed as the book falls
        tr = ValueTracker(0.0)

        def upd_book(m):
            p = tr.get_value()
            m.move_to([0.4, 1.4 - 4.1 * (p * p), 0])
        book.add_updater(upd_book)

        def upd_work(m):
            p = tr.get_value()
            m.become(set_bar(None, 2.3 * (1 - p), np.array([-4.4, -3.2, 0]),
                             color=WORK_COL))
        work[1].add_updater(upd_work)

        def upd_sp(m):
            p = tr.get_value()
            m.become(set_bar(None, 2.3 * p, sp_anchor, color=SPEED_COL))
        sp_fill.add_updater(upd_sp)

        self.play(tr.animate.set_value(1.0), run_time=2.4,
                  rate_func=rate_functions.ease_in_quad)
        for m in (book, work[1], sp_fill):
            m.clear_updaters()
        self.wait(DUR - 3.6)
