from manim import *
import numpy as np
from impulse_helpers import (make_car, crumple_car, make_wall,
                             momentum_bar, small_label)

# "Now the crash makes sense. Same momentum to remove. The crumple zone
#  stretches the stopping time —"
DUR = 8.6


class ImpulseS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall(height=3.4, x=4.4)
        self.add(wall)

        car = make_car(crumple=True, scale=0.62).move_to([-3.0, 1.4, 0])
        self.add(car)

        bar = momentum_bar(1.0, length=3.4, height=0.42,
                           label="momentum to remove",
                           show_label=False).move_to([-1.2, -1.0, 0])
        self.play(GrowFromEdge(bar, LEFT), run_time=1.0)
        cap = small_label("same momentum to remove",
                          [-1.2, -1.7, 0], color="#8C98A6", size=22)
        self.play(FadeIn(cap), run_time=0.6)

        # slow contact + long crumple
        self.play(car.animate.shift(RIGHT * (4.4 - car.get_right()[0])),
                  run_time=1.6, rate_func=rate_functions.linear)
        crushed = crumple_car(car, amount=0.62)
        self.play(Transform(car, crushed), run_time=2.0,
                  rate_func=rate_functions.ease_out_sine)

        # long stopping-time bracket
        br = BraceBetweenPoints([1.0, 2.4, 0], [4.4, 2.4, 0],
                                direction=UP, color="#8C98A6")
        t = small_label("long stopping time", [2.7, 3.0, 0],
                        color="#EAE4D5", size=24)
        self.play(GrowFromCenter(br), FadeIn(t), run_time=1.0)
        self.wait(DUR - 6.2)
