from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, divider, label,
                              make_equation_full, CHALK, DIM, RED)

# "Your weight is just Newton's pull — between your mass and the Earth's.
#  Write 'your weight is m-g' on one side, and Newton's pull on the other.
#  They're the same thing."
DUR = 13.5

LC = np.array([-3.5, -0.9, 0])


class SurfacegS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.15, kind="earth")
        person = make_person(scale=1.0)
        person.move_to([LC[0], earth.get_top()[1] + 0.4, 0])
        self.add(earth, person)
        # weight arrow stays as a quiet anchor
        top = person.get_bottom()
        arrow = Arrow(top + UP * 0.05, top + DOWN * 0.95, color=RED,
                      stroke_width=5, buff=0.05,
                      max_tip_length_to_length_ratio=0.3).set_opacity(0.6)
        self.add(arrow)

        # RIGHT: build the equation  m g = G m m_E / r_E^2
        eq = make_equation_full([3.3, 0.5, 0], scale=1.25)
        # show "your weight is m g" first (left side), then "= Newton's pull".
        mg = VGroup(eq[0], eq[1])   # m, g
        wlab = label("your weight", [3.3, 1.7, 0], size=22, color=DIM)
        self.play(FadeIn(wlab), Write(mg), run_time=1.6)
        self.wait(0.6)
        # the equals + Newton's pull
        rest = VGroup(eq[2], eq[3], eq[4])   # =, G, fraction
        plab = label("Newton's pull", [3.3, -1.2, 0], size=22, color=DIM)
        self.play(Write(rest), run_time=1.8)
        self.play(FadeIn(plab), run_time=0.6)
        self.wait(0.6)

        # Your mass m sits on BOTH sides -> glow red together.
        left_m = eq[0]                       # the m in m g
        num_m = eq[4][0]                      # first glyph of the fraction = m
        # the m on the person (left world) also glows
        m_on_you = label("m", [LC[0] + 1.0, person.get_center()[1], 0],
                         size=30, color=RED)
        self.play(
            left_m.animate.set_color(RED),
            num_m.animate.set_color(RED),
            FadeIn(m_on_you, scale=0.7),
            run_time=1.2)
        self.play(
            left_m.animate.scale(1.15),
            num_m.animate.scale(1.15),
            run_time=0.5)
        self.play(
            left_m.animate.scale(1 / 1.15),
            num_m.animate.scale(1 / 1.15),
            run_time=0.5)
        self.wait(max(0.3, DUR - 9.3))
