from manim import *
import numpy as np
from thermolaws_helpers import scatter_field, entropy_bar

# "Because the universe drifts, always, toward more spread-out, more
#  disordered, more mixed. We measure that drift with entropy."
DUR = 10.2


class ThermolawsS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sc = scatter_field([-2.0, 0, 0], disorder=0.0, n_side=5,
                           gap=0.46, seed=11)
        bar = entropy_bar([3.4, -1.7, 0], frac=0.08, height=3.4)
        self.play(FadeIn(sc), run_time=1.2)
        self.play(FadeIn(bar), run_time=0.8)
        self.wait(0.5)
        # drift toward disorder, in stages, bar rising with it
        for d, f in [(0.35, 0.34), (0.7, 0.62), (1.0, 0.9)]:
            sc2 = scatter_field([-2.0, 0, 0], disorder=d, n_side=5,
                                gap=0.46, seed=11)
            bar2 = entropy_bar([3.4, -1.7, 0], frac=f, height=3.4)
            self.play(Transform(sc, sc2), Transform(bar, bar2),
                      run_time=1.7)
        self.wait(DUR - 8.6)
