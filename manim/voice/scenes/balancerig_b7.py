from manim import *
import numpy as np
from balancerig_helpers import make_mobile, small_label

# "She wasn't short of shapes. She was short of the thing that decides
#  tilt — not weight, but weight times its reach."
DUR = 9.7


class BalancerigS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 1.0, 0], half_w=2.8,
                        shapes=[(-2.0, 0.9, "#C98A6B"),
                                (-0.7, 0.6, "#9BD6B0"),
                                (1.6, 0.8, "#E8C46B")],
                        ceil_y=3.4)
        self.add(m["group"])
        self.wait(0.6)
        # the shapes fade away, leaving the idea
        self.play(m["group"].animate.set_opacity(0.12), run_time=1.6)

        prod = Text("weight  ×  reach", font="sans", font_size=44,
                    color="#EAE4D5").move_to([0, 0.2, 0])
        prod.set_opacity(0.0)
        self.play(prod.animate.set_opacity(0.95), run_time=1.4)
        sub = small_label("not weight alone", [0, -1.1, 0],
                          color="#8C8576", size=24).set_opacity(0.0)
        self.play(sub.animate.set_opacity(0.85), run_time=1.0)
        self.wait(DUR - 4.6)
