from manim import *
import numpy as np
from specificheat_helpers import sponge, energy_bar, Thermometer, label

# "Some substances soak up a lot of energy for only a small rise in
#  temperature."
DUR = 7.0


class SpecificheatS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = sponge([-1.0, 0.0, 0], w=2.6, h=2.2)
        lw = label("water", [-1.0, -1.7, 0], size=24)
        eb = energy_bar([-1.0, 2.4, 0], length=3.4, frac=1.0)
        le = label("a lot of energy", [-1.0, 3.0, 0], size=22)
        th = Thermometer([4.2, -0.1, 0], height=2.6, level=0.10)
        ld = label("barely moves", [4.2, -2.0, 0], size=22)
        self.add(sp, lw, th, ld)
        self.play(FadeIn(eb), Write(le), run_time=1.0)
        # energy pours into the sponge
        drops = VGroup(*[Dot([-1.0 + np.random.uniform(-1, 1), 1.9, 0],
                             radius=0.06, color="#F0902A") for _ in range(8)])
        self.play(LaggedStart(*[d.animate.move_to(
            [d.get_x(), 0.0, 0]) for d in drops],
            lag_ratio=0.12, run_time=1.6))
        self.play(
            UpdateFromAlphaFunc(th, lambda m, a: m.set_level(0.10 + 0.12 * a)),
            FadeOut(drops), run_time=1.6)
        self.wait(DUR - 4.2)
