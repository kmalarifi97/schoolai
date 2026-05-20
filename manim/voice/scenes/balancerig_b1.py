from manim import *
import numpy as np
from balancerig_helpers import make_mobile, make_lina

# "Lina is hanging a mobile over her little brother's bed. A bar, a
#  string at the middle, shapes dangling off each side."
DUR = 9.9


class BalancerigS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.3, 0], half_w=3.0,
                        shapes=[(-2.2, 1.0, "#C98A6B"),
                                (-0.9, 0.6, "#9BD6B0"),
                                (1.3, 0.8, "#E8C46B"),
                                (2.5, 0.7, "#9BD6B0")],
                        ceil_y=3.4)
        self.play(FadeIn(m["ceiling"], shift=DOWN * 0.1), run_time=1.2)
        self.play(Create(m["string"]), run_time=1.0)
        self.play(GrowFromCenter(m["bar"]), run_time=1.2)
        self.play(FadeIn(m["shapes"], shift=UP * 0.2), run_time=1.6)
        lina = make_lina([-4.6, -1.4, 0], scale=0.9)
        self.play(FadeIn(lina, shift=RIGHT * 0.15), run_time=1.0)
        self.wait(DUR - 6.0)
