from manim import *
import numpy as np
from skatepark_helpers import surface_swatch, small_label

# "He decides the wood is the problem. He sands it smooth. He waxes it."
DUR = 6.4


class SkateparkS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        rough = surface_swatch([0, 0.2, 0], waxed=False, w=5.0, h=1.1)
        self.play(FadeIn(rough), run_time=1.0)
        self.wait(0.8)
        waxed = surface_swatch([0, 0.2, 0], waxed=True, w=5.0, h=1.1)
        self.play(Transform(rough, waxed), run_time=2.0,
                  rate_func=rate_functions.ease_in_out_sine)
        glint = small_label("smooth", [0, -1.0, 0], color="#8C8576",
                            size=24)
        self.play(FadeIn(glint), run_time=0.8)
        self.wait(DUR - 4.6)
