from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, spiral_in_path,
                              ellipse_path, closed_circle_path,
                              run_counter)

# "His first prediction is wrong. That is not the problem. That is the
#  point. Each miss narrows the speed."
DUR = 8.9


class OrbitlabS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, -0.2, 0])
        self.add(make_planet(c, r=0.7))
        rc = run_counter([0, 2.7, 0], used=0, total=3)
        self.add(rc)

        # run 1: spiral in
        r1 = spiral_in_path(c, r0=2.4, turns=1.5, r_end=0.7,
                            color="#C98A6B", width=4)
        self.play(Create(r1), Transform(
            rc, run_counter([0, 2.7, 0], used=1, total=3)),
            run_time=1.8)
        self.wait(0.3)
        self.play(r1.animate.set_opacity(0.25), run_time=0.5)

        # run 2: an ellipse, closer
        r2 = ellipse_path(c, a=2.4, b=1.5, color="#E8C46B", width=4)
        self.play(Create(r2), Transform(
            rc, run_counter([0, 2.7, 0], used=2, total=3)),
            run_time=1.8)
        self.wait(0.3)
        self.play(r2.animate.set_opacity(0.25), run_time=0.5)

        # run 3: near-perfect closed circle
        r3 = closed_circle_path(c, r=1.9, color="#9BD6B0", width=4)
        self.play(Create(r3), Transform(
            rc, run_counter([0, 2.7, 0], used=3, total=3)),
            run_time=1.8)
        self.wait(DUR - 8.1)
