from manim import *
import numpy as np
from collisionlab_helpers import (make_noura, make_brother, make_cart,
                                  table_line)

# "Two toy carts collided on the table. One ended up dented. Noura's
#  little brother says his cart was barely moving."
DUR = 9.6


class CollisionlabS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.2)
        self.play(Create(tbl), run_time=1.0)

        c1 = make_cart([-1.2, -0.7, 0], scale=1.0, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([1.0, -0.7, 0], scale=1.0, color="#E8C46B",
                       dented=True, facing=-1)
        self.play(FadeIn(c1, shift=UP * 0.15),
                  FadeIn(c2, shift=UP * 0.15), run_time=1.6)

        no = make_noura([-3.6, -0.35, 0], scale=1.0, facing=1)
        br = make_brother([3.3, -0.45, 0], scale=1.0, facing=-1)
        self.play(FadeIn(no), run_time=1.0)
        self.play(FadeIn(br), run_time=1.0)
        # brother gestures at his cart (a small point), Noura skeptical
        self.play(br[2].animate.rotate(-0.3,
                  about_point=br[1].get_start()), run_time=0.9)
        self.wait(DUR - 5.5)
