from manim import *
import numpy as np
from springdrop_helpers import (callback_book, callback_cart,
                                small_label)

# "And the book on the high shelf, holding energy it hadn't spent? And
#  the cart that turned a push into pure speed?"
DUR = 9.6


class SpringdropS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the book on a high shelf
        book = callback_book([0, 0.6, 0], scale=1.7, opacity=0.0)
        self.play(book.animate.set_opacity(0.9), run_time=1.4)
        bcap = small_label("gravitational PE — unspent",
                           [0, -1.4, 0], size=22, color="#8C8576")
        self.play(FadeIn(bcap), run_time=0.8)
        self.wait(1.4)
        self.play(book.animate.set_opacity(0.0),
                  bcap.animate.set_opacity(0.0), run_time=1.0)

        # the rolling cart — a push into pure speed
        cart = callback_cart([-0.8, 0.2, 0], scale=1.9, opacity=0.0)
        self.play(cart.animate.set_opacity(0.9), run_time=1.0)
        self.play(cart.animate.shift(RIGHT * 1.6), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        ccap = small_label("kinetic energy — push into speed",
                           [0, -1.6, 0], size=22, color="#8C8576")
        self.play(FadeIn(ccap), run_time=0.6)
        self.wait(DUR - 8.8)
