from manim import *
import numpy as np
from collisionlab_helpers import (callback_cars_wall, callback_lake_throw,
                                  callback_steel_clay, make_cart,
                                  table_line, momentum_bar)

# "This crash was all three at once. That is the concept. Now you know
#  which videos to go back to."
# visual ends with: [Hold 3s in silence] -- honored as a held final
# still frame, ~3s added after the converged image. No literal text.
BASE_DUR = 8.3
HOLD = 3.0
DUR = BASE_DUR + HOLD


class CollisionlabS1B25(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # the three callbacks present, spread, faint
        cw = callback_cars_wall([-4.2, 1.5, 0], scale=1.3,
                                opacity=0.8)
        lt = callback_lake_throw([0.0, 1.7, 0], scale=1.3,
                                 opacity=0.8)
        sc = callback_steel_clay([4.2, 1.6, 0], scale=1.3,
                                 opacity=0.8)
        self.play(FadeIn(cw), FadeIn(lt), FadeIn(sc), run_time=1.4)
        self.wait(0.8)

        # they converge toward center and dissolve into one
        center = np.array([0, 0.6, 0])
        self.play(
            cw.animate.move_to(center).scale(0.3).set_opacity(0.0),
            lt.animate.move_to(center).scale(0.3).set_opacity(0.0),
            sc.animate.move_to(center).scale(0.3).set_opacity(0.0),
            run_time=2.0, rate_func=rate_functions.ease_in_out_sine)

        # ... into the single two-cart + conserved-bar image
        tbl = table_line(-1.4)
        c1 = make_cart([-1.0, -0.9, 0], scale=0.95, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([1.0, -0.9, 0], scale=0.95, color="#E8C46B",
                       dented=True, facing=-1)
        bar = momentum_bar([0, 1.0, 0], length=4.4, split=0.5,
                           label=None)
        self.play(FadeIn(tbl), FadeIn(c1, scale=1.05),
                  FadeIn(c2, scale=1.05),
                  FadeIn(bar, scale=1.05), run_time=1.8)

        # the concept, complete. Stillness. [Hold 3s in silence]
        self.wait(BASE_DUR - 6.0)
        self.wait(HOLD)            # the deliberate 3s silent hold
