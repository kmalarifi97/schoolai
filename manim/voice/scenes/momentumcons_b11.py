from manim import *
import numpy as np
from momentumcons_helpers import (isolated_boundary, make_cart,
                                  momentum_token, label, CART_A_COL,
                                  CART_B_COL)

# "Inside the boundary, momentum is currency. It moves around. It is
#  never spent."
DUR = 6.8


class MomentumconsS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bnd = isolated_boundary((0, 0, 0), w=8.0, h=4.4,
                                with_label=False)
        self.add(bnd)
        cA = make_cart((-2.6, 0, 0), scale=0.9, color=CART_A_COL)
        cB = make_cart((2.6, 0, 0), scale=0.9, color=CART_B_COL)
        self.add(cA, cB)

        toks = VGroup(*[
            momentum_token((-2.6 + dx, 0.9, 0), scale=0.8)
            for dx in (-0.6, 0.0, 0.6)
        ])
        self.play(FadeIn(toks, scale=0.7), run_time=1.0)
        self.add(label("momentum is currency", (0, 2.5, 0),
                       color="#8C98A6", size=24))
        self.wait(0.5)

        # tokens slide from cart A to cart B — count constant
        self.play(
            toks[0].animate.move_to([2.6 - 0.6, 0.9, 0]),
            toks[1].animate.move_to([2.6 + 0.0, 0.9, 0]),
            run_time=1.6, rate_func=rate_functions.ease_in_out_sine,
        )
        # and one slides back — it moves, never spent
        self.play(
            toks[2].animate.move_to([-2.6, 0.9, 0]),
            toks[0].animate.move_to([2.6, 0.9, 0]),
            run_time=1.5, rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(DUR - 6.1)
