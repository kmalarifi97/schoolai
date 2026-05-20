from manim import *
import numpy as np
from skatepark_helpers import make_ramp, energy_bar, board_dot

# "Every failed run was energy he didn't count. The height he started
#  from — that became his speed at the bottom."
DUR = 9.4


class SkateparkS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.6)
        ramp = r["group"].scale(0.8).to_edge(LEFT, buff=0.4)
        self.add(ramp)
        self.wait(0.5)

        stored = energy_bar("stored", 0.9, [2.2, 0.0, 0],
                            color="#7FB8E8", max_h=2.8)
        speed = energy_bar("speed", 0.05, [3.6, 0.0, 0],
                           color="#E8C46B", max_h=2.8)
        self.play(FadeIn(stored), FadeIn(speed), run_time=1.0)
        self.wait(0.6)

        # board descends; stored pours into speed
        dot = board_dot(r["lip"]).scale(0.8).move_to(
            ramp[0].get_top())
        self.add(dot)
        new_stored = energy_bar("stored", 0.08, [2.2, 0.0, 0],
                                color="#7FB8E8", max_h=2.8)
        new_speed = energy_bar("speed", 0.88, [3.6, 0.0, 0],
                               color="#E8C46B", max_h=2.8)
        self.play(
            dot.animate.move_to(ramp[0].get_corner(DL) + RIGHT * 0.2),
            Transform(stored, new_stored),
            Transform(speed, new_speed),
            run_time=2.4, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 4.5)
