from manim import *
import numpy as np
from collisionlab_helpers import (clue_dent, clue_slide, clue_sound,
                                  momentum_bar, small_label)

# "She wasn't short of clues. She was short of a conserved quantity —
#  something the crash can't change."
DUR = 8.7


class CollisionlabS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cd = clue_dent([-3.0, 1.2, 0], scale=1.1, crossed=True)
        cs = clue_slide([0.0, 1.2, 0], scale=1.1, crossed=True)
        cn = clue_sound([3.0, 1.2, 0], scale=1.1, crossed=True)
        self.add(cd, cs, cn)
        self.wait(0.6)

        # the clues fade away
        self.play(cd.animate.set_opacity(0.0),
                  cs.animate.set_opacity(0.0),
                  cn.animate.set_opacity(0.0), run_time=1.6)

        # a single steady bar glows in
        bar = momentum_bar([0, -0.2, 0], length=5.0, split=0.5,
                           label=None)
        bar.set_opacity(0.0)
        self.play(bar.animate.set_opacity(1.0), run_time=1.6)
        cap = small_label("unchanged by the hit", [0, -1.3, 0],
                          color="#8C8576", size=22)
        self.play(FadeIn(cap), run_time=1.2)
        self.wait(DUR - 5.6)
