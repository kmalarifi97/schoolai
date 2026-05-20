from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                target_line, rise_path, qmark)

# "He eases off a little — and it still overshoots, by more than the
#  easing should explain."
DUR = 7.8


class SpringdropS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.55)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        bell_y = 1.95
        tl = target_line(bell_y, x0=-5.4, x1=3.6)
        start = sp["top"] + UP * 0.22
        ball = make_ball(start, r=0.24)
        self.add(sp["group"], ball, bell, tl)

        apex = 4.0
        arc = rise_path(start, apex, color="#C98A6B", width=3,
                        fall=False)
        moving = ball.copy()
        self.add(moving)
        self.play(MoveAlongPath(moving, arc), run_time=2.2,
                  rate_func=rate_functions.ease_out_sine)
        self.play(arc.animate.set_opacity(0.5), run_time=0.5)
        q = qmark([2.4, 1.8, 0], size=54)
        self.play(FadeIn(q), run_time=0.8)
        self.wait(DUR - 4.5)
