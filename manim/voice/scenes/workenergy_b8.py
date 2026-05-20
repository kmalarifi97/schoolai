from manim import *
import numpy as np
from workenergy_helpers import make_cart, force_arrow, EnergyBar

# "Do negative work — push backward, like a brake — and you take that
#  energy out. The cart slows."
DUR = 8.4


class WorkenergyS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cart = make_cart([-3.4, 0.8, 0], scale=0.9)
        self.add(cart)

        bar = EnergyBar([3.6, -0.2, 0], height=3.0,
                        label="energy of motion")
        bar.set_level(0.85)
        self.add(bar)
        self.wait(0.5)

        # backward force (brake) on the moving cart
        fa = force_arrow([-2.0, 1.1, 0], length=1.4, direction=LEFT,
                         label="brake", color="#E05A5A")
        self.play(GrowArrow(fa[0]), FadeIn(fa[1]), run_time=0.9)
        self.wait(0.4)

        bar.set_color_to("#E05A5A")
        self.play(cart.animate.shift(RIGHT * 1.4),
                  run_time=1.6, rate_func=rate_functions.ease_out_quad)

        def drain(m, a):
            m.set_level(0.85 - 0.65 * a)
        self.play(UpdateFromAlphaFunc(bar, drain), run_time=1.8)
        self.wait(DUR - 6.2)
