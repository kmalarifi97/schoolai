from manim import *
import numpy as np
from skatepark_helpers import make_ramp, arc_path, board_dot

# "Now he builds the real ramp. Once. And the landing is clean."
DUR = 5.8


class SkateparkS1B22(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.5)
        self.play(FadeIn(r["group"]), run_time=1.2)
        self.wait(0.5)
        # one start height, set with intent — lands clean on far ramp
        path = arc_path(r["lip"], r["land_top"], peak=1.5,
                        color="#9BD6B0", width=4)
        dot = board_dot(r["lip"])
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        # rolls down the landing, settles
        self.play(dot.animate.move_to(r["land_lo"]), run_time=0.8,
                  rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 4.5)
