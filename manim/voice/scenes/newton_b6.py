from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, divider, label, make_equation,
                            MASS1, MASS1_D, RED, CHALK, DIM)

# "Why so fast? The pull spreads out over a sphere — and a sphere grows
#  with the square of its radius. Double the distance, and the pull drops
#  to a quarter."
DUR = 12.5

C = np.array([-3.6, 0.4, 0])


class NewtonS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1 = make_mass(C, r=0.32, color=MASS1, edge=MASS1_D)
        self.add(m1)

        # Rays emanating from the mass.
        n_rays = 14
        rays = VGroup()
        for k in range(n_rays):
            ang = TAU * k / n_rays
            d = np.array([np.cos(ang), np.sin(ang), 0])
            rays.add(Line(C + d * 0.32, C + d * 2.6, color=DIM,
                          stroke_width=2.5))
        self.play(LaggedStart(*[Create(r) for r in rays],
                              lag_ratio=0.03), run_time=1.4)

        # An expanding sphere (circle, projected) — rays thin over its
        # growing surface.
        sph_r = ValueTracker(0.9)
        sphere = always_redraw(lambda: Circle(
            radius=sph_r.get_value(), stroke_color=CHALK,
            stroke_width=2.5, fill_opacity=0.05, fill_color=CHALK
            ).move_to(C))
        self.add(sphere)

        # Equation; r gains a ^2 in red.
        eq = make_equation([3.3, 0.9, 0], scale=1.2)
        eq.set_color(DIM)
        eq.m1.set_color(MASS1)
        self.add(eq)
        # the r^2 (the squared radius) pulses red
        self.play(eq.rsq.animate.set_color(RED).scale(1.3), run_time=0.9)
        self.play(eq.rsq.animate.scale(1 / 1.3), run_time=0.4)

        # Sphere doubles in radius -> surface 4x, pull 1/4.
        self.play(sph_r.animate.set_value(1.8), run_time=2.2,
                  rate_func=rate_functions.ease_in_out_sine)

        # Numerically: ×2 distance -> ¼ force.
        calc = MathTex(r"\times 2\ r", r"\;\Rightarrow\;",
                       r"\tfrac{1}{4}\,F", color=CHALK).scale(0.9)
        calc.move_to([3.3, -1.4, 0])
        calc[0].set_color(RED); calc[2].set_color(RED)
        self.play(Write(calc), run_time=1.4)
        self.wait(max(0.3, DUR - 8.6))
