from manim import *
import numpy as np
from springdrop_helpers import (make_bell, target_line, rise_path,
                                run_counter, small_label)

# "His first prediction is wrong. That is not the problem. That is the
#  point. Each miss tells him which form he mismeasured."
DUR = 10.2


class SpringdropS1B18(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bell = make_bell([0, 2.0, 0], scale=0.9)
        bell_y = 1.75
        tl = target_line(bell_y, x0=-5.0, x1=5.0)
        self.add(bell, tl)
        rc = run_counter([-1.0, -3.0, 0], used=0, total=3)
        self.add(rc)

        start = [0, -2.4, 0]
        # run 1: short
        a1 = rise_path(start, -0.2, color="#C98A6B", width=3,
                       fall=False)
        self.play(Create(a1), run_time=1.3)
        l1 = small_label("run 1 — short", [3.4, -0.4, 0], size=22,
                         color="#8C8576")
        self.play(FadeIn(l1), a1.animate.set_opacity(0.45),
                  run_time=0.7)

        # run 2: over
        a2 = rise_path(start, 3.0, color="#C98A6B", width=3,
                       fall=False)
        self.play(Create(a2), run_time=1.3)
        l2 = small_label("run 2 — over", [3.4, 1.4, 0], size=22,
                         color="#8C8576")
        self.play(FadeIn(l2), a2.animate.set_opacity(0.45),
                  run_time=0.7)

        # run 3: right at the bell line
        a3 = rise_path(start, bell_y, color="#9BD6B0", width=3.5,
                       fall=False)
        self.play(Create(a3), run_time=1.4)
        l3 = small_label("run 3 — at the bell", [3.4, bell_y, 0],
                         size=22, color="#9BD6B0")
        self.play(FadeIn(l3), run_time=0.7)
        self.wait(DUR - 8.1)
