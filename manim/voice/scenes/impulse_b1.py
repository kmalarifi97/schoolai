from manim import *
import numpy as np
from impulse_helpers import make_car, crumple_car, make_wall

# "Two cars hit a wall at the same speed. One crumples slowly. One
#  stops instantly."
DUR = 7.3


class ImpulseS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall(height=4.2, x=4.6)
        self.add(wall)

        car_c = make_car(crumple=True, scale=0.62).move_to([-5.4, 1.5, 0])
        car_r = make_car(crumple=False, scale=0.62).move_to([-5.4, -1.5, 0])
        self.play(FadeIn(car_c), FadeIn(car_r), run_time=1.0)
        self.wait(0.4)

        # both reach the wall at the same speed
        nose_x = 4.6
        self.play(
            car_c.animate.shift(RIGHT * (nose_x - car_c.get_right()[0])),
            car_r.animate.shift(RIGHT * (nose_x - car_r.get_right()[0])),
            run_time=1.8, rate_func=rate_functions.linear,
        )
        # crumple car deforms slowly; rigid car just halts (already there)
        crushed = crumple_car(car_c, amount=0.6)
        self.play(Transform(car_c, crushed), run_time=1.4,
                  rate_func=rate_functions.ease_out_sine)
        self.wait(DUR - 4.6)
