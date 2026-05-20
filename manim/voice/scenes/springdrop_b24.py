from manim import *
import numpy as np
from springdrop_helpers import (callback_bow, callback_book,
                                callback_cart, callback_pendulum,
                                make_spring, make_ball, make_bell,
                                energy_chain)

# "This machine was all of them at once. That is the concept. Now you
#  know which videos to go back to."
# visual ends with: [Hold 3s in silence] -- honored as a held final
# still frame, ~3s of silence after the four callbacks converge into
# the single launcher + energy-bar image. No literal text on screen.
BASE_DUR = 8.6
HOLD = 3.0
DUR = BASE_DUR + HOLD


class SpringdropS1B24(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # the four callbacks present, spread out, faint
        bow = callback_bow([-4.6, 1.8, 0], scale=1.0, opacity=0.8)
        book = callback_book([-1.6, 2.0, 0], scale=1.0, opacity=0.8)
        cart = callback_cart([1.4, 2.0, 0], scale=1.0, opacity=0.8)
        pend = callback_pendulum([4.4, 1.9, 0], scale=1.0,
                                 opacity=0.8)
        self.play(FadeIn(bow), FadeIn(book), FadeIn(cart),
                  FadeIn(pend), run_time=1.4)
        self.wait(0.8)

        # they converge toward the center and dissolve
        center = np.array([0, 0.4, 0])
        self.play(
            bow.animate.move_to(center).scale(0.3).set_opacity(0.0),
            book.animate.move_to(center).scale(0.3).set_opacity(0.0),
            cart.animate.move_to(center).scale(0.3).set_opacity(0.0),
            pend.animate.move_to(center).scale(0.3).set_opacity(0.0),
            run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        # ... into the single launcher + energy-bar image
        sp = make_spring([-3.4, -2.2, 0], height=1.5, compress=0.45)
        ball = make_ball(sp["top"] + UP * 0.2, r=0.22)
        bell = make_bell([-3.4, 1.6, 0], scale=0.7)
        chain = energy_chain([2.0, -0.3, 0], stage=0.5, scale=0.85)
        self.play(FadeIn(sp["group"], scale=1.05),
                  FadeIn(ball, scale=1.05),
                  FadeIn(bell, scale=1.05),
                  FadeIn(chain, scale=1.05), run_time=1.8)

        # the concept, complete. Stillness. [Hold 3s in silence]
        self.wait(BASE_DUR - 6.0)
        self.wait(HOLD)            # the deliberate 3s silent hold
