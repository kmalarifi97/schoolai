from manim import *
import numpy as np
from skatepark_helpers import (callback_book, callback_cart,
                               callback_pendulum, make_ramp,
                               bar_chart_panel)

# "This ramp was all of them, at once. That is the concept. Now you
#  know which videos to go back to."
# visual ends with: [Hold 3s in silence] -- honored as a held final
# still frame, ~3s added to this scene's run time. No literal text.
BASE_DUR = 8.5
HOLD = 3.0
DUR = BASE_DUR + HOLD


class SkateparkS1B25(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # the three callbacks present, spread out, faint
        book = callback_book([-4.0, 1.6, 0], scale=1.1, opacity=0.8)
        cart = callback_cart([0.0, 2.0, 0], scale=1.1, opacity=0.8)
        pend = callback_pendulum([4.0, 1.8, 0], scale=1.1, opacity=0.8)
        self.play(FadeIn(book), FadeIn(cart), FadeIn(pend),
                  run_time=1.2)
        self.wait(0.8)

        # they converge toward the center and dissolve
        center = np.array([0, 0.2, 0])
        self.play(
            book.animate.move_to(center).scale(0.3).set_opacity(0.0),
            cart.animate.move_to(center).scale(0.3).set_opacity(0.0),
            pend.animate.move_to(center).scale(0.3).set_opacity(0.0),
            run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        # ... into the single ramp + energy-bar image
        r = make_ramp(launch_h=2.2)
        ramp = r["group"].scale(0.7).move_to([-2.4, -0.4, 0])
        panel = bar_chart_panel([3.0, -0.2, 0], pe=0.5, ke=0.4,
                                th=0.1, scale=0.8)
        self.play(FadeIn(ramp, scale=1.05),
                  FadeIn(panel, scale=1.05), run_time=1.8)

        # the hint, complete. Stillness. [Hold 3s in silence]
        self.wait(BASE_DUR - 5.8)
        self.wait(HOLD)            # the deliberate 3s silent hold
