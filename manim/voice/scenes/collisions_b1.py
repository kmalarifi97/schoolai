from manim import *
import numpy as np
from collisions_helpers import make_cart, momentum_bar, speed_arrow

# "Two balls collide. We already know one rule never breaks:
#  total momentum stays the same."
DUR = 7.84


class CollisionsS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        bar = momentum_bar([0, 2.3, 0], frac=0.6)
        self.add(bar)

        cL = make_cart([-4.2, -0.6, 0], color="#8C95A1")
        cR = make_cart([4.2, -0.6, 0], color="#A6857A")
        aL = speed_arrow([-4.2, 0.4, 0], [1.0, 0, 0])
        aR = speed_arrow([4.2, 0.4, 0], [-1.0, 0, 0])
        self.play(FadeIn(cL), FadeIn(cR), run_time=1.0)
        self.play(GrowArrow(aL), GrowArrow(aR), run_time=0.7)

        self.play(cL.animate.move_to([-0.75, -0.6, 0]),
                  cR.animate.move_to([0.75, -0.6, 0]),
                  FadeOut(aL), FadeOut(aR),
                  run_time=1.3, rate_func=rate_functions.ease_in_quad)
        flash = Circle(radius=0.18, color="#EAE4D5", stroke_width=3
                       ).move_to([0, -0.6, 0])
        self.play(flash.animate.scale(4).set_opacity(0), run_time=0.5)
        self.play(cL.animate.move_to([-3.0, -0.6, 0]),
                  cR.animate.move_to([3.4, -0.6, 0]),
                  run_time=1.4, rate_func=rate_functions.ease_out_quad)
        self.wait(DUR - 6.4)
