from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                target_line, rise_path)

# "One goal. The ball just reaches the bell — taps it — and no higher."
DUR = 6.3


class SpringdropS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.0)
        ball = make_ball(sp["top"] + UP * 0.22, r=0.24)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        self.add(sp["group"], ball, bell)

        bell_y = 1.95
        tl = target_line(bell_y, x0=-5.4, x1=3.6)
        self.play(Create(tl), run_time=1.4)
        arc = rise_path(sp["top"] + UP * 0.22, bell_y, color="#7FB8E8",
                        width=3, fall=False)
        self.play(Create(arc), run_time=1.6)
        self.wait(DUR - 3.0)
