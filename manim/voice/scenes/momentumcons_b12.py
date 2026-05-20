from manim import *
import numpy as np
from momentumcons_helpers import label, PLUS_COL, MINUS_COL

# "Setting total momentum before equal to total momentum after, and
#  solving for an unknown velocity in a collision or recoil — that's
#  yours."
DUR = 12.4


class MomentumconsS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        before_t = label("before", (-3.4, 2.4, 0), color="#8C98A6",
                          size=26)
        after_t = label("after", (3.4, 2.4, 0), color="#8C98A6",
                         size=26)

        # one fixed total bar on each side, equal length
        tb = Rectangle(width=3.0, height=0.5, fill_color="#EAD58C",
                       fill_opacity=0.9, stroke_color="#EAD58C",
                       stroke_width=2).move_to([-3.4, 1.2, 0])
        ta = Rectangle(width=3.0, height=0.5, fill_color="#EAD58C",
                       fill_opacity=0.9, stroke_color="#EAD58C",
                       stroke_width=2).move_to([3.4, 1.2, 0])
        eq = Text("=", font="sans", font_size=52, color="#EAE4D5"
                  ).move_to([0, 1.2, 0])
        self.play(FadeIn(before_t), FadeIn(after_t), run_time=0.8)
        self.play(GrowFromEdge(tb, LEFT), GrowFromEdge(ta, LEFT),
                  run_time=1.1)
        self.play(FadeIn(eq), run_time=0.8)

        # the AFTER split left open: one part known, one a question
        known = Rectangle(width=1.7, height=0.42, fill_color=PLUS_COL,
                          fill_opacity=0.9, stroke_width=2,
                          stroke_color=PLUS_COL)
        known.move_to([3.4 - 1.5 + 0.85, -0.4, 0])
        unknown = DashedVMobject(
            Rectangle(width=1.3, height=0.42, stroke_color=MINUS_COL,
                      stroke_width=2.5, fill_opacity=0), num_dashes=20)
        unknown.next_to(known, RIGHT, buff=0)
        qm = Text("?", font="sans", font_size=40, color=MINUS_COL
                  ).move_to(unknown.get_center())
        self.play(GrowFromEdge(known, LEFT), run_time=0.9)
        self.play(Create(unknown), FadeIn(qm), run_time=1.0)
        self.add(label("solve for v", (3.4, -1.5, 0), color="#8C98A6",
                       size=24))

        yours = label("that's yours", (0, -2.7, 0), color="#EAE4D5",
                      size=30)
        self.play(FadeIn(yours), run_time=1.0)
        # holds — hand the thinking back to the student
        self.wait(DUR - 6.6)
