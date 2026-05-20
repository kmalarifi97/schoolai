from manim import *
import numpy as np
from collisionlab_helpers import make_cart, table_line, small_label, qmark

# "She tries reading speed from how far they slid after. But a heavy
#  cart and a light cart slide differently from the same hit."
DUR = 10.4


class CollisionlabS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.6)
        self.add(tbl)

        # heavy cart slides a little; light cart slides far
        heavy = make_cart([-2.6, -1.05, 0], scale=1.0, color="#7FB8E8",
                          facing=1)
        light = make_cart([-2.6, 0.6, 0], scale=0.8, color="#E8C46B",
                          facing=1)
        self.add(heavy, light)

        t_heavy = DashedLine([-1.9, -1.05, 0], [-0.4, -1.05, 0],
                             color="#8C8576", stroke_width=2,
                             dash_length=0.08).set_opacity(0.6)
        t_light = DashedLine([-1.9, 0.6, 0], [3.4, 0.6, 0],
                             color="#8C8576", stroke_width=2,
                             dash_length=0.08).set_opacity(0.6)
        self.play(
            heavy.animate.move_to([-0.4, -1.05, 0]),
            Create(t_heavy),
            run_time=1.4, rate_func=rate_functions.ease_out_sine)
        self.play(
            light.animate.move_to([3.4, 0.6, 0]),
            Create(t_light),
            run_time=1.8, rate_func=rate_functions.ease_out_sine)

        s1 = small_label("heavy", [-3.4, -1.05, 0], color="#8C8576",
                         size=20)
        s2 = small_label("light", [-3.4, 0.6, 0], color="#8C8576",
                         size=20)
        tag = small_label("same hit, different slide", [0, 1.9, 0],
                          color="#EAE4D5", size=22)
        q = qmark([2.7, 1.9, 0], size=34)
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(tag), run_time=1.2)
        self.play(FadeIn(q), run_time=0.7)
        self.wait(DUR - 6.8)
