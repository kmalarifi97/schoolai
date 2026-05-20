from manim import *
import numpy as np
from workenergy_helpers import (make_figure, make_wall, small_label,
                                zero_tag)

# "It's why the wall taught you nothing. No motion, no work, no change.
#  Effort isn't in the equation."
DUR = 8.5


class WorkenergyS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall([2.2, -0.3, 0], height=4.0)
        fig = make_figure([0.2, -0.9, 0], scale=1.0, straining=True,
                          facing=1)
        self.play(FadeIn(wall), FadeIn(fig), run_time=1.0)
        self.wait(0.6)

        rows = [
            ("motion", -3.6, 1.6),
            ("work", -3.6, 0.6),
            ("change", -3.6, -0.4),
        ]
        for name, x, y in rows:
            t = small_label(name, [x, y, 0], color="#8C98A6", size=28)
            z = zero_tag([x + 2.0, y, 0], size=40)
            self.play(FadeIn(t, run_time=0.4), GrowFromCenter(z,
                      run_time=0.4))
        self.wait(0.4)
        sub = small_label("effort isn't in the equation", [0, -2.9, 0],
                          color="#8C98A6", size=26).set_opacity(0.85)
        self.play(FadeIn(sub, run_time=0.9))
        self.wait(DUR - 6.2)
