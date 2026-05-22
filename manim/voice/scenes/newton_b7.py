from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from newton_helpers import (make_coin, double_pull, divider, label,
                            make_equation, MASS1, MASS2, RED, CHALK, DIM)

# "One more piece. A number that sets gravity's overall strength — the same
#  everywhere in the universe. Call it big G. It's tiny, which is why you
#  don't feel two coins pull."
DUR = 13.7


class NewtonS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # Two coins on a table with an almost-invisible pull.
        table = Line([-5.6, -1.4, 0], [-1.0, -1.4, 0], color=DIM,
                     stroke_width=2)
        self.add(table)
        c1 = make_coin([-4.2, -1.2, 0], w=0.6)
        c2 = make_coin([-2.3, -1.2, 0], w=0.6)
        self.play(FadeIn(c1), FadeIn(c2), run_time=0.9)
        faint_pull = double_pull([-4.2, -1.2, 0], [-2.3, -1.2, 0],
                                 0.3, 0.3, color=RED, width=1.0)
        faint_pull.set_opacity(0.25)
        self.play(FadeIn(faint_pull), run_time=0.8)
        coin_note = label("almost nothing", [-3.2, -0.4, 0], size=20,
                          color=DIM)
        self.play(FadeIn(coin_note), run_time=0.7)

        # Equation; G fades in red with a "tiny number" tag.
        eq = make_equation([3.3, 0.6, 0], scale=1.25)
        eq.set_color(DIM)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)
        self.add(eq)
        self.play(eq.G.animate.set_color(RED).scale(1.35), run_time=1.0)
        self.play(eq.G.animate.scale(1 / 1.35), run_time=0.4)

        gtag = label("a tiny number — same everywhere",
                     [3.3, -0.8, 0], size=20, color=RED, opacity=0.9)
        self.play(FadeIn(gtag), run_time=0.9)
        gval = MathTex(r"G \approx 6.7\times 10^{-11}",
                       color=CHALK).scale(0.8).move_to([3.3, -1.7, 0])
        gval.set_color(DIM)
        self.play(Write(gval), run_time=1.6)
        self.wait(max(0.3, DUR - 7.0))
