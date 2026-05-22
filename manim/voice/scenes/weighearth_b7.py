from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_sun, make_planet, make_cavendish,
                                divider, label, make_equation_mE,
                                CHALK, DIM, RED, STEEL)

# "And it doesn't stop at Earth. The same trick weighs the sun, the
#  planets, anything you can orbit or stand near. Cavendish measured a
#  thread in a room — and held a planet on a number."
DUR = 14.6


class WeighearthS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # RIGHT: the m_E equation, generalized to "any mass M".
        eq = make_equation_mE([3.3, 1.8, 0], scale=1.1)
        eq.get_part_by_tex("m_E").set_color(RED)
        self.add(eq)
        general = label("works for any world", [3.3, 0.7, 0], size=22,
                        color=DIM)
        self.play(FadeIn(general), run_time=0.8)

        # LEFT: the sun and planets each get a computed mass.
        sun = make_sun([-4.4, 1.3, 0], scale=0.7)
        self.play(FadeIn(sun), run_time=0.8)
        smass = label("M_sun = 2×10^30 kg", [-3.0, 1.3, 0], size=20,
                      color=RED)
        self.play(FadeIn(smass), run_time=0.8)
        self.wait(0.4)

        planets = VGroup(
            make_planet([-4.6, -0.2, 0], r=0.18, color="#C97B4A"),
            make_planet([-3.9, -0.2, 0], r=0.22, color="#C9A24B"),
            make_planet([-3.2, -0.2, 0], r=0.16, color="#7FA8E8"))
        pmass = label("each: a mass on a number", [-3.0, -0.7, 0], size=20,
                      color=RED)
        self.play(LaggedStart(*[FadeIn(p, scale=0.7) for p in planets],
                              lag_ratio=0.3), run_time=1.2)
        self.play(FadeIn(pmass), run_time=0.8)
        self.wait(0.4)

        # A nod to the Cavendish torsion apparatus.
        cav = make_cavendish([-3.5, -2.3, 0], scale=0.65)
        self.play(FadeIn(cav), run_time=1.0)
        cnote = label("a thread in a room — a planet on a number",
                      [-3.3, -3.4, 0], size=17, color=DIM)
        self.play(FadeIn(cnote), run_time=0.8)
        self.wait(max(0.3, DUR - 8.6))
