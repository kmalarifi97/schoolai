from manim import *
import numpy as np
from workenergy_helpers import make_cart, force_arrow, small_label

# "Where it goes: into motion. The cart that was still is now fast."
DUR = 6.0


class WorkenergyS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cart = make_cart([-4.4, -0.6, 0], scale=0.95)
        still = small_label("still", [-4.4, -1.8, 0],
                            color="#8C98A6", size=26)
        self.play(FadeIn(cart), FadeIn(still), run_time=0.9)
        self.wait(0.5)

        fa = force_arrow([-5.4, -0.3, 0], length=0.9, direction=RIGHT,
                         label="F")
        self.play(GrowArrow(fa[0]), FadeIn(fa[1]), run_time=0.6)

        # speed bar grows under the cart as it accelerates across
        sbar = Rectangle(width=0.01, height=0.30, fill_color="#9CC97F",
                         fill_opacity=0.9, stroke_width=0)
        sbar.move_to([-4.4, -1.6, 0]).align_to(cart, LEFT)
        self.add(sbar)

        def grow_bar(m, a):
            w = 0.01 + 3.0 * a
            nb = Rectangle(width=w, height=0.30, fill_color="#9CC97F",
                           fill_opacity=0.9, stroke_width=0)
            nb.move_to([-4.4 + w / 2 + 2.6 * a, -1.7, 0])
            m.become(nb)

        self.play(cart.animate.shift(RIGHT * 6.0),
                  fa.animate.shift(RIGHT * 6.0),
                  UpdateFromAlphaFunc(sbar, grow_bar),
                  FadeOut(still, run_time=0.6),
                  run_time=2.4, rate_func=rate_functions.ease_in_quad)
        fast = small_label("fast", [3.4, -1.7, 0], color="#9CC97F",
                           size=28)
        self.play(FadeIn(fast), run_time=0.5)
        self.wait(DUR - 5.4)
