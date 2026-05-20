from manim import *
import numpy as np
from skatepark_helpers import make_ramp, arc_path, small_label

# "Same height, two answers — because friction was a term he never
#  wrote down."
DUR = 6.9


class SkateparkS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.4)
        self.add(r["group"])
        short_end = np.array([r["gap_x1"] - 0.3,
                              r["ground_y"] - 0.05, 0])
        over_end = np.array([6.2, r["ground_y"] - 0.05, 0])
        a1 = arc_path(r["lip"], short_end, peak=1.2, color="#C98A6B",
                      width=4)
        a2 = arc_path(r["lip"], over_end, peak=1.7, color="#9BD6B0",
                      width=4)
        self.play(Create(a1), Create(a2), run_time=1.6)

        # each tagged with its heat-loss size
        t1 = small_label("big heat loss",
                         np.array([-0.4, 0.4, 0]),
                         color="#D98C5F", size=20)
        t2 = small_label("small heat loss",
                         np.array([3.4, 2.0, 0]),
                         color="#D98C5F", size=20)
        self.play(FadeIn(t1), FadeIn(t2), run_time=1.0)
        miss = small_label("friction", [0, -2.6, 0],
                           color="#EAE4D5", size=30)
        self.play(Write(miss), run_time=1.0)
        self.wait(DUR - 3.6)
