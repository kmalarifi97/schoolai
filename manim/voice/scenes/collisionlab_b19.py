from manim import *
import numpy as np
from collisionlab_helpers import run_counter, small_label

# "Her first prediction is wrong. That is not the problem. That is the
#  point. Each miss tells her which clue had fooled her."
DUR = 10.2


class CollisionlabS1B19(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the sim's result line; the prediction must converge onto it
        target = Line([-3.0, 0.6, 0], [3.0, 0.6, 0],
                      color="#9BD6B0", stroke_width=4).set_opacity(0.8)
        tl = small_label("sim", [3.6, 0.6, 0], color="#9BD6B0",
                         size=20)
        self.add(target, tl)

        pred = Line([-3.0, -1.5, 0], [3.0, -1.5, 0],
                    color="#7FB8E8", stroke_width=4)
        pl = small_label("predicted", [-4.0, -1.5, 0],
                         color="#7FB8E8", size=20)
        self.play(Create(pred), FadeIn(pl), run_time=1.0)

        rc = run_counter([0, 2.6, 0], used=0, total=3)
        self.add(rc)

        # run 1 miss -> run 2 closer -> run 3 close (converging)
        for k, y in enumerate([-0.9, 0.05, 0.5]):
            new_rc = run_counter([0, 2.6, 0], used=k + 1, total=3)
            self.play(
                pred.animate.move_to([0, y, 0]),
                Transform(rc, new_rc),
                run_time=1.4, rate_func=rate_functions.ease_in_out_sine)
            self.wait(0.4)
        self.wait(DUR - 6.4)
