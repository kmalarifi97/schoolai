from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label,
                            make_equation, MASS1, MASS1_D, MASS2, MASS2_D,
                            RED, CHALK, DIM)

# "Then the distance between them. Call it r. Move them apart, and the pull
#  weakens. But not gently — it drops off fast."
DUR = 9.9

CY = 0.3


class NewtonS1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # m1 fixed at left; m2 slides away. Distance r between centers.
        x1 = -4.4
        gap = ValueTracker(2.0)
        m1 = make_mass([x1, CY, 0], r=0.42, color=MASS1, edge=MASS1_D)
        self.add(m1)
        m2 = always_redraw(lambda: make_mass(
            [x1 + gap.get_value(), CY, 0], r=0.28,
            color=MASS2, edge=MASS2_D))
        self.add(m2)

        # Pull arrows; strength ~ 1/r^2 so it drops off fast.
        def arrow():
            g = gap.get_value()
            w = 9 * (2.0 / g) ** 2
            return double_pull([x1, CY, 0], [x1 + g, CY, 0], 0.42, 0.28,
                               color=RED, width=float(np.clip(w, 1.5, 12)))
        self.add(always_redraw(arrow))

        # The r measurement line (dim), and an r label.
        def rline():
            g = gap.get_value()
            return DashedLine([x1 + 0.42, CY - 0.9, 0],
                              [x1 + g - 0.28, CY - 0.9, 0],
                              color=DIM, stroke_width=2)
        self.add(always_redraw(rline))
        rlab = always_redraw(lambda: label(
            "r", [x1 + gap.get_value() / 2, CY - 1.3, 0], size=28, color=RED))
        self.add(rlab)

        # Equation; r (the r^2 slot) glows red.
        eq = make_equation([3.3, 0.4, 0], scale=1.25)
        eq.set_color(DIM)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)
        self.add(eq)
        self.play(eq.rsq.animate.set_color(RED), run_time=1.0)

        # Move them apart — pull weakens fast.
        self.play(gap.animate.set_value(4.6), run_time=2.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.4)
        self.play(gap.animate.set_value(2.4), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(max(0.3, DUR - 7.0))
