from manim import *
import numpy as np
from machines_helpers import ma_ratio, small_label, title_label

# "The factor by which it multiplies your force has a name. The
#  mechanical advantage."
DUR = 6.9


class MachinesS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        frac = ma_ratio([0, 0.3, 0], scale=1.25)
        self.play(FadeIn(frac[0], shift=DOWN * 0.2), run_time=0.9)
        self.play(Create(frac[1]), run_time=0.6)
        self.play(FadeIn(frac[2], shift=UP * 0.2), run_time=0.9)
        self.wait(0.5)

        box = SurroundingRectangle(frac, color="#EAE4D5", buff=0.35,
                                   stroke_width=2, corner_radius=0.12)
        self.play(Create(box), run_time=1.0)
        lbl = title_label("mechanical advantage", [0, -2.3, 0], size=36)
        self.play(Write(lbl), run_time=1.3)
        self.wait(DUR - 5.2)
