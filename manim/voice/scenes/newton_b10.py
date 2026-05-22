from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d, make_sun as grav_sun
from newton_helpers import (make_mass, pull_arrow, label, make_equation,
                            MASS1, MASS1_D, MASS2, MASS2_D, RED, CHALK, DIM)

# "Remember the bend. A steeper bend means a stronger pull — and this
#  equation is exactly how steep. The curve, written as a force."
DUR = 10.7


class NewtonS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The teaser's bend, full frame; depth is a live knob.
        dip = ValueTracker(1.4)
        fabric = always_redraw(
            lambda: make_fabric_3d(dip_amount=dip.get_value()))
        self.add(fabric)
        self.play(Create(make_fabric_3d(dip_amount=1.4)), run_time=0.01)
        self.wait(0.2)

        center = np.array([0, -0.35, 0])
        # A mass on the slope; pull-arrow strength tracks the dip depth.
        ball = make_mass(center + np.array([2.2, 0.2, 0]), r=0.22,
                         color=MASS2, edge=MASS2_D)
        self.add(ball)

        def arrow():
            w = 3 + 6 * dip.get_value()
            start = center + np.array([2.2, 0.2, 0])
            end = center + np.array([0.9, -0.1, 0])
            return pull_arrow(start, end, color=RED, width=float(w))
        self.add(always_redraw(arrow))

        # Equation slides over the bend, top-center.
        eq = make_equation([0, 2.6, 0], scale=1.0)
        eq.set_color(CHALK)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)
        self.play(FadeIn(eq, shift=DOWN * 0.3), run_time=1.2)

        steep = label("steeper bend = stronger pull", [0, -3.2, 0],
                      size=22, color=DIM)
        self.play(FadeIn(steep), run_time=0.8)

        # Steepen the well -> arrow grows; shallow it -> weaker.
        self.play(dip.animate.set_value(2.0), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)
        self.play(dip.animate.set_value(0.6), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(max(0.3, DUR - 9.0))
