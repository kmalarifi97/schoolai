from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from surfaceg_helpers import (make_world, make_person, radius_line, divider,
                              label, make_equation_reduced,
                              CHALK, DIM, RED)

# "No codes. g, the pull per kilogram. m-Earth, the world's mass. r-Earth,
#  its radius. The square, again the sphere. Read it — that's why you
#  weigh what you weigh."
DUR = 13.0

LC = np.array([-3.5, -0.5, 0])


class SurfacegS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        earth = make_world(LC, r=1.2, kind="earth")
        person = make_person(scale=0.85)
        person.move_to([LC[0], earth.get_top()[1] + 0.32, 0])
        rline = radius_line(earth, angle=-PI / 4, color=CHALK, width=4)
        self.add(earth, person, rline)

        eq = make_equation_reduced([3.3, 0.4, 0], scale=1.4)
        self.add(eq)
        self.wait(0.6)

        g_sym = eq[0]
        G_sym = eq[2]
        mE = eq.get_part_by_tex("m_E")
        rE = eq.get_part_by_tex("r_E")

        # g — pull per kilogram (g + weight arrow pulse).
        top = person.get_bottom()
        warrow = Arrow(top + UP * 0.05, top + DOWN * 0.7, color=RED,
                       stroke_width=5, buff=0.05,
                       max_tip_length_to_length_ratio=0.3)
        self.play(g_sym.animate.set_color(RED), GrowArrow(warrow),
                  run_time=1.0)
        self.play(g_sym.animate.set_color(CHALK),
                  warrow.animate.set_opacity(0.4), run_time=0.6)

        # m_E — world's mass (Earth body + m_E pulse).
        self.play(mE.animate.set_color(RED),
                  earth.body.animate.set_stroke(RED, width=5),
                  run_time=1.0)
        self.play(earth.body.animate.set_stroke("#1A4885", width=2.5),
                  run_time=0.6)

        # r_E — its radius (radius line + r_E pulse).
        self.play(rE.animate.set_color(RED),
                  rline.animate.set_stroke(RED, width=6), run_time=1.0)
        self.play(rline.animate.set_stroke(CHALK, width=4), run_time=0.6)

        # The square — again the sphere (the ^2 exponent glyph).
        sq = eq[3][5]
        self.play(sq.animate.set_color(RED).scale(1.5), run_time=0.8)
        sqnote = label("the square — the sphere", [3.3, -1.6, 0],
                       size=22, color=DIM)
        self.play(FadeIn(sqnote), run_time=0.8)

        # restore reds for a held, fully color-bound final.
        self.play(g_sym.animate.set_color(RED), run_time=0.6)
        self.wait(max(0.4, DUR - 9.0))
