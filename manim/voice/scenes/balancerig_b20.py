from manim import *
import numpy as np
from balancerig_helpers import make_mobile, small_label

# "The level mobile was never the homework. This is: in one sentence,
#  your own words — why did moving a light shape outward beat moving a
#  heavy one inward?"
DUR = 12.4


class BalancerigS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 1.3, 0], half_w=2.8,
                        shapes=[(-2.2, 0.9, "#C98A6B"),
                                (-0.8, 0.6, "#9BD6B0"),
                                (1.6, 0.7, "#E8C46B"),
                                (2.4, 0.7, "#9BD6B0")],
                        ceil_y=3.6)
        self.add(m["group"])
        self.wait(1.0)

        q = small_label(
            "why did light, far out  beat  heavy, near in?",
            [0, -0.6, 0], color="#EAE4D5", size=26).set_opacity(0.0)
        self.play(q.animate.set_opacity(0.95), run_time=1.6)

        # an empty line waits for the student's own sentence
        line = Line([-3.4, -1.8, 0], [3.4, -1.8, 0], color="#8C8576",
                    stroke_width=2).set_opacity(0.5)
        self.play(Create(line), run_time=1.0)
        self.wait(DUR - 4.6)   # silence — the line waits
