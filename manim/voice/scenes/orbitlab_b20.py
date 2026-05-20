from manim import *
import numpy as np
from orbitlab_helpers import make_planet, closed_circle_path

# "The closed circle was never the homework. This is: in one sentence,
#  your own words — why does staying in orbit mean falling forever
#  without landing?"
DUR = 12.2


class OrbitlabS1B20(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0.7, 0])
        planet = make_planet(c, r=0.6)
        circ = closed_circle_path(c, r=1.6, color="#9BD6B0", width=4)
        self.play(FadeIn(planet), Create(circ), run_time=1.6)
        self.wait(1.0)
        # an empty line waits for the student's own sentence
        line = Line([-3.6, -2.4, 0], [3.6, -2.4, 0],
                    color="#5A5446", stroke_width=3).set_opacity(0.7)
        self.play(Create(line), run_time=1.4)
        # a slow blinking cursor — silence is content
        cursor = Line([-3.6, -2.30, 0], [-3.6, -2.55, 0],
                      color="#EAE4D5", stroke_width=3)
        self.add(cursor)
        for _ in range(3):
            self.play(cursor.animate.set_opacity(0.0), run_time=0.6)
            self.play(cursor.animate.set_opacity(1.0), run_time=0.6)
        self.wait(DUR - 7.6)
