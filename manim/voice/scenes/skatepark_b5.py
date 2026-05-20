from manim import *
import numpy as np
from skatepark_helpers import make_ramp, arc_path, board_dot

# "He lowers it a little. Short again."
DUR = 4.0


class SkateparkS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r_hi = make_ramp(launch_h=3.0)
        self.add(r_hi["group"])
        r_mid = make_ramp(launch_h=2.4)      # lowered a notch
        self.play(Transform(r_hi["group"], r_mid["group"]), run_time=1.0)
        short_end = np.array([r_mid["gap_x1"] - 0.3,
                              r_mid["ground_y"] - 0.05, 0])
        path = arc_path(r_mid["lip"], short_end, peak=1.2,
                        color="#C98A6B")
        dot = board_dot(r_mid["lip"])
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.5,
                  rate_func=rate_functions.ease_in_quad)
        self.play(dot.animate.set_opacity(0.0), run_time=0.3)
        self.wait(DUR - 2.8)
