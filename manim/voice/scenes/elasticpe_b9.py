from manim import *
import numpy as np
from elasticpe_helpers import (trampoline, bent_beam, clock_spring,
                               small_label)

# "It's everywhere. A trampoline. A pole vault. The spring in a clock.
#  A diving board."
DUR = 7.5


class ElasticpeS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        tr = trampoline([-4.6, 0.4, 0], dip=0.45, w=1.9)
        tl = small_label("trampoline", [-4.6, -1.0, 0], size=22)

        pole = bent_beam([-1.7, 1.6, 0], [-1.7, -1.0, 0], bend=-0.6)
        pl = small_label("pole vault", [-1.6, -1.5, 0], size=22)

        ck = clock_spring([1.4, 0.5, 0], turns=3.4)
        cl = small_label("clock spring", [1.4, -1.2, 0], size=22)

        bd = bent_beam([3.6, 1.4, 0], [5.4, 1.4, 0], bend=-0.55)
        dl = small_label("diving board", [4.5, 0.3, 0], size=22)

        for grp in ([tr, tl], [pole, pl], [ck, cl], [bd, dl]):
            self.play(*[FadeIn(m) for m in grp], run_time=0.8)
            self.wait(0.25)
        self.wait(DUR - 4.7)
