from manim import *
import numpy as np
from tempvsthermal_helpers import energy_bar, small_label

# "Add up all that jiggling and the tub holds an ocean of energy. That
#  total is thermal energy."
DUR = 8.1


class TempvsthermalS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # many tiny per-particle bars on the left, merging into one huge bar
        rng = np.random.default_rng(10)
        tiny = VGroup()
        cols, rows = 14, 5
        for c in range(cols):
            for r in range(rows):
                h = rng.uniform(0.10, 0.26)
                b = Rectangle(width=0.10, height=h, fill_color="#8FB8D8",
                              fill_opacity=0.9, stroke_width=0)
                b.move_to([-5.4 + c * 0.16, -1.6 + r * 0.45, 0],
                          aligned_edge=DOWN)
                tiny.add(b)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in tiny],
                              lag_ratio=0.004, run_time=2.0))
        self.add(small_label("add up every particle's jiggle",
                             [-3.4, 2.4, 0], size=22, color="#8FB8D8"))

        # match's tiny bar for contrast
        match_bar = energy_bar(0.45, [1.6, -1.6, 0], width=0.5,
                               color="#FF7A3C", label="match")
        self.play(GrowFromEdge(match_bar[0], DOWN), FadeIn(match_bar[1]),
                  run_time=0.8)

        # the tub's huge summed bar
        big = Rectangle(width=1.1, height=0.05, fill_color="#E5A23C",
                        fill_opacity=0.92, stroke_width=0)
        big.move_to([4.2, -1.6, 0], aligned_edge=DOWN)
        self.add(big)
        big_full = Rectangle(width=1.1, height=4.3, fill_color="#E5A23C",
                             fill_opacity=0.92, stroke_width=0)
        big_full.move_to([4.2, -1.6, 0], aligned_edge=DOWN)
        self.play(Transform(big, big_full),
                  tiny.animate.set_opacity(0.30), run_time=1.6)
        self.add(small_label("thermal energy = total", [4.2, 3.1, 0],
                             size=24, color="#E5A23C"))
        self.wait(DUR - 6.2)
