from manim import *
import numpy as np
from springdrop_helpers import energy_chain, small_label

# "Spring energy becomes motion becomes height. The same total, just
#  changing form — and a heavier ball turns the same total into less
#  height."
DUR = 11.5


class SpringdropS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        chain = energy_chain([0, 0.2, 0], stage=0.0, scale=1.05)
        self.play(FadeIn(chain), run_time=1.2)

        # sweep the energy along the chain: spring -> motion -> height
        for st in [0.25, 0.5, 0.75, 1.0]:
            nxt = energy_chain([0, 0.2, 0], stage=st, scale=1.05)
            self.play(Transform(chain, nxt), run_time=1.3,
                      rate_func=rate_functions.ease_in_out_sine)

        tag = small_label("same total", [0, 2.4, 0], size=26,
                          color="#8C8576")
        self.play(FadeIn(tag), run_time=0.8)

        # heavier ball -> same total, shorter height bar
        heavy = energy_chain([0, 0.2, 0], stage=1.0, heavy=True,
                             scale=1.05)
        tag2 = small_label("heavier ball -> less height",
                           [0, -2.4, 0], size=24, color="#8C8576")
        self.play(Transform(chain, heavy), FadeIn(tag2),
                  run_time=1.6)
        self.wait(DUR - 8.5)
