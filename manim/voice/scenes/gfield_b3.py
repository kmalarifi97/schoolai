from manim import *
import numpy as np
from gfield_helpers import make_earth, make_rock, small_label

# "Newton himself was uneasy about this. Action at a distance, across
#  empty space, with nothing in between."
DUR = 9.0


class GfieldS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        earth = make_earth([0, -2.7, 0]).scale(1.7)
        rock = make_rock(7, scale=0.36).move_to([0, 1.5, 0])
        self.add(earth, rock)
        self.wait(0.8)
        # highlight the empty gap between them
        gap = DashedLine([0, 1.05, 0], [0, -1.55, 0],
                         color="#5A6E80", stroke_width=2,
                         dash_length=0.12).set_opacity(0.7)
        brace_l = Line([-0.5, 1.05, 0], [0.5, 1.05, 0],
                       color="#5A6E80", stroke_width=2).set_opacity(0.6)
        brace_r = Line([-0.5, -1.55, 0], [0.5, -1.55, 0],
                       color="#5A6E80", stroke_width=2).set_opacity(0.6)
        self.play(Create(gap), FadeIn(brace_l), FadeIn(brace_r),
                  run_time=1.4)
        lbl = small_label("nothing in between", [0, -0.25, 0],
                          color="#8C98A6", size=24)
        self.play(FadeIn(lbl), run_time=1.0)
        self.wait(DUR - 4.2)
