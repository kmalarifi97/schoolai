from manim import *
import numpy as np
from impulse_helpers import (make_car, momentum_bar, small_label,
                             big_label)

# "The motion that had to be killed was identical. So what made the
#  difference?"
DUR = 7.0


class ImpulseS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        car1 = make_car(crumple=True, scale=0.5).move_to([-3.4, 1.7, 0])
        car2 = make_car(crumple=False, scale=0.5).move_to([-3.4, -1.7, 0])
        self.add(car1, car2)

        bar1 = momentum_bar(1.0, length=3.0, height=0.46,
                            label="motion", show_label=False)
        bar1.next_to(car1, RIGHT, buff=0.6)
        bar2 = momentum_bar(1.0, length=3.0, height=0.46,
                            label="motion", show_label=False)
        bar2.next_to(car2, RIGHT, buff=0.6)
        self.play(GrowFromEdge(bar1, LEFT), GrowFromEdge(bar2, LEFT),
                  run_time=1.3)

        eq = small_label("same amount to stop",
                         [1.6, 0, 0], color="#8C98A6", size=26)
        self.play(FadeIn(eq), run_time=0.9)
        self.wait(0.5)

        q = big_label("?", [1.6, -0.05, 0], color="#EAE4D5", size=72)
        self.play(FadeOut(eq, run_time=0.5),
                  FadeIn(q, scale=0.5, run_time=0.9))
        self.wait(DUR - 4.1)
