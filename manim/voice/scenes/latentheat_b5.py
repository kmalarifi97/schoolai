from manim import *
import numpy as np
from latentheat_helpers import make_lattice, small_label

# "— it's breaking the bonds that hold them in place. Energy spent on
#  freedom, not on speed."
DUR = 7.5


class LatentheatS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        lat = make_lattice([0, 0.2, 0], rows=4, cols=4, gap=0.72,
                            part_r=0.17)
        bonds, parts = lat[0], lat[1]
        self.add(bonds, parts)
        self.wait(0.5)

        # snap bonds one by one
        self.play(LaggedStart(*[FadeOut(b, scale=1.3) for b in bonds],
                              lag_ratio=0.05, run_time=2.2))
        # particles loosen into liquid disorder
        rng = np.random.default_rng(42)
        anims = []
        for p in parts:
            off = rng.uniform(-0.45, 0.45, size=2)
            anims.append(p.animate.shift(np.array([off[0], off[1], 0])))
        self.play(*anims, run_time=1.6,
                  rate_func=rate_functions.ease_out_sine)
        lbl = small_label("freedom, not speed", [0, -2.4, 0],
                          color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=0.8)
        self.wait(DUR - 5.6)
