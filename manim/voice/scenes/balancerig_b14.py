from manim import *
import numpy as np
from balancerig_helpers import balancing_act, small_label, qmark

# "Where must the last mass go so the left and right twists match — and
#  the plank stays level when she lets go?"
DUR = 9.3


class BalancerigS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        b = balancing_act([0, -0.4, 0], half_w=3.2,
                          bricks=[(-3, 2)], scale=1.0)
        self.add(b["group"])
        self.wait(0.4)

        # an x = ? blank where the last brick must go (right side)
        step = b["step"]
        cx = b["group"].get_center()
        xpos = np.array([cx[0] + 2 * step, cx[1] + 0.55, 0])
        blank = DashedVMobject(
            Rectangle(width=0.5, height=0.6, stroke_color="#8C8576",
                      stroke_width=2, fill_opacity=0),
            num_dashes=18).move_to(xpos)
        q = qmark(xpos + np.array([0, 0.0, 0]), size=40, color="#E8C46B",
                  opacity=0.85)
        self.play(Create(blank), FadeIn(q), run_time=1.2)

        rel = Text("τ_left  =  τ_right", font="sans", font_size=36,
                   color="#EAE4D5").move_to([0, 2.4, 0])
        self.play(Write(rel), run_time=1.4)
        self.play(FadeIn(small_label("x = ?", [xpos[0], cx[1] + 1.4, 0],
                                     color="#E8C46B", size=24)),
                  run_time=0.9)
        self.wait(DUR - 4.9)
