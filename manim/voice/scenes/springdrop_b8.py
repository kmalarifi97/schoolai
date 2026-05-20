from manim import *
import numpy as np
from springdrop_helpers import energy_bar, small_label

# "The squeeze stores energy in the spring. Let go, and it becomes the
#  ball's speed."
DUR = 7.3


class SpringdropS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        spring_b = energy_bar("spring stored", 0.95, [-2.4, 0, 0],
                              color="#7FB8E8", max_h=3.0, w=0.8)
        speed_b = energy_bar("speed", 0.05, [2.4, 0, 0],
                             color="#E8C46B", max_h=3.0, w=0.8)
        arr = Arrow([-1.6, 0.2, 0], [1.6, 0.2, 0], color="#8C8576",
                    stroke_width=4, buff=0,
                    max_tip_length_to_length_ratio=0.18)
        arr.set_opacity(0.6)
        self.play(FadeIn(spring_b), run_time=1.2)
        self.play(GrowArrow(arr), FadeIn(speed_b), run_time=1.0)

        # spring empties into speed
        new_spring = energy_bar("spring stored", 0.05, [-2.4, 0, 0],
                                color="#7FB8E8", max_h=3.0, w=0.8)
        new_speed = energy_bar("speed", 0.95, [2.4, 0, 0],
                               color="#E8C46B", max_h=3.0, w=0.8)
        self.play(Transform(spring_b, new_spring),
                  Transform(speed_b, new_speed),
                  run_time=2.4, rate_func=rate_functions.ease_in_sine)
        self.wait(DUR - 4.6)
