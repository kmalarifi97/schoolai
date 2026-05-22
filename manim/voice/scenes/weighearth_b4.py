from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from weighearth_helpers import (make_earth, divider, label,
                                make_equation_g, make_equation_mE,
                                CHALK, DIM, RED)

# "Multiply across, and the Earth's mass stands alone: it equals g, times
#  the radius squared, divided by big G."
DUR = 9.3

LC = np.array([-3.5, 0.0, 0])


class WeighearthS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_earth(LC, r=1.2)
        earth.body.set_stroke(RED, width=5)
        self.add(earth)

        # Start from g = G m_E / r_E^2 (m_E red, carried from b3).
        eqg = make_equation_g([3.3, 0.8, 0], scale=1.3)
        eqg.get_part_by_tex("m_E").set_color(RED)
        self.add(eqg)
        self.wait(0.6)

        # "Multiply across" — a hint label.
        mult = label("multiply across", [3.3, 1.9, 0], size=22, color=DIM)
        self.play(FadeIn(mult), run_time=0.8)

        # Rearrange to m_E = g r_E^2 / G (clean crossfade to the new form).
        eqm = make_equation_mE([3.3, -0.4, 0], scale=1.4)
        eqm.get_part_by_tex("m_E").set_color(RED)
        arrow = Arrow([3.3, 0.2, 0], [3.3, -0.05, 0], color=RED,
                      stroke_width=4, buff=0.05,
                      max_tip_length_to_length_ratio=0.4)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.play(FadeOut(eqg, shift=UP * 0.2),
                  FadeIn(eqm, shift=UP * 0.2), run_time=1.4)
        self.wait(0.4)

        # The isolated m_E pulses red — it stands alone.
        mE = eqm.get_part_by_tex("m_E")
        box = SurroundingRectangle(mE, color=RED, buff=0.1, corner_radius=0.08)
        self.play(Create(box), run_time=0.8)
        alone = label("the Earth's mass, alone", [3.3, -2.0, 0], size=21,
                      color=RED)
        self.play(FadeIn(alone), run_time=0.8)
        self.wait(max(0.3, DUR - 5.6))
