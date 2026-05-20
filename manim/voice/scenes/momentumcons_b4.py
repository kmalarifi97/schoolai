from manim import *
import numpy as np
from momentumcons_helpers import (make_figure, make_bag, momentum_bar,
                                  zero_line, sign_tag, label,
                                  PLUS_COL, MINUS_COL)

# "Add it up the right way — motion as momentum, with direction.
#  Forward counts as plus. Backward as minus."
DUR = 8.6


class MomentumconsS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the two bodies up top
        fig = make_figure((-3.4, 2.0, 0), scale=0.55)
        bag = make_bag((3.4, 2.0, 0), scale=0.55)
        self.add(fig, bag)

        origin = (0, -0.4, 0)
        zl = zero_line(origin, height=3.0)
        self.play(Create(zl), run_time=1.0)

        # forward = plus (bag, blue, right)
        plus_t = sign_tag("+", (2.0, 1.4, 0), PLUS_COL, size=40)
        bar_p = momentum_bar(1.7, +1, origin=origin, unit=1.4,
                             color=PLUS_COL)
        self.play(FadeIn(plus_t), GrowFromEdge(bar_p, LEFT), run_time=1.2)
        self.play(label("forward", (2.4, -1.4, 0), color=PLUS_COL,
                        size=24).animate.set_opacity(0.95), run_time=0.6)

        # backward = minus (person, orange, left)
        minus_t = sign_tag("−", (-2.0, 1.4, 0), MINUS_COL, size=40)
        bar_m = momentum_bar(1.7, -1, origin=origin, unit=1.4,
                             color=MINUS_COL)
        self.play(FadeIn(minus_t), GrowFromEdge(bar_m, RIGHT),
                  run_time=1.2)
        self.add(label("backward", (-2.4, -1.4, 0), color=MINUS_COL,
                       size=24))
        self.wait(DUR - 5.0)
