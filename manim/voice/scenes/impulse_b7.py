from manim import *
import numpy as np
from impulse_helpers import force_time_graph, small_label, AREA_COL

# "It's force multiplied by the time it acts. That product is the
#  impulse."
DUR = 6.6


class ImpulseS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        g = force_time_graph("wide", width=5.4, height=3.2).move_to(
            [0, 0.1, 0])
        self.add(g[0], g[1], g[2], g[3], g[5])
        self.play(DrawBorderThenFill(g.area), run_time=1.2)

        # highlight the area
        self.play(g.area.animate.set_fill(opacity=0.8), run_time=0.7,
                  rate_func=rate_functions.there_and_back)

        lbl = small_label("impulse  =  force × time",
                          [0, -2.7, 0], color=AREA_COL, size=34)
        self.play(Write(lbl), run_time=1.1)
        self.wait(DUR - 3.0)
