from manim import *
import numpy as np
from weightless_helpers import ballistic_arc, small_label

# "Now the trick. Throw a ball. It curves down and hits the ground."
DUR = 6.0


class WeightlessS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        ground = Line([-6.5, -2.6, 0], [6.5, -2.6, 0],
                      color="#3A8B6B", stroke_width=4)
        hill = VMobject(stroke_color="#3A8B6B", stroke_width=4)
        hill.set_points_smoothly([
            np.array([-6.5, -2.6, 0]), np.array([-4.5, -1.6, 0]),
            np.array([-3.6, -1.2, 0]), np.array([-2.8, -1.35, 0]),
            np.array([-1.0, -2.2, 0]), np.array([1.0, -2.6, 0])])
        self.play(Create(ground), Create(hill), run_time=1.0)

        launch = np.array([-3.6, -1.0, 0])
        ball = Dot(launch, radius=0.12, color="#E8C97F")
        self.play(FadeIn(ball, scale=0.5), run_time=0.6)

        arc = ballistic_arc(launch, vx=2.6, g=5.0, t_max=1.45,
                            color="#E8C97F")
        self.play(MoveAlongPath(ball, arc),
                  Create(arc), run_time=1.8,
                  rate_func=rate_functions.linear)
        self.add(small_label("hits the ground", [2.4, -2.0, 0], size=22))
        self.wait(DUR - 3.4)
