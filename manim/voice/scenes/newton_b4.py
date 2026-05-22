from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label,
                            make_equation, MASS1, MASS1_D, MASS2, MASS2_D,
                            RED, CHALK, DIM)

# "First, the masses. Call them m-one and m-two. More mass, more pull.
#  Double either one, and the force doubles."
DUR = 9.3

P1 = np.array([-4.2, 0.3, 0])
P2 = np.array([-1.4, 0.0, 0])


class NewtonS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1_r = ValueTracker(0.40)
        m2_r = ValueTracker(0.28)
        m1 = always_redraw(lambda: make_mass(
            P1, r=m1_r.get_value(), color=MASS1, edge=MASS1_D))
        m2 = always_redraw(lambda: make_mass(
            P2, r=m2_r.get_value(), color=MASS2, edge=MASS2_D))
        self.add(m1, m2)
        lab1 = label("m₁", P1 + np.array([0, 1.0, 0]), size=26, color=MASS1)
        lab2 = label("m₂", P2 + np.array([0, 0.8, 0]), size=26, color=MASS2)
        self.add(lab1, lab2)

        # Pull arrow whose width tracks the product of the masses.
        def arrow():
            strength = (m1_r.get_value() / 0.40) * (m2_r.get_value() / 0.28)
            w = 4 + 7 * (strength - 1)
            return double_pull(P1, P2, m1_r.get_value(), m2_r.get_value(),
                               color=RED, width=max(3, w))
        self.add(always_redraw(arrow))

        # Equation, m_1 and m_2 glow red.
        eq = make_equation([3.3, 0.4, 0], scale=1.25)
        eq.set_color(DIM)
        self.add(eq)
        self.play(eq.m1.animate.set_color(RED),
                  eq.m2.animate.set_color(RED), run_time=1.0)

        # Knob: grow m_1 -> thicker pull; shrink it -> thinner. Linear.
        self.play(m1_r.animate.set_value(0.62), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.3)
        self.play(m1_r.animate.set_value(0.28), run_time=1.6,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.2)
        self.play(m1_r.animate.set_value(0.40), run_time=1.0,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(max(0.3, DUR - 7.5))
