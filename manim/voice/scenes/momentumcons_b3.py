from manim import *
import numpy as np
from momentumcons_helpers import make_figure, make_bag, label

# "Before: nothing moving. After: two things moving, opposite ways.
#  Where did that motion come from?"
DUR = 8.1


class MomentumconsS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        divider = DashedLine([0, 2.2, 0], [0, -2.6, 0],
                             color="#3A4A5A", stroke_width=2,
                             dash_length=0.14).set_opacity(0.5)
        self.add(divider)

        # BEFORE panel (left): figure + bag together, still
        before_t = label("before", (-3.2, 2.6, 0), color="#8C98A6", size=24)
        f0 = make_figure((-3.6, 0.1, 0), scale=0.7)
        b0 = make_bag((-2.7, 0.1, 0), scale=0.62)
        self.play(FadeIn(before_t), FadeIn(f0), FadeIn(b0), run_time=1.1)
        self.wait(0.6)

        # AFTER panel (right): figure left, bag right, arrows opposite
        after_t = label("after", (3.2, 2.6, 0), color="#8C98A6", size=24)
        f1 = make_figure((2.0, 0.1, 0), scale=0.7)
        b1 = make_bag((5.0, 0.1, 0), scale=0.62)
        a_f = Arrow([2.6, -0.9, 0], [1.3, -0.9, 0], color="#E8A07F",
                    stroke_width=5, buff=0,
                    max_tip_length_to_length_ratio=0.3)
        a_b = Arrow([4.4, -0.9, 0], [5.7, -0.9, 0], color="#7FB8E8",
                    stroke_width=5, buff=0,
                    max_tip_length_to_length_ratio=0.3)
        self.play(FadeIn(after_t), FadeIn(f1), FadeIn(b1), run_time=1.0)
        self.play(GrowArrow(a_f), GrowArrow(a_b), run_time=1.0)

        q = Text("?", font="sans", font_size=66, color="#EAE4D5"
                 ).move_to([0, -1.9, 0])
        self.play(FadeIn(q, scale=0.6), run_time=0.9)
        self.wait(DUR - 5.6)
