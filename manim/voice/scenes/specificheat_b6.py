from manim import *
import numpy as np
from specificheat_helpers import gram_cube, Thermometer, label, INK

# "That stubbornness — how much energy one gram needs to warm by one degree —
#  is the specific heat."
DUR = 8.1


class SpecificheatS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        defn = label("specific heat", [0, 2.5, 0], size=46, color=INK)
        sub = label("energy to raise 1 g by 1°", [0, 1.6, 0], size=28,
                    color="#9AA0A6")
        cube = gram_cube([-2.4, -0.8, 0], side=0.9)
        gl = label("1 g", [-2.4, -1.9, 0], size=24)
        th = Thermometer([1.6, -0.6, 0], height=2.4, level=0.30)
        td = label("+1°", [1.6, -2.2, 0], size=24)
        self.play(Write(defn), run_time=1.2)
        self.play(FadeIn(sub), run_time=0.9)
        self.play(FadeIn(cube), FadeIn(gl), FadeIn(th), FadeIn(td),
                  run_time=1.0)
        glow = Square(1.4, stroke_width=0, fill_color="#E2533B",
                      fill_opacity=0.0).move_to(cube.get_center())
        self.add(glow)
        self.play(
            glow.animate.set_fill(opacity=0.35),
            UpdateFromAlphaFunc(th, lambda m, a: m.set_level(0.30 + 0.18 * a)),
            run_time=1.4)
        self.wait(DUR - 4.5)
