from manim import *
import numpy as np
from gravpe_helpers import (make_book, dashed_ref, energy_bar, SPEED_COL,
                            REF_COL, small_label)

# "Only the change in height matters - how far it actually falls. Set
#  your reference at the floor, the table, or the roof: the fall distance
#  stays the same, so the energy released is identical."
DUR = 14.8


class GravpeS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Three side-by-side panels. World geometry is identical in all
        # three: book starts at the SAME absolute height, falls the SAME
        # 2 m. Only the dashed reference line differs (floor / table /
        # roof). Released-energy bar (= m g * delta_h) is identical.
        centers_x = [-4.3, 0.0, 4.3]
        titles = ["reference: floor", "reference: table",
                  "reference: roof"]
        # absolute y of start and end of the fall (same everywhere)
        y_start = 2.0          # release height
        y_end = -0.2           # after a 2 m drop
        # reference line per panel (floor below, table at end, roof above)
        ref_ys = [-1.4, y_end, 3.0]

        panels = VGroup()
        for cx, title, ref_y in zip(centers_x, titles, ref_ys):
            panel = VGroup()
            # short ground tick under each panel
            ground = Line([cx - 1.45, -2.7, 0], [cx + 1.45, -2.7, 0],
                          color="#5A4836", stroke_width=3)
            ttl = small_label(title, [cx, 3.5, 0], color="#EAE4D5", size=22)

            # reference dashed line (clipped to this panel's width)
            ref = DashedLine([cx - 1.55, ref_y, 0], [cx + 1.55, ref_y, 0],
                             color=REF_COL, stroke_width=2.4,
                             dash_length=0.14, dashed_ratio=0.55)
            ref.set_opacity(0.9)
            rlbl = small_label("ref", [cx + 1.95, ref_y, 0],
                               color=REF_COL, size=18)

            # the book at the SAME start height in every panel
            book = make_book(scale=0.62).move_to([cx, y_start, 0])

            # the 2 m fall bracket (same length everywhere)
            drop = DoubleArrow([cx - 1.05, y_start, 0],
                               [cx - 1.05, y_end, 0], color="#8C98A6",
                               buff=0, stroke_width=2.5,
                               max_tip_length_to_length_ratio=0.10,
                               tip_length=0.14)
            dlbl = small_label("2 m", [cx - 1.45, (y_start + y_end) / 2, 0],
                               color="#8C98A6", size=18)

            panel.add(ground, ttl, ref, rlbl, book, drop, dlbl)
            panel.book = book
            panels.add(panel)
            panel.start = y_start
            panel.end = y_end
            panel.cx = cx

        self.play(LaggedStart(*[FadeIn(p) for p in panels],
                              lag_ratio=0.25, run_time=2.4))
        self.wait(0.8)

        # all three books fall the same 2 m, together
        anims = []
        for p in panels:
            anims.append(p.book.animate.move_to([p.cx, p.end, 0]))
        self.play(*anims, run_time=1.6,
                  rate_func=rate_functions.ease_in_quad)
        self.wait(0.5)

        # identical released-energy bar appears under each panel
        bars = VGroup()
        for p in panels:
            b = energy_bar([p.cx, -2.6, 0], height=1.7, max_height=1.9,
                           width=0.30, color=SPEED_COL)
            bars.add(b)
        self.play(*[AnimationGroup(GrowFromEdge(b[1], DOWN), Create(b[0]))
                    for b in bars], run_time=1.4)
        eq = small_label("energy released: identical", [0, -3.4, 0],
                         color=SPEED_COL, size=24)
        self.play(FadeIn(eq), run_time=0.9)
        self.wait(DUR - 8.6)
