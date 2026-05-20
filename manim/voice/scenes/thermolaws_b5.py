from manim import *
import numpy as np
from thermolaws_helpers import stone_tablet, tablet_arrow, small_label

# "Then the second rule, the strange one. It's about direction."
DUR = 5.5


class ThermolawsS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        t2 = stone_tablet([0, 0.1, 0], scale=1.1, faint=False)
        self.play(FadeIn(t2), run_time=1.2)
        self.wait(0.4)
        roman = small_label("II", [0, 1.3, 0], size=46, color="#5C5750")
        arr = tablet_arrow(t2)
        self.play(Write(roman), run_time=0.8)
        self.play(GrowArrow(arr), run_time=1.2)
        self.wait(DUR - 3.6)
