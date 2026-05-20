from manim import *
import numpy as np
from skatepark_helpers import make_ramp, arc_path, board_dot

# "So he builds the launch higher. Now he overshoots — flies past the
#  landing, and crashes."
DUR = 7.8


class SkateparkS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r_lo = make_ramp(launch_h=1.3)
        self.add(r_lo["group"])
        self.wait(0.4)
        r_hi = make_ramp(launch_h=3.0)       # raised launch
        self.play(Transform(r_lo["group"], r_hi["group"]), run_time=1.6)
        self.wait(0.4)
        over_end = np.array([6.4, r_hi["ground_y"] - 0.1, 0])
        path = arc_path(r_hi["lip"], over_end, peak=1.6,
                        color="#C98A6B")
        dot = board_dot(r_hi["lip"])
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=2.0,
                  rate_func=rate_functions.ease_in_quad)
        self.play(Flash(dot, color="#C98A6B", flash_radius=0.5),
                  run_time=0.6)
        self.play(dot.animate.set_opacity(0.0), run_time=0.4)
        self.wait(DUR - 6.0)
