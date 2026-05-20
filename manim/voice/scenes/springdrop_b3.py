from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                target_line, rise_path)

# "He presses the spring a little. The ball pops up and falls short,
#  well below the bell."
DUR = 7.7


class SpringdropS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.0)
        ball = make_ball(sp["top"] + UP * 0.22, r=0.24)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        bell_y = 1.95
        tl = target_line(bell_y, x0=-5.4, x1=3.6)
        self.add(sp["group"], ball, bell, tl)

        # small compression
        sp2 = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.25)
        start = sp2["top"] + UP * 0.22
        self.play(Transform(sp["group"], sp2["group"]),
                  ball.animate.move_to(start), run_time=1.4)

        apex = -0.4
        arc = rise_path(start, apex, color="#C98A6B", width=3)
        moving = ball.copy()
        self.add(moving)
        self.play(MoveAlongPath(moving, arc), run_time=2.4,
                  rate_func=rate_functions.ease_out_sine)
        self.play(FadeIn(arc.set_opacity(0.5)), run_time=0.6)
        self.wait(DUR - 4.4)
