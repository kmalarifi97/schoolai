from manim import *
import numpy as np
from momentumcons_helpers import (make_cart, momentum_bar, label,
                                  PLUS_COL, MINUS_COL, CART_A_COL,
                                  CART_B_COL)

# "And how collisions work. Two carts meet. Whatever one gains, the
#  other gives up. The total never changes."
DUR = 9.1


class MomentumconsS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        track = Line([-6, 0.4, 0], [6, 0.4, 0], color="#3A4A5A",
                     stroke_width=2).set_opacity(0.5)
        self.add(track)

        c1 = make_cart((-4.5, 0.8, 0), scale=1.0, color=CART_A_COL)
        c2 = make_cart((4.5, 0.8, 0), scale=1.0, color=CART_B_COL)
        self.add(c1, c2)
        self.wait(0.5)

        # they meet
        self.play(c1.animate.move_to([-0.7, 0.8, 0]),
                  c2.animate.move_to([0.7, 0.8, 0]),
                  run_time=1.6, rate_func=rate_functions.ease_in_quad)
        # exchange: c1 slows, c2 speeds — they swap
        self.play(c1.animate.move_to([-1.2, 0.8, 0]),
                  c2.animate.move_to([4.6, 0.8, 0]),
                  run_time=1.6, rate_func=rate_functions.ease_out_quad)

        # individual bars change, the summed total bar stays fixed length
        lbl = label("total", (0, -2.7, 0), color="#8C98A6", size=24)
        total = Rectangle(width=3.4, height=0.42, fill_color="#EAD58C",
                          fill_opacity=0.9, stroke_color="#EAD58C",
                          stroke_width=2).move_to([0, -2.0, 0])
        b1 = Rectangle(width=2.2, height=0.36, fill_color=CART_A_COL,
                       fill_opacity=0.9, stroke_width=2,
                       stroke_color=CART_A_COL).move_to([-1.7, -1.1, 0])
        b2 = Rectangle(width=1.2, height=0.36, fill_color=CART_B_COL,
                       fill_opacity=0.9, stroke_width=2,
                       stroke_color=CART_B_COL).move_to([0.8, -1.1, 0])
        self.play(FadeIn(total), FadeIn(lbl), run_time=0.9)
        self.play(GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT),
                  run_time=0.9)
        # swap their lengths — total unchanged
        nb1 = Rectangle(width=1.2, height=0.36, fill_color=CART_A_COL,
                        fill_opacity=0.9, stroke_width=2,
                        stroke_color=CART_A_COL)
        nb1.move_to([-2.2, -1.1, 0]).align_to(b1, LEFT)
        nb2 = Rectangle(width=2.2, height=0.36, fill_color=CART_B_COL,
                        fill_opacity=0.9, stroke_width=2,
                        stroke_color=CART_B_COL)
        nb2.next_to(nb1, RIGHT, buff=0)
        self.play(Transform(b1, nb1), Transform(b2, nb2), run_time=1.2)
        self.wait(DUR - 8.2)
