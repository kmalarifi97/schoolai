from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label,
                            make_equation, MASS1, MASS1_D, MASS2, MASS2_D,
                            RED, CHALK, DIM)

# "No more weird codes. m-one and m-two, the two masses. r, how far apart.
#  G, gravity's universal strength. The square, the spreading over a
#  sphere. Read it — that's the pull between anything and anything."
DUR = 16.0

P1 = np.array([-4.2, 0.6, 0])
P2 = np.array([-1.5, 0.2, 0])


class NewtonS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1 = make_mass(P1, r=0.45, color=MASS1, edge=MASS1_D)
        m2 = make_mass(P2, r=0.28, color=MASS2, edge=MASS2_D)
        arr = double_pull(P1, P2, 0.45, 0.28, color=CHALK, width=5)
        self.add(m1, m2, arr)
        rline = DashedLine([P1[0] + 0.45, -1.0, 0], [P2[0] - 0.28, -1.0, 0],
                           color=DIM, stroke_width=2)
        rlab = label("r", [(P1[0] + P2[0]) / 2, -1.4, 0], size=26, color=DIM)
        self.add(rline, rlab)

        eq = make_equation([3.3, 0.4, 0], scale=1.4)
        eq.set_color(CHALK)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)
        self.add(eq)
        self.wait(0.8)

        # m_1 + blue mass pulse together.
        self.play(eq.m1.animate.scale(1.3).set_color(RED),
                  m1.animate.set_stroke(RED, width=6),
                  Flash(P1, color=MASS1, line_length=0.2), run_time=1.0)
        self.play(eq.m1.animate.scale(1 / 1.3).set_color(MASS1),
                  m1.animate.set_stroke(MASS1_D, width=2.5), run_time=0.5)

        # m_2 + amber mass pulse together.
        self.play(eq.m2.animate.scale(1.3).set_color(RED),
                  m2.animate.set_stroke(RED, width=6),
                  Flash(P2, color=MASS2, line_length=0.2), run_time=1.0)
        self.play(eq.m2.animate.scale(1 / 1.3).set_color(MASS2),
                  m2.animate.set_stroke(MASS2_D, width=2.5), run_time=0.5)

        # r + distance line pulse together.
        self.play(eq.rsq.animate.scale(1.3).set_color(RED),
                  rline.animate.set_stroke(RED, width=4),
                  rlab.animate.set_color(RED), run_time=1.0)
        self.play(eq.rsq.animate.scale(1 / 1.3).set_color(CHALK),
                  rline.animate.set_stroke(DIM, width=2),
                  rlab.animate.set_color(DIM), run_time=0.5)

        # G + the whole pull pulse together.
        self.play(eq.G.animate.scale(1.3).set_color(RED),
                  arr.animate.set_color(RED), run_time=1.0)
        self.play(eq.G.animate.scale(1 / 1.3).set_color(CHALK),
                  arr.animate.set_color(CHALK), run_time=0.5)

        read = label("the pull between anything and anything",
                     [3.3, -1.9, 0], size=20, color=DIM)
        self.play(FadeIn(read), run_time=1.0)
        self.wait(max(0.4, DUR - 9.7))
