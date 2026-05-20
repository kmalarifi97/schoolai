from manim import *
import numpy as np
from power_helpers import (simple_car, value_bar, small_label,
                           STAIR_COL, POWER_COL)

# "It's why a small engine and a big engine can move the same car the
#  same mile — but not in the same time."
DUR = 9.0


class PowerS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        y1, y2 = 1.4, -0.4
        startx, endx = -5.0, 4.4
        for y in (y1, y2):
            self.add(Line([startx, y - 0.32, 0], [endx + 0.6, y - 0.32, 0],
                          color=STAIR_COL, stroke_width=3))
        finish = DashedLine([endx + 0.55, 2.0, 0], [endx + 0.55, -1.0, 0],
                            color="#EAE4D5", stroke_width=3)
        c1 = simple_car([startx, y1, 0], scale=1.0)
        c2 = simple_car([startx, y2, 0], scale=1.0)
        l1 = small_label("big engine", [startx, y1 + 0.7, 0], size=22)
        l2 = small_label("small engine", [startx, y2 + 0.7, 0], size=22)
        self.add(finish)
        self.play(FadeIn(c1), FadeIn(c2), FadeIn(l1), FadeIn(l2),
                  run_time=0.9)
        l1.add_updater(lambda m: m.move_to(c1.get_center() + UP * 0.7))
        l2.add_updater(lambda m: m.move_to(c2.get_center() + UP * 0.7))

        # big engine finishes far sooner; small one still arrives
        self.play(c1.animate.move_to([endx, y1, 0]), run_time=1.6,
                  rate_func=rate_functions.ease_out_sine)
        self.play(c2.animate.move_to([endx, y2, 0]), run_time=2.6,
                  rate_func=rate_functions.linear)
        l1.clear_updaters()
        l2.clear_updaters()

        pb1 = value_bar(2.2, width=0.7, color=POWER_COL,
                        anchor=[-1.0, -2.9, 0], label="power")
        pb2 = value_bar(0.9, width=0.7, color=POWER_COL,
                        anchor=[1.0, -2.9, 0], label="power")
        self.play(GrowFromEdge(pb1.bar, DOWN), GrowFromEdge(pb2.bar, DOWN),
                  FadeIn(pb1[1]), FadeIn(pb2[1]), run_time=1.0)
        self.wait(max(0.3, DUR - 8.1))
