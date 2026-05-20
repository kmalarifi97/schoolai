from manim import *
import numpy as np
from thermalbudget_helpers import efc_layout, small_label

# "The melt-on-time was never the homework. This is: in one sentence,
#  your own words — where did the energy go while the thermometer stood
#  still?"
DUR = 11.7


class ThermalbudgetS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the setup holds, still
        efc = efc_layout([0, 0.7, 0], scale=0.75, heat=0.4,
                         melt=0.3, chunks=False)
        self.play(FadeIn(efc), run_time=1.2)
        self.wait(1.2)

        q = small_label(
            "where did the energy go while the thermometer stood "
            "still?", [0, -1.4, 0], color="#8C8576", size=22)
        self.play(Write(q), run_time=1.8)

        # an empty line waits for the student's sentence
        line = Line([-3.6, -2.6, 0], [3.6, -2.6, 0],
                    color="#5A5446", stroke_width=3).set_opacity(0.7)
        self.play(Create(line), run_time=1.2)
        cursor = Line([-3.6, -2.50, 0], [-3.6, -2.74, 0],
                      color="#EAE4D5", stroke_width=3)
        self.add(cursor)
        for _ in range(2):
            self.play(cursor.animate.set_opacity(0.0), run_time=0.6)
            self.play(cursor.animate.set_opacity(1.0), run_time=0.6)
        self.wait(DUR - 8.6)
