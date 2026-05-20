from manim import *
import numpy as np
from impulse_helpers import (force_time_graph, momentum_bar,
                             small_label, big_label, AREA_COL, P_COLOR)

# "Computing the impulse from a force acting over a time interval, and
#  the change in momentum it produces — that's yours."
DUR = 10.0


class ImpulseS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        g = force_time_graph("wide", width=3.8, height=2.6).move_to(
            [-3.4, 0.4, 0])
        self.play(Create(g[0]), Create(g[1]), run_time=0.9)
        self.play(DrawBorderThenFill(g.area), Create(g[5]),
                  run_time=1.2)
        il = small_label("impulse", [-3.4, -1.6, 0], color=AREA_COL,
                         size=26)
        self.play(FadeIn(il), run_time=0.5)

        eq = big_label("=", [0, 0.4, 0], color="#EAE4D5", size=58)
        self.play(Write(eq), run_time=0.6)

        bar = momentum_bar(0.55, length=2.8, height=0.55,
                           show_label=False).move_to([3.4, 0.4, 0])
        dp = small_label("change in p", [3.4, -1.6, 0], color=P_COLOR,
                         size=26)
        self.play(GrowFromEdge(bar, LEFT), FadeIn(dp), run_time=1.0)

        # time left as an open knob
        knob = small_label("time — left to you",
                           g.axes_origin + np.array([1.9, -0.55, 0]),
                           color="#8C98A6", size=22)
        self.play(FadeIn(knob), run_time=0.7)

        yours = small_label("that's yours", [0, -2.9, 0],
                            color="#EAE4D5", size=28)
        self.play(FadeIn(yours), run_time=0.9)
        self.wait(DUR - 6.8)
