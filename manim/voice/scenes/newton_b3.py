from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_mass, double_pull, divider, label,
                            MASS1, MASS1_D, MASS2, MASS2_D, FAINT, DIM, CHALK)

# "It's not a mystery. The pull depends on just two things: how much mass,
#  and how far apart. That's the whole story."
DUR = 9.7

P1 = np.array([-4.4, 0.3, 0])
P2 = np.array([-1.6, -0.2, 0])


class NewtonS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        m1 = make_mass(P1, r=0.45, color=MASS1, edge=MASS1_D)
        m2 = make_mass(P2, r=0.28, color=MASS2, edge=MASS2_D)
        arr = double_pull(P1, P2, 0.45, 0.28, color=DIM, width=4)
        self.add(m1, m2, arr)

        # RIGHT: reveal two clean slots labeled "mass" and "distance".
        frame = RoundedRectangle(width=4.8, height=3.0, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.2, 0])
        self.play(Create(frame), run_time=0.9)

        slot1 = DashedVMobject(
            RoundedRectangle(width=1.5, height=1.0, corner_radius=0.12),
            num_dashes=18).set_stroke(DIM, width=1.8, opacity=0.7
            ).move_to([2.4, 0.7, 0])
        slot2 = DashedVMobject(
            RoundedRectangle(width=1.5, height=1.0, corner_radius=0.12),
            num_dashes=18).set_stroke(DIM, width=1.8, opacity=0.7
            ).move_to([4.2, 0.7, 0])
        l1 = label("mass", [2.4, -0.3, 0], size=24, color=CHALK)
        l2 = label("distance", [4.2, -0.3, 0], size=24, color=CHALK)
        self.play(FadeIn(slot1), FadeIn(l1), run_time=1.0)
        self.play(FadeIn(slot2), FadeIn(l2), run_time=1.0)
        cap = label("just two things", [3.3, -1.6, 0], size=22,
                    color=DIM, opacity=0.85)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(max(0.3, DUR - 4.5))
