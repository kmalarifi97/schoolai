from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                target_line, rise_path, small_label)

# "A heavier ball with the same press barely clears his hand. Same
#  spring, completely different height."
DUR = 8.7


class SpringdropS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.55)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        bell_y = 1.95
        tl = target_line(bell_y, x0=-5.4, x1=3.6)
        start = sp["top"] + UP * 0.22
        ball = make_ball(start, r=0.30, heavy=True)
        self.add(sp["group"], bell, tl)
        self.play(FadeIn(ball, scale=0.8), run_time=1.0)

        tag = small_label("mass?", [1.6, -1.6, 0], size=26,
                          color="#8C8576")
        self.play(FadeIn(tag), run_time=0.8)

        # same compression, barely rises
        apex = -1.4
        arc = rise_path(start, apex, color="#C98A6B", width=3)
        moving = ball.copy()
        self.add(moving)
        self.play(MoveAlongPath(moving, arc), run_time=2.0,
                  rate_func=rate_functions.ease_out_sine)
        self.play(arc.animate.set_opacity(0.5), run_time=0.5)
        self.wait(DUR - 5.3)
