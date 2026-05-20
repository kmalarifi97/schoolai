from manim import *
import numpy as np
from thermolaws_helpers import stone_tablet

# "Two rules govern every engine, every fridge, every living thing.
#  They sound almost too simple."
DUR = 8.3


class ThermolawsS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        t1 = stone_tablet([-2.6, 0, 0], scale=1.0, faint=True)
        t2 = stone_tablet([2.6, 0, 0], scale=1.0, faint=True)
        self.play(FadeIn(t1, run_time=1.6), FadeIn(t2, run_time=1.6))
        self.wait(1.0)
        # they hold, blank and waiting, a faint settle
        self.play(t1.animate.set_opacity(0.46),
                  t2.animate.set_opacity(0.46), run_time=1.4)
        self.wait(DUR - 5.6)
