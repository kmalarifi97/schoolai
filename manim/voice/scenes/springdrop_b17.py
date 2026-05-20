from manim import *
import numpy as np
from springdrop_helpers import compression_control, run_counter

# "He adjusts the compression. Predicts again. Three tries. That's all
#  he gets."
DUR = 7.0


class SpringdropS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cc = compression_control([0, 0.8, 0], frac=0.35, w=3.4)
        rc = run_counter([-0.8, -1.6, 0], used=0, total=3)
        self.play(FadeIn(cc), run_time=1.0)
        # nudge it deliberately, not random
        self.play(cc[0][1].animate.shift(RIGHT * 0.7), run_time=1.4,
                  rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(rc), run_time=1.0)
        self.wait(DUR - 3.4)
