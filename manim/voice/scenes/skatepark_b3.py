from manim import *
import numpy as np
from skatepark_helpers import make_ramp, ideal_arc, arc_path, board_dot

# "He starts low. He doesn't make it. He falls into the gap."
DUR = 5.6


class SkateparkS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=1.3)          # low start
        self.add(r["group"])
        ideal = ideal_arc(r["lip"], r["land_top"], peak=1.4)
        self.add(ideal)
        self.wait(0.6)
        # falls short, into the gap
        short_end = np.array([(r["gap_x0"] + r["gap_x1"]) / 2,
                              r["ground_y"] - 0.1, 0])
        path = arc_path(r["lip"], short_end, peak=0.9, color="#C98A6B")
        dot = board_dot(r["lip"])
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.8,
                  rate_func=rate_functions.ease_in_quad)
        self.play(dot.animate.set_opacity(0.0), run_time=0.5)
        self.wait(DUR - 3.4)
