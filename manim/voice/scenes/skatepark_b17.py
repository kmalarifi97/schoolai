from manim import *
import numpy as np
from skatepark_helpers import small_label

# "How fast at the bottom. How high on the far side. Worked out from
#  the energy — start height, minus what friction takes."
DUR = 10.1


class SkateparkS1B17(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        q1 = small_label("v at bottom  =  ?", [0, 1.7, 0],
                         color="#EAE4D5", size=34)
        q2 = small_label("h on far side  =  ?", [0, 0.6, 0],
                         color="#EAE4D5", size=34)
        self.play(FadeIn(q1, shift=UP * 0.15), run_time=1.0)
        self.play(FadeIn(q2, shift=UP * 0.15), run_time=1.0)
        self.wait(0.6)

        # the relation sketch, numbers left open
        rel = small_label("PE  −  heat  →  KE", [0, -1.4, 0],
                          color="#7FB8E8", size=32)
        box = SurroundingRectangle(rel, color="#5A5446", buff=0.35,
                                   corner_radius=0.1).set_opacity(0.5)
        self.play(Write(rel), run_time=1.4)
        self.play(Create(box), run_time=1.0)
        self.wait(DUR - 5.0)
