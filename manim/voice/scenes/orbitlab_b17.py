from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, spiral_in_path,
                              escape_path, closed_circle_path,
                              small_label)

# "After — he explains the gap. Spiraled in? Launch was slow. Flew
#  off? Too fast. The trace names his error."
DUR = 9.1


class OrbitlabS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cs = [np.array([-4.2, -0.2, 0]),
              np.array([0.0, -0.2, 0]),
              np.array([4.2, -0.2, 0])]
        for cc in cs:
            self.add(make_planet(cc, r=0.42))

        sp = spiral_in_path(cs[0], r0=1.3, turns=1.5, r_end=0.42,
                            color="#C98A6B", width=3)
        ci = closed_circle_path(cs[1], r=1.05, color="#9BD6B0",
                                width=3)
        es = escape_path(cs[2], r0=0.95, color="#C98A6B", width=3)
        self.play(Create(sp), Create(ci), Create(es), run_time=1.8)
        self.wait(0.4)

        t1 = small_label("too slow", cs[0] + np.array([0, 1.9, 0]),
                         color="#C98A6B", size=22)
        t2 = small_label("target", cs[1] + np.array([0, 1.9, 0]),
                         color="#9BD6B0", size=22)
        t3 = small_label("too fast", cs[2] + np.array([0, 1.9, 0]),
                         color="#C98A6B", size=22)
        self.play(FadeIn(t1), FadeIn(t3), run_time=1.0)
        self.play(FadeIn(t2), run_time=0.8)
        tag = small_label("the trace names the error", [0, -2.8, 0],
                          color="#8C8576", size=22)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(DUR - 5.6)
