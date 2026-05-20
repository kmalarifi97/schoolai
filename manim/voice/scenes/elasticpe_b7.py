from manim import *
import numpy as np
from elasticpe_helpers import make_bar, set_bar, small_label

# "So the stored energy doesn't grow steadily — it grows faster the
#  more you deform it."
DUR = 7.5


class ElasticpeS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # axis cue
        x_lbl = small_label("deformation", [0.0, -2.7, 0], size=24)
        y_lbl = small_label("stored energy", [-4.6, 1.4, 0],
                            size=24).rotate(PI / 2)
        self.add(x_lbl, y_lbl)

        # four bars climbing in accelerating jumps (~ x^2)
        fracs = [0.06, 0.22, 0.50, 0.92]
        xs = [-2.4, -0.8, 0.8, 2.4]
        bars = []
        for xx, fr in zip(xs, fracs):
            b = make_bar([xx, -0.4, 0], max_h=3.4, w=0.78, frac=0.001,
                         color="#7FB8E8")
            self.add(b["frame"], b["fill"])
            bars.append((b, fr))

        for b, fr in bars:
            tgt = set_bar(b, fr)
            self.play(Transform(b["fill"], tgt),
                      run_time=0.85, rate_func=rate_functions.ease_out_quad)
            self.wait(0.2)
        self.wait(DUR - 4.6)
