from manim import *
import numpy as np
from balancerig_helpers import make_mobile, twist_arrow, small_label

# "Every shape twists the bar by its weight times its distance from the
#  string. That twist is what has to balance."
DUR = 9.5


class BalancerigS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.6, 0], half_w=3.0,
                        shapes=[(-2.4, 1.0, "#C98A6B"),
                                (-1.0, 0.6, "#9BD6B0"),
                                (1.6, 0.8, "#E8C46B"),
                                (2.6, 0.7, "#9BD6B0")],
                        ceil_y=3.4)
        self.add(m["group"])
        pv = m["string"].get_end()
        self.wait(0.5)

        # a turning arrow for each shape, sized by weight x distance
        specs = [(-2.4, 1.0, "left"), (-1.0, 0.6, "left"),
                 (1.6, 0.8, "right"), (2.6, 0.7, "right")]
        arrows = VGroup()
        for (x, w, side) in specs:
            ctr = np.array([x * 0.55, 0.55, 0]) + np.array(
                [pv[0], pv[1], 0]) * 0
            ctr = np.array([x, m["bar"].get_center()[1] + 0.55, 0])
            a = twist_arrow(ctr, w, abs(x), side=side)
            arrows.add(a)
        for a in arrows:
            self.play(FadeIn(a), run_time=0.7)
        self.play(FadeIn(small_label("weight × distance = twist",
                                     [0, -1.9, 0], color="#EAE4D5",
                                     size=24)), run_time=0.9)
        self.wait(DUR - 4.6)
