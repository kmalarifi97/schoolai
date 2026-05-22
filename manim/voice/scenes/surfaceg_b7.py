from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, divider, label,
                              make_equation_reduced, CHALK, DIM, RED, MOON)

# "What's it for? It tells you the surface gravity of ANY world. Swap in
#  the Moon's mass and radius — you get one-sixth. Mars, Jupiter, a
#  distant moon: same equation, new world."
DUR = 14.0

LC = np.array([-3.5, 0.3, 0])


class SurfacegS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.1, kind="earth")
        elbl = label("Earth", [LC[0], LC[1] - 1.55, 0], size=24, color=DIM)
        self.add(earth, elbl)

        # RIGHT: equation + a g read-out.
        eq = make_equation_reduced([3.3, 1.4, 0], scale=1.2)
        eq.get_part_by_tex("m_E").set_color(RED)
        eq.get_part_by_tex("r_E").set_color(RED)
        self.add(eq)
        gread = MathTex(r"g = 9.8\ \text{m/s}^{2}", color=CHALK).scale(1.0)
        gread.move_to([3.3, -0.4, 0])
        self.add(gread)
        self.wait(0.6)

        # A "knob" swaps Earth -> Moon (m_E, r_E change).
        knob = label("swap the world", [LC[0], LC[1] + 1.8, 0], size=22,
                     color=RED)
        self.play(FadeIn(knob), run_time=0.8)

        moon = make_world(LC, r=0.55, kind="moon")
        mlbl = label("Moon", [LC[0], LC[1] - 1.0, 0], size=24, color=DIM)
        self.play(
            ReplacementTransform(earth, moon),
            ReplacementTransform(elbl, mlbl),
            run_time=1.6)

        # g drops to ~1.6 (one-sixth).
        gmoon = MathTex(r"g = 1.6\ \text{m/s}^{2}", color=RED).scale(1.0)
        gmoon.move_to([3.3, -0.4, 0])
        self.play(ReplacementTransform(gread, gmoon), run_time=1.2)
        sixth = label("about one-sixth", [3.3, -1.3, 0], size=22, color=RED)
        self.play(FadeIn(sixth), run_time=0.8)
        self.wait(0.6)

        # Quick Mars / Jupiter values flash on the RIGHT.
        flashes = VGroup(
            label("Mars: g = 3.7", [3.3, -2.1, 0], size=22, color=DIM),
            label("Jupiter: g = 24.8", [3.3, -2.7, 0], size=22, color=DIM))
        self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.15) for f in flashes],
                              lag_ratio=0.4), run_time=1.6)
        self.wait(max(0.3, DUR - 8.2))
