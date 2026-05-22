from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label,
                            make_equation, MASS1, MASS1_D, MASS2, MASS2_D,
                            RED, CHALK, DIM)

# "Put it together. Force equals big G, times the two masses multiplied,
#  divided by the distance squared. Newton's law of universal gravitation."
DUR = 11.7

P1 = np.array([-4.2, 0.4, 0])
P2 = np.array([-1.6, 0.0, 0])


class NewtonS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1 = make_mass(P1, r=0.45, color=MASS1, edge=MASS1_D)
        m2 = make_mass(P2, r=0.28, color=MASS2, edge=MASS2_D)
        self.add(m1, m2, double_pull(P1, P2, 0.45, 0.28, color=RED, width=6))

        eq = make_equation([3.3, 0.4, 0], scale=1.35)
        eq.set_color(CHALK)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)

        # Build piece by piece: F, then =, then G, then numerator, bar, r^2.
        self.play(Write(eq.F), run_time=0.7)
        self.play(Write(eq.eqsign), run_time=0.5)
        self.play(FadeIn(eq.G, scale=0.7), run_time=0.7)
        self.play(FadeIn(eq.num, shift=DOWN * 0.2), run_time=0.9)
        self.play(Create(eq.bar), run_time=0.5)
        self.play(FadeIn(eq.rsq, shift=UP * 0.2), run_time=0.7)
        self.wait(0.3)

        # The full equation flashes once.
        box = SurroundingRectangle(eq, color=RED, buff=0.28,
                                   corner_radius=0.1)
        self.play(Create(box), run_time=0.5)
        self.play(FadeOut(box), run_time=0.5)

        name = label("Newton's law of universal gravitation",
                     [3.3, -1.6, 0], size=22, color=DIM)
        self.play(FadeIn(name), run_time=1.0)
        self.wait(max(0.3, DUR - 7.5))
