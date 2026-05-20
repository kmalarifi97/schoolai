from manim import *
import numpy as np
from machines_helpers import work_bars, small_label

# "In a perfect machine, what you put in equals what you get out. Force
#  times distance, conserved."
DUR = 7.5


class MachinesS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wb = work_bars([0.4, 0.2, 0], scale=1.15, in_w=3.4, out_w=3.4)
        in_bar, out_bar, in_lbl, out_lbl = wb
        self.play(FadeIn(in_lbl), FadeIn(out_lbl), run_time=0.8)
        self.play(GrowFromEdge(in_bar, LEFT), run_time=1.1)
        self.play(GrowFromEdge(out_bar, LEFT), run_time=1.1)
        self.wait(0.4)

        eq = small_label("work in  =  work out", [0.4, -2.4, 0],
                         color="#EAE4D5", size=30)
        self.play(FadeIn(eq), run_time=0.9)
        # pulse both equally to stress the equality
        self.play(in_bar.animate.set_opacity(1.0),
                  out_bar.animate.set_opacity(1.0),
                  run_time=0.8, rate_func=rate_functions.there_and_back)
        self.wait(DUR - 5.1)
