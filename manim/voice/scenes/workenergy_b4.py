from manim import *
import numpy as np
from workenergy_helpers import make_figure, make_cart, force_arrow

# "Now push a cart and let it roll. Same force — but this time it moves."
DUR = 6.4


class WorkenergyS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fig = make_figure([-4.6, -0.9, 0], scale=1.0, straining=True,
                          facing=1)
        cart = make_cart([-2.7, -1.05, 0], scale=0.95)
        self.play(FadeIn(fig), FadeIn(cart), run_time=1.0)
        self.wait(0.5)
        fa = force_arrow([-3.7, -0.7, 0], length=1.0, direction=RIGHT,
                         label="F")
        self.play(GrowArrow(fa[0]), FadeIn(fa[1]), run_time=0.8)
        self.wait(0.4)
        # this time it moves
        self.play(fig.animate.shift(RIGHT * 2.4),
                  cart.animate.shift(RIGHT * 2.4),
                  fa.animate.shift(RIGHT * 2.4),
                  run_time=2.0, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 4.7)
