from manim import *
import numpy as np
from collisionlab_helpers import (make_noura, make_brother, make_cart,
                                  table_line, momentum_bar)

# "Now she answers her brother. Not from the dent — from the numbers.
#  And she can show why."
DUR = 7.8


class CollisionlabS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.4)
        c1 = make_cart([-1.0, -0.9, 0], scale=0.9, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([1.0, -0.9, 0], scale=0.9, color="#E8C46B",
                       dented=True, facing=-1)
        no = make_noura([-3.6, -0.55, 0], scale=0.95, facing=1)
        br = make_brother([3.3, -0.65, 0], scale=0.95, facing=-1)
        self.add(tbl, c1, c2, no, br)

        # Noura points; the conserved-total bar drawn confidently above
        self.play(no[2].animate.rotate(0.4,
                  about_point=no[1].get_start()), run_time=0.8)
        bar = momentum_bar([0, 1.3, 0], length=4.4, split=0.5,
                           label=None)
        bar.set_opacity(0.0)
        self.play(bar.animate.set_opacity(1.0), run_time=1.4)
        self.wait(DUR - 3.0)
