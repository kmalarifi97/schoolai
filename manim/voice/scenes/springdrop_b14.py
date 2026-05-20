from manim import *
import numpy as np
from springdrop_helpers import (compression_control, small_label,
                                qmark)

# "How far must he compress it so the stored energy becomes exactly the
#  height of the bell — for this ball's mass?"
DUR = 9.5


class SpringdropS1B14(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cc = compression_control([0, 1.4, 0], frac=0.4, w=3.4)
        blank = Text("compression  x = ?", font="sans", font_size=30,
                     color="#EAE4D5").move_to([0, 2.6, 0])
        self.play(FadeIn(blank), run_time=1.0)
        self.play(FadeIn(cc), run_time=1.0)

        rel = MathTex(r"\tfrac{1}{2}kx^{2}\;=\;m\,g\,h",
                      color="#EAE4D5").scale(1.3).move_to([0, -0.4, 0])
        self.play(Write(rel), run_time=1.8)
        q1 = qmark([-2.0, -1.8, 0], size=40)
        q2 = qmark([2.0, -1.8, 0], size=40)
        cap = small_label("numbers open — for this ball's mass",
                          [0, -2.7, 0], size=22, color="#8C8576")
        self.play(FadeIn(q1), FadeIn(q2), FadeIn(cap), run_time=1.0)
        self.wait(DUR - 5.8)
