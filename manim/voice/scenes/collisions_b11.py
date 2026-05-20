from manim import *
import numpy as np
from collisions_helpers import slider, steel_ball, small_label

# "Real life lives in between. Most collisions keep some bounce
#  and lose some energy."
DUR = 7.12


class CollisionsS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sl = slider([0, -1.6, 0], width=6.6, knob_frac=0.5)
        self.play(FadeIn(sl), run_time=1.0)
        self.play(sl.knob.animate.move_to(
            sl.track.get_left() + RIGHT * 6.6 * 0.62),
            run_time=1.0, rate_func=rate_functions.ease_in_out_sine)

        # a ball dropped, bouncing lower each time (real-world energy loss)
        ball = steel_ball([0, 2.6, 0], r=0.30)
        floor = Line([-2.2, 1.0, 0], [2.2, 1.0, 0],
                     color="#5A6470", stroke_width=3)
        self.play(FadeIn(ball), Create(floor), run_time=0.6)
        heights = [2.6, 2.0, 1.55, 1.25]
        xs = [0.0, 0.6, 1.05, 1.4]
        for i in range(len(heights) - 1):
            self.play(ball.animate.move_to([xs[i], 1.30, 0]),
                      run_time=0.45,
                      rate_func=rate_functions.ease_in_quad)
            self.play(ball.animate.move_to([xs[i + 1], heights[i + 1], 0]),
                      run_time=0.45,
                      rate_func=rate_functions.ease_out_quad)
        self.play(ball.animate.move_to([xs[-1] + 0.2, 1.30, 0]),
                  run_time=0.4, rate_func=rate_functions.ease_in_quad)
        self.wait(DUR - 5.8)
