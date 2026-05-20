from manim import *
import numpy as np
from collisionlab_helpers import momentum_bar, small_label

# "Mass times velocity, added up for both carts. Before the hit and
#  after — that total stays the same. Always."
DUR = 9.2


class CollisionlabS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        L = 5.2

        before = momentum_bar([0, 1.1, 0], length=L, split=0.62,
                              label=None)
        bl = small_label("before", [-3.6, 1.1, 0], color="#8C8576",
                         size=22)
        self.play(FadeIn(before), FadeIn(bl), run_time=1.2)
        defn = small_label("m × v,  both carts", [0, 2.1, 0],
                           color="#EAE4D5", size=22)
        self.play(FadeIn(defn), run_time=1.0)

        # the impact flash between before and after
        flash = Dot([0, 0.0, 0], radius=0.07, color="#EAE4D5")
        self.play(flash.animate.scale(8).set_opacity(0.0),
                  run_time=0.8)

        # after: split point shifts (carts swapped speed) but the bar is
        # the SAME total length — conserved.
        after = momentum_bar([0, -1.1, 0], length=L, split=0.30,
                             label=None)
        al = small_label("after", [-3.6, -1.1, 0], color="#8C8576",
                         size=22)
        self.play(TransformFromCopy(before[0], after[0]),
                  FadeIn(al), run_time=1.6)

        # a faint guide showing the two ends line up exactly
        g1 = DashedLine([-L / 2, 1.1, 0], [-L / 2, -1.1, 0],
                        color="#7FB8E8", stroke_width=2,
                        dash_length=0.1).set_opacity(0.5)
        g2 = DashedLine([L / 2, 1.1, 0], [L / 2, -1.1, 0],
                        color="#7FB8E8", stroke_width=2,
                        dash_length=0.1).set_opacity(0.5)
        eq = small_label("same total. always.", [0, -2.2, 0],
                         color="#7FB8E8", size=22)
        self.play(Create(g1), Create(g2), FadeIn(eq), run_time=1.4)
        self.wait(DUR - 7.4)
