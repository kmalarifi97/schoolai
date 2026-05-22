from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_earth
from newton_helpers import (make_mass, divider, label, make_equation,
                            MASS1, MASS2, RED, CHALK, DIM)

# "What's it for? Hand it any two masses and a distance, and it gives you
#  the exact pull between them — an apple and the Earth, the Earth and the
#  Moon, two galaxies. Not the shape of the path, not why mass bends space
#  — just how strong."
DUR = 18.3


class NewtonS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # Equation small at the top of the RIGHT half.
        eq = make_equation([3.3, 2.5, 0], scale=0.95)
        eq.set_color(CHALK)
        eq.m1.set_color(MASS1); eq.m2.set_color(MASS2)
        self.add(eq)

        # Three quick examples on the LEFT, each with a computed force value.
        rows = []

        # 1. apple + Earth
        apple = Circle(radius=0.12, fill_color="#C0392B", fill_opacity=1,
                       stroke_color="#7B241C", stroke_width=2
                       ).move_to([-5.0, 1.7, 0])
        earth = make_earth([-3.9, 1.7, 0]).scale(0.6)
        v1 = MathTex(r"F \approx 1\ \text{N}", color=CHALK
                     ).scale(0.7).move_to([-1.9, 1.7, 0])
        rows.append(VGroup(apple, earth, v1))

        # 2. Earth + Moon
        earth2 = make_earth([-5.0, 0.0, 0]).scale(0.55)
        moon = Circle(radius=0.14, fill_color="#9A9A9A", fill_opacity=1,
                      stroke_color="#5A5A5A", stroke_width=2
                      ).move_to([-3.9, 0.0, 0])
        v2 = MathTex(r"F \approx 2{\times}10^{20}\ \text{N}", color=CHALK
                     ).scale(0.7).move_to([-1.6, 0.0, 0])
        rows.append(VGroup(earth2, moon, v2))

        # 3. two galaxies
        g1 = VGroup(*[Dot([-5.0 + 0.18 * np.cos(a), -1.7 + 0.18 * np.sin(a), 0],
                          radius=0.03, color="#BCA6E0") for a in
                      np.linspace(0, TAU, 9)])
        g1.add(Dot([-5.0, -1.7, 0], radius=0.06, color=WHITE))
        g2 = VGroup(*[Dot([-3.9 + 0.18 * np.cos(a), -1.7 + 0.18 * np.sin(a), 0],
                          radius=0.03, color="#9AC0E0") for a in
                      np.linspace(0, TAU, 9)])
        g2.add(Dot([-3.9, -1.7, 0], radius=0.06, color=WHITE))
        v3 = MathTex(r"F \approx 10^{30}\ \text{N}", color=CHALK
                     ).scale(0.7).move_to([-1.8, -1.7, 0])
        rows.append(VGroup(g1, g2, v3))

        for r in rows:
            self.play(FadeIn(r), run_time=1.3)
            self.wait(0.3)

        # Struck-through tags on the RIGHT: "path shape", "why".
        def struck(text, pos):
            t = label(text, pos, size=22, color=DIM)
            ln = Line(t.get_left() + LEFT * 0.05, t.get_right() + RIGHT * 0.05,
                      color=RED, stroke_width=3)
            return VGroup(t, ln)
        s1 = struck("not the path's shape", [3.3, 0.5, 0])
        s2 = struck("not why space bends", [3.3, -0.4, 0])
        just = label("— just how strong", [3.3, -1.5, 0], size=24,
                     color=CHALK)
        self.play(FadeIn(s1), run_time=1.0)
        self.play(FadeIn(s2), run_time=1.0)
        self.play(FadeIn(just), run_time=1.0)
        self.wait(max(0.3, DUR - 12.5))
