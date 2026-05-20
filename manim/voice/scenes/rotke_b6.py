from manim import *
import numpy as np
from rotke_helpers import (axis_pin, rim_element, tangent_speed_arrow,
                           energy_bar, small_label)

# "Each tiny piece has its own motion energy. Add them all up, and the
#  wheel as a whole holds plenty."
DUR = 8.6


class RotkeS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([-2.6, -0.1, 0])
        R = 1.9
        ring = Circle(radius=R, stroke_color="#7FB8E8", stroke_width=2.5,
                      fill_opacity=0).move_to(C)
        self.add(ring, axis_pin(C, scale=1.1))

        n = 8
        elems = VGroup(*[rim_element(TAU * k / n, C, R) for k in range(n)])
        arrows = VGroup(*[tangent_speed_arrow(TAU * k / n, C, R,
                                              length=0.62)
                          for k in range(n)])
        self.play(LaggedStart(*[FadeIn(e) for e in elems],
                              lag_ratio=0.05, run_time=0.9))
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows],
                              lag_ratio=0.05, run_time=1.2))
        self.add(small_label("each piece: its own motion energy",
                             C + np.array([0, -R - 0.55, 0]),
                             size=22, color="#8C98A6"))

        # sum into one glowing energy bar
        base = np.array([3.0, -2.4, 0])
        bar = energy_bar(0.02, base, width=0.62, label="total energy")
        self.add(bar)
        target = energy_bar(2.7, base, width=0.62, label="total energy")
        self.play(Transform(bar, target), run_time=1.6)
        self.wait(DUR - 5.7)
