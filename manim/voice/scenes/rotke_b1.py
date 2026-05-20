from manim import *
import numpy as np
from rotke_helpers import make_flywheel, axis_pin

# "A spinning flywheel, going nowhere. Its center never moves."
DUR = 5.7


class RotkeS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = [0, 0, 0]
        fw = make_flywheel(C, radius=1.9)
        pin = axis_pin(C, scale=1.2)
        self.play(FadeIn(fw, scale=0.85), run_time=1.0)
        self.add(pin)
        self.play(Rotate(fw, angle=-TAU * 1.4, about_point=np.array(C)),
                  run_time=DUR - 1.4,
                  rate_func=linear)
        self.wait(0.4)
