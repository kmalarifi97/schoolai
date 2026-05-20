from manim import *
import numpy as np
from elasticpe_helpers import make_bow

# "Pull a bow. It doesn't move. It just bends, and waits."
DUR = 5.4


class ElasticpeS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        relaxed = make_bow([0.6, 0, 0], draw=0.0, scale=1.4)
        self.play(FadeIn(relaxed["group"]), run_time=1.1)
        self.wait(0.5)
        drawn = make_bow([0.6, 0, 0], draw=0.85, scale=1.4)
        self.play(
            Transform(relaxed["limbs"], drawn["limbs"]),
            Transform(relaxed["string"], drawn["string"]),
            Transform(relaxed["arrow"], drawn["arrow"]),
            Transform(relaxed["nock"], drawn["nock"]),
            run_time=1.6, rate_func=rate_functions.ease_out_cubic)
        # held taut, perfectly still
        self.wait(DUR - 3.7)
