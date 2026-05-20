from manim import *
import numpy as np
from momentumcons_helpers import (make_figure, make_bag, momentum_bar,
                                  label, PLUS_COL, MINUS_COL)

# "And it's just Newton's third law, looked at over time. Every push has
#  an equal, opposite push back."
DUR = 8.3


class MomentumconsS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        hand = make_figure((-2.4, 0.6, 0), scale=0.55)
        bag = make_bag((2.0, 0.6, 0), scale=0.6)
        self.add(hand, bag)
        self.wait(0.6)

        # equal-opposite force pair at the contact
        f_on_bag = Arrow([-0.2, 0.6, 0], [1.2, 0.6, 0], color=PLUS_COL,
                         stroke_width=6, buff=0,
                         max_tip_length_to_length_ratio=0.3)
        f_on_hand = Arrow([-0.2, 0.6, 0], [-1.6, 0.6, 0],
                          color=MINUS_COL, stroke_width=6, buff=0,
                          max_tip_length_to_length_ratio=0.3)
        self.play(GrowArrow(f_on_bag), GrowArrow(f_on_hand),
                  run_time=1.2)
        self.add(label("equal, opposite", (0, 1.6, 0), color="#8C98A6",
                       size=24))
        self.wait(0.6)

        # resolve into equal-opposite momentum changes (over time)
        origin = (0, -1.6, 0)
        dp_b = momentum_bar(1.3, +1, origin=origin, unit=1.2,
                            color=PLUS_COL, height=0.40)
        dp_h = momentum_bar(1.3, -1, origin=origin, unit=1.2,
                            color=MINUS_COL, height=0.40)
        arrow_down = Arrow([0, -0.2, 0], [0, -1.0, 0], color="#8C98A6",
                           stroke_width=3, buff=0).set_opacity(0.6)
        self.play(GrowArrow(arrow_down), run_time=0.7)
        self.play(GrowFromEdge(dp_b, LEFT), GrowFromEdge(dp_h, RIGHT),
                  run_time=1.3)
        self.add(label("Δp", (0, -2.5, 0), color="#8C98A6", size=24))
        self.wait(DUR - 5.7)
