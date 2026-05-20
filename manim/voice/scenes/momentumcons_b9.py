from manim import *
import numpy as np
from momentumcons_helpers import (make_rocket, exhaust_plume,
                                  momentum_bar, label, PLUS_COL,
                                  MINUS_COL)

# "It's how a rocket climbs. Throw exhaust down hard; the rocket is
#  thrown up just as hard."
DUR = 8.3


class MomentumconsS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rk = make_rocket((-2.4, -0.6, 0), scale=1.0)
        self.play(FadeIn(rk, scale=0.8), run_time=1.0)
        self.wait(0.4)

        # exhaust thrown down hard
        ex = exhaust_plume((-2.4, -1.6, 0), scale=1.0)
        ex_arrow = Arrow([-2.4, -2.0, 0], [-2.4, -3.0, 0],
                         color=MINUS_COL, stroke_width=6, buff=0,
                         max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(ex), GrowArrow(ex_arrow), run_time=1.1)

        # rocket thrown up just as hard
        up_arrow = Arrow([-2.4, 0.6, 0], [-2.4, 1.9, 0], color=PLUS_COL,
                         stroke_width=6, buff=0,
                         max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(up_arrow),
                  rk.animate.shift(UP * 0.5), run_time=1.3)

        # the two momenta balancing, side by side
        origin = (3.0, 0, 0)
        from momentumcons_helpers import zero_line
        zl = zero_line((3.0, 0, 0), height=3.2)
        pu = Rectangle(width=0.46, height=1.5, fill_color=PLUS_COL,
                       fill_opacity=0.9, stroke_color=PLUS_COL,
                       stroke_width=2).move_to([3.0, 0.85, 0])
        pd = Rectangle(width=0.46, height=1.5, fill_color=MINUS_COL,
                       fill_opacity=0.9, stroke_color=MINUS_COL,
                       stroke_width=2).move_to([3.0, -0.85, 0])
        self.play(Create(zl), run_time=0.7)
        self.play(GrowFromEdge(pu, DOWN), GrowFromEdge(pd, UP),
                  run_time=1.1)
        self.add(label("rocket up", (4.5, 0.85, 0), color=PLUS_COL,
                       size=22),
                 label("exhaust down", (4.7, -0.85, 0), color=MINUS_COL,
                       size=22))
        self.wait(DUR - 6.6)
