from manim import *
import numpy as np
from rotke_helpers import (make_flywheel, axis_pin, speed_zero_tag,
                           question_mark, make_hand, spark_burst,
                           rim_element, tangent_speed_arrow, energy_bar,
                           mass_disk, moi_label, make_potters_wheel,
                           make_ball, make_slope, small_label)


class RotkeTest(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        fw = make_flywheel([-4.6, 1.8, 0], radius=1.1)
        self.add(fw, axis_pin([-4.6, 1.8, 0]))
        self.add(speed_zero_tag([-1.6, 2.2, 0]))
        self.add(question_mark([0.6, 2.4, 0]))
        hand = make_hand(0.8).move_to([2.4, 2.0, 0])
        self.add(hand, spark_burst([1.8, 2.0, 0]))

        C = np.array([-4.4, -1.4, 0])
        ring = Circle(radius=1.0, stroke_color="#7FB8E8",
                      stroke_width=2, fill_opacity=0).move_to(C)
        self.add(ring)
        for k in range(6):
            a = TAU * k / 6
            self.add(rim_element(a, C, 1.0))
            self.add(tangent_speed_arrow(a, C, 1.0, length=0.55))

        self.add(energy_bar(2.0, [-1.6, -2.4, 0], label="energy"))
        self.add(mass_disk([1.4, -1.4, 0], radius=0.95, at_rim=False))
        self.add(mass_disk([4.6, -1.4, 0], radius=0.95, at_rim=True))
        self.add(moi_label([2.8, -3.1, 0], size=22))

        self.add(make_potters_wheel([5.0, 2.0, 0], scale=0.8))
        ln, s, e = make_slope(width=3.0, drop=1.2, base_y=-3.2, x0=-1.0)
        self.add(ln, make_ball(s + np.array([0.4, 0.3, 0]), radius=0.3))
        self.add(small_label("test", [0, -3.6, 0], size=20))
        self.wait(0.4)
