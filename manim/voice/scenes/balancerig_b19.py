from manim import *
import numpy as np
from balancerig_helpers import make_mobile, make_lina, small_label

# "Now she hangs the real mobile. Once. And it floats level over the
#  bed."
DUR = 6.5


class BalancerigS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.7, 0], half_w=3.0,
                        shapes=[(-2.4, 0.9, "#C98A6B"),
                                (-0.9, 0.6, "#9BD6B0"),
                                (1.7, 0.7, "#E8C46B"),
                                (2.5, 0.7, "#9BD6B0")],
                        ceil_y=3.4)
        lina = make_lina([-4.8, -1.6, 0], scale=0.85)
        self.add(lina)
        # one deliberate arrangement; it settles perfectly level
        self.play(FadeIn(m["ceiling"]), Create(m["string"]),
                  run_time=1.0)
        self.play(FadeIn(m["rig"], shift=UP * 0.15), run_time=1.4)
        # a faint bed line below
        bed = Line([-2.6, -2.4, 0], [2.6, -2.4, 0], color="#8C8576",
                   stroke_width=3).set_opacity(0.4)
        self.play(Create(bed), run_time=0.8)
        self.play(FadeIn(small_label("level", [3.6, 0.7, 0],
                                     color="#9BD6B0", size=22)),
                  run_time=0.8)
        self.wait(DUR - 4.0)
