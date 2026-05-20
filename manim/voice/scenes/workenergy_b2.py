from manim import *
import numpy as np
from workenergy_helpers import (make_figure, make_wall, small_label,
                                zero_tag)

# "You're exhausted—your muscles burned energy. But in physics, you did
#  no work on the wall. None."
DUR = 8.3


class WorkenergyS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall([1.4, 0, 0], height=4.6)
        fig = make_figure([-0.6, -0.6, 0], scale=1.05, straining=True,
                          facing=1)
        self.add(wall, fig)
        self.wait(0.8)

        lbl = small_label("work on the wall", [-1.4, 2.6, 0],
                          color="#EAE4D5", size=30)
        self.play(FadeIn(lbl, run_time=0.9))
        self.wait(0.5)
        zt = zero_tag([1.4, 2.5, 0], size=92)
        self.play(GrowFromCenter(zt), run_time=0.8)
        self.wait(0.6)
        sub = small_label("effort ≠ work", [0, -2.7, 0],
                          color="#8C98A6", size=26).set_opacity(0.85)
        self.play(FadeIn(sub, run_time=0.9))
        self.wait(DUR - 5.3)
