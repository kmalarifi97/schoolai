from manim import *
import numpy as np
from skatepark_helpers import (callback_book, callback_cart,
                               callback_pendulum)

# "And if all of this felt familiar — it should. Do you remember the
#  book that sat still on the shelf, holding energy it hadn't spent?
#  The cart that turned a push into speed? The pendulum that never lost
#  a thing — until something quietly took it?"
DUR = 19.0


class SkateparkS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.0)

        # 1) the book on a shelf — flickers in, holds, fades
        book = callback_book([0, 0.2, 0], scale=1.6, opacity=0.0)
        self.play(book.animate.set_opacity(0.9), run_time=1.4)
        self.wait(2.4)
        self.play(book.animate.set_opacity(0.0), run_time=1.2)

        # 2) the rolling cart — push into speed
        cart = callback_cart([-0.6, 0.0, 0], scale=1.8, opacity=0.0)
        self.play(cart.animate.set_opacity(0.9), run_time=1.4)
        self.play(cart.animate.shift(RIGHT * 1.4), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.8)
        self.play(cart.animate.set_opacity(0.0), run_time=1.2)

        # 3) the swinging pendulum — never lost a thing, until...
        pend = callback_pendulum([0, 1.2, 0], scale=1.7, opacity=0.0,
                                 theta=0.6)
        self.play(pend.animate.set_opacity(0.9), run_time=1.2)
        # a small swing
        self.play(Rotate(pend, angle=-1.0, about_point=[0, 1.95, 0]),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.play(Rotate(pend, angle=1.0, about_point=[0, 1.95, 0]),
                  run_time=1.2, rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 17.6)
