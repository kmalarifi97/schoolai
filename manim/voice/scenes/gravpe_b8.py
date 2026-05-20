from manim import *
import numpy as np
from gravpe_helpers import (make_book, make_table, table_top_y, floor_line,
                            dashed_ref, height_bracket, small_label)

# "Compared to the floor, yes - it could still fall. Compared to the
#  table top, no - it's already there."
DUR = 7.8


class GravpeS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fl = floor_line(y=-3.3)
        table = make_table([-0.6, -0.6, 0], top_width=3.0, leg_height=2.5)
        ty = table_top_y(table)
        book = make_book(scale=1.0).move_to([-0.6, ty + 0.16, 0])
        self.add(fl, table, book)
        self.wait(0.4)

        # reference at the floor -> has PE (height = book above floor)
        ref_floor = dashed_ref(-3.3, color="#7FB8E8")
        hb_floor = height_bracket(2.4, -3.3, ty + 0.16,
                                  color="#7FB8E8", label="h")
        self.play(Create(ref_floor), run_time=0.8)
        self.play(GrowFromEdge(hb_floor, DOWN), run_time=1.0)
        yes = small_label("vs floor: yes", [-3.7, 2.3, 0], color="#7FB8E8")
        self.play(FadeIn(yes), run_time=0.7)
        self.wait(0.8)

        # reference at the table top -> no PE (height = 0)
        ref_tbl = dashed_ref(ty + 0.16, color="#E8B45A")
        no = small_label("vs table top: no", [3.4, 2.3, 0],
                         color="#E8B45A")
        self.play(Create(ref_tbl), FadeIn(no), run_time=1.0)
        self.wait(DUR - 5.5)
