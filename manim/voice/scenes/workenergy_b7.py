from manim import *
import numpy as np
from workenergy_helpers import make_cart, work_region, EnergyBar

# "That motion is itself a kind of energy — energy of movement. The
#  work became speed."
DUR = 7.5


class WorkenergyS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cart = make_cart([-3.6, 1.4, 0], scale=0.9)
        self.add(cart)

        rect, rlbl = work_region([-5.0, -1.9, 0], w=3.0, h=1.2,
                                 label="W")
        self.play(FadeIn(rect), Write(rlbl), run_time=1.0)
        self.wait(0.5)

        bar = EnergyBar([3.4, -0.2, 0], height=3.0,
                        label="energy of motion")
        bar.set_level(0.001)
        self.play(FadeIn(bar.frame), FadeIn(bar.caption), run_time=0.8)

        # the work shading transforms into the motion-energy bar
        target = rect.copy()
        self.play(Transform(rect, bar.frame.copy().set_fill(
                      "#9CC97F", 0.0).set_stroke(width=0)),
                  FadeOut(rlbl), run_time=1.0)
        self.remove(rect)

        def fill(m, a):
            m.set_level(a)
        self.play(UpdateFromAlphaFunc(bar, fill), run_time=1.6)
        self.wait(DUR - 5.7)
