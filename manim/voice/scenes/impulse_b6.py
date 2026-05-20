from manim import *
import numpy as np
from impulse_helpers import force_time_graph, small_label

# "A force acting for a long time, and a much bigger force acting for an
#  instant, can do the very same job."
DUR = 9.0


class ImpulseS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        g_wide = force_time_graph("wide", width=4.0, height=2.6).move_to(
            [-3.2, 0.3, 0])
        g_narr = force_time_graph("narrow", width=4.0, height=2.6).move_to(
            [3.2, 0.3, 0])

        self.play(Create(g_wide[0]), Create(g_wide[1]),
                  Create(g_narr[0]), Create(g_narr[1]), run_time=1.2)
        self.play(FadeIn(g_wide[2]), FadeIn(g_wide[3]),
                  FadeIn(g_narr[2]), FadeIn(g_narr[3]), run_time=0.6)

        self.play(DrawBorderThenFill(g_wide.area),
                  Create(g_wide[5]), run_time=1.4)
        self.wait(0.3)
        self.play(DrawBorderThenFill(g_narr.area),
                  Create(g_narr[5]), run_time=1.4)

        l1 = small_label("long, small", [-3.2, -2.4, 0],
                         color="#8C98A6", size=24)
        l2 = small_label("brief, huge", [3.2, -2.4, 0],
                         color="#8C98A6", size=24)
        same = small_label("same job", [0, 2.6, 0],
                           color="#EAE4D5", size=30)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(same), run_time=0.9)

        # pulse both areas together to stress equality
        self.play(g_wide.area.animate.set_fill(opacity=0.75),
                  g_narr.area.animate.set_fill(opacity=0.75),
                  run_time=0.8, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 6.6)
