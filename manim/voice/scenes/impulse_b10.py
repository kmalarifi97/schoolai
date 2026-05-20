from manim import *
import numpy as np
from impulse_helpers import force_time_graph, small_label

# "— so the force needed drops. The rigid car stops in an instant, and
#  the force spikes."
DUR = 7.6


class ImpulseS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        g_c = force_time_graph("wide", width=4.0, height=2.6).move_to(
            [-3.2, 0.3, 0])
        g_r = force_time_graph("narrow", width=4.0, height=2.6).move_to(
            [3.2, 0.3, 0])

        self.add(g_c[0], g_c[1], g_c[2], g_c[3], g_c[5],
                 g_r[0], g_r[1], g_r[2], g_r[3], g_r[5])

        self.play(DrawBorderThenFill(g_c.area), run_time=1.2)
        c1 = small_label("crumple: long, low", [-3.2, -2.4, 0],
                         color="#8C98A6", size=24)
        self.play(FadeIn(c1), run_time=0.6)
        self.wait(0.4)

        self.play(DrawBorderThenFill(g_r.area), run_time=1.0)
        c2 = small_label("rigid: instant, huge", [3.2, -2.4, 0],
                         color="#C96A5A", size=24)
        # the spike pulse
        self.play(FadeIn(c2),
                  g_r.area.animate.set_fill(opacity=0.85),
                  run_time=0.8, rate_func=rate_functions.there_and_back)

        same = small_label("equal areas — same momentum removed",
                           [0, 2.7, 0], color="#EAE4D5", size=24)
        self.play(FadeIn(same), run_time=0.8)
        self.wait(DUR - 4.8)
