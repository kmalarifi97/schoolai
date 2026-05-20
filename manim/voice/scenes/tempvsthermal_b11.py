from manim import *
import numpy as np
from tempvsthermal_helpers import small_label

# "Temperature is the per-particle average. Thermal energy is the grand
#  total. Intensity versus amount."
DUR = 8.7


class TempvsthermalS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        divider = DashedLine([0, -3.2, 0], [0, 3.2, 0],
                             color="#5A6E80", stroke_width=2).set_opacity(0.5)
        self.play(Create(divider), run_time=0.8)

        # LEFT panel: a single fast particle = temperature
        title_l = small_label("temperature", [-3.4, 2.7, 0], size=28,
                              color="#FF7A3C")
        sub_l = small_label("per-particle average", [-3.4, 2.1, 0],
                            size=20, color="#8C98A6")
        part = Dot([-3.4, -0.2, 0], radius=0.22, color="#FF7A3C")
        self.play(FadeIn(title_l), FadeIn(sub_l), FadeIn(part, scale=0.5),
                  run_time=1.0)

        # RIGHT panel: a vast summed bar = thermal energy
        title_r = small_label("thermal energy", [3.4, 2.7, 0], size=28,
                              color="#E5A23C")
        sub_r = small_label("the grand total", [3.4, 2.1, 0],
                            size=20, color="#8C98A6")
        bar = Rectangle(width=1.3, height=0.05, fill_color="#E5A23C",
                        fill_opacity=0.92, stroke_width=0)
        bar.move_to([3.4, -2.4, 0], aligned_edge=DOWN)
        self.add(bar)
        bar_full = Rectangle(width=1.3, height=4.0, fill_color="#E5A23C",
                             fill_opacity=0.92, stroke_width=0)
        bar_full.move_to([3.4, -2.4, 0], aligned_edge=DOWN)
        self.play(FadeIn(title_r), FadeIn(sub_r),
                  Transform(bar, bar_full), run_time=1.4)

        self.play(part.animate.shift(RIGHT * 0.18), run_time=0.5,
                  rate_func=rate_functions.there_and_back)
        self.add(small_label("intensity   versus   amount", [0, -3.6, 0],
                             size=24, color="#EAE4D5"))
        self.wait(DUR - 4.7)
