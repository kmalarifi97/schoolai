from manim import *
import numpy as np
from collisionlab_helpers import make_cart, table_line, small_label

# "Her brother runs it again. Same carts. This time the dented one was
#  clearly the fast one. Her rule just broke."
DUR = 9.4


class CollisionlabS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.0)
        self.add(tbl)

        # the previously-"slow" (dented) cart now comes in clearly fast
        c_fast = make_cart([-5.0, -0.5, 0], scale=1.0, color="#E8C46B",
                           dented=True, facing=1)
        c_slow = make_cart([1.4, -0.5, 0], scale=1.0, color="#7FB8E8",
                           facing=-1)
        self.add(c_fast, c_slow)

        # fast streak lines behind the dented cart
        streaks = VGroup(*[
            Line([-5.9, -0.5 + dy, 0], [-5.3, -0.5 + dy, 0],
                 color="#8C8576", stroke_width=2).set_opacity(0.5)
            for dy in (-0.2, 0.0, 0.2)])
        self.play(FadeIn(streaks), run_time=0.5)
        self.play(c_fast.animate.move_to([0.5, -0.5, 0]),
                  streaks.animate.shift(RIGHT * 5.5).set_opacity(0.0),
                  run_time=1.4, rate_func=rate_functions.ease_in_sine)
        # impact
        flash = Dot([0.9, -0.5, 0], radius=0.06, color="#EAE4D5")
        self.play(flash.animate.scale(7).set_opacity(0.0),
                  c_slow.animate.shift(RIGHT * 0.9),
                  run_time=0.7)

        rule = small_label("dent = slower", [0, 1.5, 0],
                           color="#8C8576", size=26)
        strike = Line(rule.get_left() + LEFT * 0.1,
                      rule.get_right() + RIGHT * 0.1,
                      color="#C98A6B", stroke_width=4)
        self.play(FadeIn(rule), run_time=0.8)
        self.play(Create(strike), run_time=0.9)
        self.wait(DUR - 6.0)
