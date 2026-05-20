from manim import *
import numpy as np
from momentumcons_helpers import (make_balance, momentum_bar, label,
                                  PLUS_COL, MINUS_COL)

# "Total momentum before: zero. Total after: still zero. Nothing was
#  created. It only got shared."
# Visual carries the marker [Hold 2s in silence] — honored as a 2.0s
# extra still hold on the final frame (no literal text rendered).
HOLD = 2.0
DUR = 7.6 + HOLD


class MomentumconsS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bal = make_balance((0, 0.2, 0), span=5.0)
        self.add(bal)

        # BEFORE: both pans empty -> total zero
        before_t = label("before", (-3.6, 2.4, 0), color="#8C98A6",
                          size=24)
        z0 = label("total = 0", (0, -1.7, 0), color="#EAE4D5", size=30)
        self.play(FadeIn(before_t), run_time=0.8)
        self.play(FadeIn(z0), run_time=0.8)
        self.wait(1.0)

        # AFTER: + bag on right pan, − you on left pan; still sums to 0
        after_t = label("after", (3.6, 2.4, 0), color="#8C98A6", size=24)
        bp = momentum_bar(0.9, +1, origin=(2.0, -0.45, 0), unit=1.0,
                          color=PLUS_COL, height=0.36)
        bm = momentum_bar(0.9, -1, origin=(-2.0, -0.45, 0), unit=1.0,
                          color=MINUS_COL, height=0.36)
        self.play(FadeIn(after_t), run_time=0.7)
        self.play(GrowFromEdge(bm, RIGHT), GrowFromEdge(bp, LEFT),
                  run_time=1.3)
        # balance stays level — total unchanged, still zero
        self.play(Indicate(z0, scale_factor=1.12, color="#EAE4D5"),
                  run_time=1.0)

        # [Hold 2s in silence] — final frame held still, no extra motion
        self.wait(DUR - 6.6)
