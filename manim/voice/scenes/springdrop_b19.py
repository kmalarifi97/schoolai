from manim import *
import numpy as np
from springdrop_helpers import (make_spring, make_ball, make_bell,
                                target_line, rise_path)

# "Now he sets the real launcher. Once. The ball rises, taps the bell,
#  and falls back."
DUR = 7.5


class SpringdropS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sp = make_spring([-1.0, -2.4, 0], height=1.6, compress=0.55)
        bell = make_bell([-1.0, 2.2, 0], scale=1.0)
        bell_y = 1.92
        tl = target_line(bell_y, x0=-5.4, x1=3.6)
        start = sp["top"] + UP * 0.22
        ball = make_ball(start, r=0.24)
        self.add(sp["group"], ball, bell, tl)

        # one deliberate run: rises exactly to the bell, taps, falls
        up = rise_path(start, bell_y, color="#9BD6B0", width=3.5,
                       fall=False)
        moving = ball.copy()
        self.add(moving)
        self.play(MoveAlongPath(moving, up), run_time=2.0,
                  rate_func=rate_functions.ease_out_sine)
        # the tap: a small ring flash on the bell
        ring = Circle(radius=0.16, color="#E8C46B", stroke_width=3
                      ).move_to(bell.get_bottom())
        self.play(ring.animate.scale(2.4).set_opacity(0.0),
                  run_time=0.7)
        # falls back
        down = rise_path([moving.get_center()[0], bell_y, 0],
                         start[1], color="#9BD6B0", width=3.5,
                         fall=False)
        self.play(MoveAlongPath(moving, down), run_time=1.6,
                  rate_func=rate_functions.ease_in_sine)
        self.wait(DUR - 4.3)
