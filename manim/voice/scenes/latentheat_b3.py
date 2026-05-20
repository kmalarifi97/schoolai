from manim import *
import numpy as np
from latentheat_helpers import energy_arrows, small_label

# "Energy in, no temperature rise. The heat is going somewhere we can't
#  see on the thermometer."
DUR = 8.6


class LatentheatS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # energy pouring into a flat temperature line
        arrows = energy_arrows([-3.0, 0.0, 0], n=5, length=0.9,
                               spread=1.5, y=-1.2)
        flat = Line([-1.0, 0.4, 0], [3.4, 0.4, 0], color="#E8615A",
                    stroke_width=6)
        ax = Arrow([-1.0, -1.4, 0], [-1.0, 1.4, 0], color="#8C98A6",
                   stroke_width=3, buff=0,
                   max_tip_length_to_length_ratio=0.06)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.1, run_time=1.4))
        self.play(Create(ax), Create(flat), run_time=1.2)
        tlbl = small_label("temperature", [-1.0, 1.7, 0],
                           color="#8C98A6", size=22)
        q = Text("?", font="sans", font_size=72, color="#EAE4D5"
                 ).move_to([1.2, 1.5, 0])
        self.play(FadeIn(tlbl), FadeIn(q, scale=0.6), run_time=1.0)
        self.wait(DUR - 3.6)
