from manim import *
import numpy as np
from impulse_helpers import (make_car, crumple_car, make_wall,
                             make_driver, small_label)

# "Same speed in. Same dead stop. One driver walks away. One does not."
DUR = 6.3


class ImpulseS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        wall = make_wall(height=4.2, x=4.6)
        self.add(wall)

        # both already stopped against the wall
        car_c = crumple_car(make_car(crumple=True, scale=0.62), amount=0.6)
        car_c.move_to([0, 1.5, 0])
        car_c.shift(RIGHT * (4.6 - car_c.get_right()[0]))
        car_r = make_car(crumple=False, scale=0.62).move_to([0, -1.5, 0])
        car_r.shift(RIGHT * (4.6 - car_r.get_right()[0]))
        self.add(car_c, car_r)
        self.wait(0.6)

        # crumple driver walks away (stands, moves left)
        drv_ok = make_driver(scale=0.62).move_to(
            car_c.get_left() + np.array([-0.5, 0.25, 0]))
        self.play(FadeIn(drv_ok, shift=UP * 0.2), run_time=0.9)
        self.play(drv_ok.animate.shift(LEFT * 1.6), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)

        # rigid driver does not — a slumped marker
        x = small_label("×", car_r.get_top() + np.array([0, 0.5, 0]),
                        color="#C96A5A", size=44)
        self.play(FadeIn(x, scale=0.6), run_time=0.8)
        self.wait(DUR - 4.9)
