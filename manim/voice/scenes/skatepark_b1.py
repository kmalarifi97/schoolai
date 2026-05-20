from manim import *
import numpy as np
from skatepark_helpers import make_ramp, make_faris

# "Faris built a ramp out of plywood. A launch on one side, a gap, a
#  landing on the other."
DUR = 7.8


class SkateparkS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.0)
        launch, gap, landing, face = r["group"]
        self.play(FadeIn(launch, shift=UP * 0.2), run_time=1.4)
        self.play(Create(gap), run_time=1.0)
        self.play(FadeIn(landing, shift=UP * 0.2), run_time=1.4)
        faris = make_faris([-3.0, r["ground_y"] + 0.7, 0], scale=0.9)
        self.play(FadeIn(faris, shift=UP * 0.15), run_time=1.0)
        self.wait(DUR - 4.8)
