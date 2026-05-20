from manim import *
import numpy as np
from springdrop_helpers import energy_bar, small_label

# "And the speed buys height — trading itself away as the ball climbs,
#  until none is left and it stops at the top."
DUR = 9.5


class SpringdropS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        speed_b = energy_bar("speed", 0.95, [-2.4, 0, 0],
                             color="#E8C46B", max_h=3.0, w=0.8)
        height_b = energy_bar("height", 0.05, [2.4, 0, 0],
                              color="#9BD6B0", max_h=3.0, w=0.8)
        arr = Arrow([-1.6, 0.2, 0], [1.6, 0.2, 0], color="#8C8576",
                    stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.18)
        arr.set_opacity(0.6)
        self.play(FadeIn(speed_b), FadeIn(height_b), GrowArrow(arr),
                  run_time=1.2)

        new_speed = energy_bar("speed", 0.02, [-2.4, 0, 0],
                               color="#E8C46B", max_h=3.0, w=0.8)
        new_height = energy_bar("height", 0.95, [2.4, 0, 0],
                                color="#9BD6B0", max_h=3.0, w=0.8)
        self.play(Transform(speed_b, new_speed),
                  Transform(height_b, new_height),
                  run_time=3.0, rate_func=rate_functions.ease_out_sine)
        tag = small_label("speed = 0 at the top", [0, -2.4, 0],
                          size=24, color="#8C8576")
        self.play(FadeIn(tag), run_time=1.0)
        self.wait(DUR - 5.2)
