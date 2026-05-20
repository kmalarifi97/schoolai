from manim import *
import numpy as np
from skatepark_helpers import make_ramp

# "The clean landing was never the homework. This is: in one sentence,
#  your own words — why did the same ramp give two answers, and which
#  energy did he keep forgetting?"
DUR = 13.4


class SkateparkS1B23(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        r = make_ramp(launch_h=2.5)
        ramp = r["group"].scale(0.85).shift(UP * 0.6)
        self.play(FadeIn(ramp), run_time=1.2)
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
        self.wait(DUR - 8.6)
