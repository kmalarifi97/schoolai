from manim import *
import numpy as np
from collisionlab_helpers import make_cart, table_line

# "The argument was never the homework. This is: in one sentence, your
#  own words — which clue lied, and which rule never did?"
DUR = 10.3


class CollisionlabS1B21(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tbl = table_line(-1.0)
        c1 = make_cart([-1.0, -0.55, 0], scale=0.95, color="#7FB8E8",
                       facing=1)
        c2 = make_cart([1.0, -0.55, 0], scale=0.95, color="#E8C46B",
                       dented=True, facing=-1)
        self.play(FadeIn(c1), FadeIn(c2), run_time=1.2)
        # the two carts hold, still

        # an empty line waits for the student's sentence
        line = Line([-3.4, 1.0, 0], [3.4, 1.0, 0], color="#5A5446",
                    stroke_width=2).set_opacity(0.0)
        self.play(line.animate.set_opacity(0.6), run_time=1.4)

        # a slow caret blink at the start of the line, then silence
        caret = Line([-3.3, 0.95, 0], [-3.3, 1.25, 0],
                     color="#EAE4D5", stroke_width=3)
        self.play(FadeIn(caret), run_time=0.6)
        for _ in range(2):
            self.play(caret.animate.set_opacity(0.1), run_time=0.6)
            self.play(caret.animate.set_opacity(0.9), run_time=0.6)
        # let it rest — silence is the point
        self.wait(DUR - 6.0)
