from manim import *
import numpy as np
from centerofmass_helpers import (make_figure, make_load, com_dot,
                                  ground_line, plumb_line, small_label)

# "And why a person leans into a heavy bag — moving their center of mass
#  back over their feet."
DUR = 8.3

GY = -2.2


class CenterofmassS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        gl = ground_line(y=GY)
        self.add(gl)

        ctr = [-0.4, GY + 1.0, 0]

        # upright + load forward: combined com pushed forward of the feet
        fig0 = make_figure(center=ctr, scale=1.0, lean=0.0)
        load0 = make_load(fig0.hand, scale=1.0)
        feet_x = ctr[0]
        # combined com (body ~ at torso mid, load out front) -> forward
        com_fwd = [ctr[0] + 0.62, GY + 0.95, 0]
        com0 = com_dot(com_fwd, scale=0.8)
        pl0 = plumb_line(com_fwd, GY)

        self.play(FadeIn(fig0), FadeIn(load0), run_time=1.0)
        self.play(Create(com0), Create(pl0), run_time=1.0)
        warn = small_label("ahead of the feet", [ctr[0] + 0.6, GY - 0.55, 0],
                           size=22, color="#C98A4A")
        self.play(FadeIn(warn), run_time=0.7)
        self.wait(0.6)

        # lean back: combined com slides back over the feet
        fig1 = make_figure(center=ctr, scale=1.0, lean=0.40)
        load1 = make_load(fig1.hand, scale=1.0)
        com_over = [feet_x, GY + 0.95, 0]
        com1 = com_dot(com_over, scale=0.8)
        pl1 = plumb_line(com_over, GY)
        ok = small_label("back over the feet", [ctr[0] - 0.1, GY - 0.55, 0],
                         size=22, color="#7FB8E8")

        self.play(
            ReplacementTransform(fig0, fig1),
            ReplacementTransform(load0, load1),
            ReplacementTransform(com0, com1),
            ReplacementTransform(pl0, pl1),
            ReplacementTransform(warn, ok),
            run_time=1.8,
        )
        self.wait(DUR - 6.9)
