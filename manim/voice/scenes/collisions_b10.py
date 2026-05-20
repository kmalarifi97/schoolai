from manim import *
import numpy as np
from collisions_helpers import checklist, title

# "So a collision has two questions. Momentum: always conserved.
#  Motion energy: only sometimes."
DUR = 7.55


class CollisionsS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ttl = title("two questions", [0, 2.6, 0], size=32)
        self.play(FadeIn(ttl), run_time=0.7)

        cl = checklist([0.2, 0.0, 0], [
            ("momentum", True, "always conserved"),
            ("motion energy", False, "elastic only"),
        ])
        self.play(FadeIn(cl[0], shift=RIGHT * 0.3), run_time=0.9)
        self.wait(0.6)
        self.play(FadeIn(cl[1], shift=RIGHT * 0.3), run_time=0.9)
        self.wait(DUR - 4.1)
