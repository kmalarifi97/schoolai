from manim import *
import numpy as np
from collisionlab_helpers import make_cart, table_line, qmark, small_label

# "She wants one answer. Who was actually going faster, the moment they
#  hit?"
DUR = 6.8


class CollisionlabS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.2)
        # the collision instant: the two carts nose to nose, frozen
        c1 = make_cart([-0.75, -0.7, 0], scale=1.0, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([0.75, -0.7, 0], scale=1.0, color="#E8C46B",
                       dented=True, facing=-1)
        self.add(tbl, c1, c2)

        flash = Dot([0, -0.7, 0], radius=0.08, color="#EAE4D5")
        self.play(flash.animate.scale(6).set_opacity(0.0),
                  run_time=0.8)

        q1 = qmark([-1.6, 0.7, 0], size=44)
        q2 = qmark([1.6, 0.7, 0], size=44)
        s1 = small_label("speed?", [-1.6, 1.3, 0], color="#8C8576",
                         size=20)
        s2 = small_label("speed?", [1.6, 1.3, 0], color="#8C8576",
                         size=20)
        self.play(FadeIn(q1, shift=DOWN * 0.1),
                  FadeIn(q2, shift=DOWN * 0.1),
                  FadeIn(s1), FadeIn(s2), run_time=1.4)
        self.wait(DUR - 3.0)
