from manim import *
import numpy as np
from balancerig_helpers import make_mobile, qmark

# "She adds a small shape near the string. It barely changes anything.
#  She doesn't see why."
DUR = 7.8


class BalancerigS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        m = make_mobile([0, 0.3, 0], half_w=3.0,
                        shapes=[(-1.8, 0.9, "#C98A6B"),
                                (1.9, 0.7, "#9BD6B0")],
                        ceil_y=3.4)
        pv = m["string"].get_end()
        m["rig"].rotate(0.30, about_point=pv)   # tilted a bit left
        self.add(m["ceiling"], m["string"], m["rig"])
        self.wait(0.5)

        # a small shape placed near the center pivot
        thread = Line([0.35, 0.22, 0], [0.35, -0.10, 0],
                      color="#B8B0A0", stroke_width=1.5)
        small = Circle(radius=0.16, fill_color="#9BD6B0",
                       fill_opacity=1, stroke_color="#EAE4D5",
                       stroke_width=1.5).move_to([0.35, -0.26, 0])
        near = VGroup(thread, small)
        near.rotate(0.30, about_point=pv)
        self.play(FadeIn(near, shift=UP * 0.2), run_time=1.0)
        m["rig"].add(near)
        # it barely changes anything
        self.play(Rotate(m["rig"], angle=-0.04, about_point=pv),
                  run_time=1.2,
                  rate_func=rate_functions.ease_in_out_sine)
        q = qmark([3.4, 0.4, 0], size=44).set_opacity(0.0)
        self.play(q.animate.set_opacity(0.55), run_time=1.0)
        self.wait(DUR - 4.7)
