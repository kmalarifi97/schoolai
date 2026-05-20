from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, ellipse_path,
                              spiral_in_path, escape_path)

# "Faster, slower, faster. Sometimes an egg shape, sometimes a crash.
#  He's clicking, not choosing."
DUR = 8.3


class OrbitlabS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)

        attempts = [
            ellipse_path(c, a=2.6, b=1.2, color="#C98A6B", phase=0.2),
            spiral_in_path(c, r0=2.2, turns=1.0, r_end=0.85,
                           color="#C98A6B"),
            ellipse_path(c, a=1.6, b=2.4, color="#C98A6B", phase=1.1),
            escape_path(c, r0=1.6, color="#C98A6B"),
            ellipse_path(c, a=2.9, b=1.7, color="#C98A6B", phase=-0.6),
            spiral_in_path(c, r0=2.6, turns=1.4, r_end=0.85,
                           color="#C98A6B"),
        ]
        prev = None
        for a in attempts:
            a.set_opacity(0.7)
            if prev is None:
                self.play(Create(a), run_time=0.9)
            else:
                self.play(FadeOut(prev, run_time=0.25),
                          Create(a, run_time=0.9))
            prev = a
        self.wait(DUR - (0.9 + 5 * (0.9)))
