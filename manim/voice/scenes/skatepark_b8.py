from manim import *
import numpy as np
from skatepark_helpers import make_ramp, plywood_stack

# "He raises, lowers, sands, guesses. He is almost out of plywood, and
#  out of patience."
DUR = 7.5


class SkateparkS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.0)
        self.add(r["group"])

        # a start-height marker jittering up and down
        marker = Line([r["lip"][0] - 0.5, r["lip"][1], 0],
                      [r["lip"][0] + 0.5, r["lip"][1], 0],
                      color="#EAE4D5", stroke_width=4).set_opacity(0.8)
        self.add(marker)
        gy = r["ground_y"]
        for h in [2.8, 1.5, 3.1, 1.9, 2.5, 1.3]:
            self.play(marker.animate.move_to([r["lip"][0], gy + h, 0]),
                      run_time=0.5)

        # dwindling stack alongside
        stack = plywood_stack([5.0, gy + 0.4, 0], n=6, w=1.5)
        self.add(stack)
        for k in range(4):
            self.play(FadeOut(stack[-1 - k], shift=UP * 0.1),
                      run_time=0.3)
        self.wait(DUR - 5.7)
