from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, spiral_in_path,
                              closed_circle_path, escape_path,
                              small_label)

# "Too slow, the pull wins — it falls in. Too fast, the straight line
#  wins — it escapes. The lap lives in between."
DUR = 9.5


class OrbitlabS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # three small panels: slow / matched / fast
        cs = [np.array([-4.2, -0.2, 0]),
              np.array([0.0, -0.2, 0]),
              np.array([4.2, -0.2, 0])]
        for cc in cs:
            self.add(make_planet(cc, r=0.42))

        sp = spiral_in_path(cs[0], r0=1.3, turns=1.6, r_end=0.42,
                            color="#C98A6B", width=3)
        ci = closed_circle_path(cs[1], r=1.05, color="#9BD6B0",
                                width=3)
        es = escape_path(cs[2], r0=0.95, color="#C98A6B", width=3)

        l1 = small_label("too slow", cs[0] + np.array([0, 1.9, 0]),
                         color="#C98A6B", size=22)
        l2 = small_label("matched", cs[1] + np.array([0, 1.9, 0]),
                         color="#9BD6B0", size=22)
        l3 = small_label("too fast", cs[2] + np.array([0, 1.9, 0]),
                         color="#C98A6B", size=22)

        self.play(Create(sp), FadeIn(l1), run_time=1.8)
        self.wait(0.3)
        self.play(Create(ci), FadeIn(l2), run_time=1.8)
        self.wait(0.3)
        self.play(Create(es), FadeIn(l3), run_time=1.8)
        self.wait(DUR - 6.0)
