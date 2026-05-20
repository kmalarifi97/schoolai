from manim import *
import numpy as np
from skatepark_helpers import energy_bar, surface_swatch, small_label

# "And the rough wood quietly ate some of it — turned it into heat. Wax
#  the ramp, less is eaten, he goes further."
DUR = 9.4


class SkateparkS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # rough case: a thick heat stream siphons off
        sw_r = surface_swatch([-3.4, 1.8, 0], waxed=False, w=3.0, h=0.6)
        lblr = small_label("rough", [-3.4, 1.2, 0], color="#8C8576",
                           size=20)
        stored = energy_bar("stored", 0.85, [-3.4, -1.0, 0],
                            color="#7FB8E8", max_h=2.4)
        heat_r = energy_bar("heat", 0.35, [-1.6, -1.0, 0],
                            color="#D98C5F", max_h=2.4)
        speed_r = energy_bar("speed", 0.5, [-0.2, -1.0, 0],
                             color="#E8C46B", max_h=2.4)
        self.play(FadeIn(sw_r), FadeIn(lblr), FadeIn(stored),
                  run_time=1.0)
        self.play(FadeIn(heat_r), FadeIn(speed_r), run_time=1.2)
        self.wait(0.8)

        # waxed case: thin heat stream, more speed
        sw_w = surface_swatch([3.4, 1.8, 0], waxed=True, w=3.0, h=0.6)
        lblw = small_label("waxed", [3.4, 1.2, 0], color="#8C8576",
                           size=20)
        heat_w = energy_bar("heat", 0.10, [2.0, -1.0, 0],
                            color="#D98C5F", max_h=2.4)
        speed_w = energy_bar("speed", 0.75, [3.4, -1.0, 0],
                             color="#E8C46B", max_h=2.4)
        self.play(FadeIn(sw_w), FadeIn(lblw), FadeIn(heat_w),
                  FadeIn(speed_w), run_time=1.4)
        self.wait(DUR - 5.4)
