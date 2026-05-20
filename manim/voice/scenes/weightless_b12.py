from manim import *
import numpy as np
from weightless_helpers import (make_earth, orbit_circle, point_on_circle,
                                small_label)

# "Falling, with nothing to push back. How fast must you go to keep
#  missing the ground? Set falling equal to curving — and solve."
# visual: clean labeled circle, speed left as open symbol 'v = ?'
DUR = 10.2


class WeightlessS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, 0, 0])
        earth = make_earth(C).scale(3.0)
        R = 2.5
        orbit = orbit_circle(C, R, color="#7FB8E8", width=3)
        self.play(FadeIn(earth), Create(orbit), run_time=1.8)

        # orbiting point
        th = PI / 2
        p = point_on_circle(C, R, th)
        dot = Dot(p, radius=0.11, color="#E8C97F")

        # velocity tangent (open symbol) and gravity (inward)
        v_arr = Arrow(p, p + np.array([1.5, 0, 0]), color="#E8C97F",
                      stroke_width=5, buff=0,
                      max_tip_length_to_length_ratio=0.24)
        g_arr = Arrow(p, p + (C - p) / np.linalg.norm(C - p) * 1.2,
                      color="#7FB8E8", stroke_width=5, buff=0,
                      max_tip_length_to_length_ratio=0.26)
        self.play(FadeIn(dot), GrowArrow(v_arr), GrowArrow(g_arr),
                  run_time=1.4)

        vq = Text("v = ?", font="sans", font_size=44, color="#EAE4D5",
                  weight=BOLD).move_to(p + np.array([1.7, 0.55, 0]))
        self.play(Write(vq), run_time=1.2)
        self.add(small_label("falling  =  curving",
                             C + np.array([0, -R - 0.9, 0]),
                             color="#EAE4D5", size=26))
        self.wait(DUR - 4.4)
