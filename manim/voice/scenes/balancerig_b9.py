from manim import *
import numpy as np
from balancerig_helpers import make_mobile, twist_arrow, small_label

# "Level means the left twists and the right twists cancel. Exactly.
#  The total turning effect is zero."
DUR = 8.6


class BalancerigS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.7, 0], half_w=3.0,
                        shapes=[(-2.4, 0.9, "#C98A6B"),
                                (2.0, 1.0, "#E8C46B")],
                        ceil_y=3.4)
        self.add(m["group"])
        by = m["bar"].get_center()[1]
        self.wait(0.4)

        # equal and opposite turning arrows: left CCW, right CW
        la = twist_arrow(np.array([-2.0, by + 0.55, 0]), 0.9, 2.4,
                         side="left")
        ra = twist_arrow(np.array([2.0, by + 0.55, 0]), 1.0, 2.0,
                         side="right")
        ll = small_label("left twist", [-3.0, by + 1.7, 0],
                         color="#7FB8E8", size=20)
        rl = small_label("right twist", [3.0, by + 1.7, 0],
                         color="#E8C46B", size=20)
        self.play(FadeIn(la), FadeIn(ll), run_time=1.0)
        self.play(FadeIn(ra), FadeIn(rl), run_time=1.0)
        self.wait(0.6)

        # they cancel -> collapse into a clean 0
        zero = Text("0", font="sans", font_size=84, color="#EAE4D5"
                    ).move_to([0, by - 0.1, 0])
        self.play(
            la.animate.move_to([0, by - 0.1, 0]).scale(0.2
                                                       ).set_opacity(0),
            ra.animate.move_to([0, by - 0.1, 0]).scale(0.2
                                                       ).set_opacity(0),
            run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.play(Write(zero), run_time=0.9)
        self.play(FadeIn(small_label("total turning effect",
                                     [0, by - 1.4, 0],
                                     color="#8C8576", size=22)),
                  run_time=0.7)
        self.wait(DUR - 6.5)
