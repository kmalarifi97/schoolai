from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label, qmark,
                            MASS1, MASS1_D, MASS2, MASS2_D, FAINT, DIM, CHALK)

# "So what sets the strength of the pull? If we knew, we could predict the
#  force between any two things in the universe."
DUR = 9.9

P1 = np.array([-4.4, 0.3, 0])
P2 = np.array([-1.6, -0.2, 0])


class NewtonS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1 = make_mass(P1, r=0.45, color=MASS1, edge=MASS1_D)
        m2 = make_mass(P2, r=0.28, color=MASS2, edge=MASS2_D)
        arr = double_pull(P1, P2, 0.45, 0.28, color=DIM, width=4)
        self.add(m1, m2, arr)
        self.wait(0.4)

        # A question mark over the two masses.
        q = qmark([-3.0, 1.7, 0], size=72)
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=1.0)

        # RIGHT: blank equation frame with a faint '?' in the value slot.
        frame = RoundedRectangle(width=4.6, height=2.4, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.4, 0])
        self.play(Create(frame), run_time=0.9)
        f_eq = MathTex(r"F", r"=", r"?", color=CHALK).scale(1.5)
        f_eq.move_to([3.3, 0.4, 0])
        f_eq[2].set_color(DIM)
        self.play(Write(f_eq[0]), Write(f_eq[1]), run_time=0.9)
        self.play(FadeIn(f_eq[2], scale=1.3), run_time=0.8)
        cap = label("predict any pull", [3.3, -1.2, 0], size=22,
                    color=DIM, opacity=0.85)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(max(0.3, DUR - 5.6))
