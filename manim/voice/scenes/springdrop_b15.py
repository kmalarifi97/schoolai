from manim import *
import numpy as np
from springdrop_helpers import energy_chain, small_label

# "Then he releases. And he watches the bars hand energy along, not the
#  ball."
DUR = 6.8


class SpringdropS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        chain = energy_chain([0, 0.0, 0], stage=0.0, scale=1.1)
        cap = small_label("elastic -> kinetic -> gravitational",
                          [0, 2.4, 0], size=22, color="#8C8576")
        flat = small_label("total flat", [0, -2.4, 0], size=22,
                           color="#8C8576")
        self.add(chain)
        self.play(FadeIn(cap), FadeIn(flat), run_time=0.8)

        for st in [0.4, 0.7, 1.0]:
            nxt = energy_chain([0, 0.0, 0], stage=st, scale=1.1)
            self.play(Transform(chain, nxt), run_time=1.3,
                      rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 4.7)
