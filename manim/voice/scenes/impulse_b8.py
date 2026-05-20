from manim import *
import numpy as np
from impulse_helpers import (force_time_graph, momentum_bar,
                             small_label, big_label, AREA_COL, P_COLOR)

# "And the impulse equals exactly the change in momentum. That's the
#  whole bridge."
DUR = 7.2


class ImpulseS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        g = force_time_graph("wide", width=3.6, height=2.4).move_to(
            [-3.4, 0.4, 0])
        self.add(g[0], g[1], g[5])
        self.play(DrawBorderThenFill(g.area), run_time=1.1)
        il = small_label("impulse", [-3.4, -1.6, 0], color=AREA_COL,
                         size=26)
        self.play(FadeIn(il), run_time=0.6)

        eq = big_label("=", [0, 0.4, 0], color="#EAE4D5", size=60)
        self.play(Write(eq), run_time=0.7)

        bar = momentum_bar(0.55, length=2.8, height=0.55,
                           show_label=False).move_to([3.4, 0.4, 0])
        dp = small_label("change in p", [3.4, -1.6, 0], color=P_COLOR,
                         size=26)
        self.play(GrowFromEdge(bar, LEFT), FadeIn(dp), run_time=1.1)

        bridge = small_label("the whole bridge", [0, -2.7, 0],
                             color="#8C98A6", size=26)
        self.play(FadeIn(bridge), run_time=0.8)
        self.wait(DUR - 4.3)
