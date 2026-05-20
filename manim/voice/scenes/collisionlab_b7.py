from manim import *
import numpy as np
from collisionlab_helpers import (make_noura, clue_dent, clue_slide,
                                  clue_sound)

# "Every clue lies on its own. The dent, the slide, the noise — none of
#  them, alone, gives her the speed."  (held beat)
DUR = 8.8


class CollisionlabS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        cd = clue_dent([-3.0, 1.0, 0], scale=1.2)
        cs = clue_slide([0.0, 1.0, 0], scale=1.2)
        cn = clue_sound([3.0, 1.0, 0], scale=1.2)
        self.play(FadeIn(cd), run_time=0.7)
        self.play(FadeIn(cs), run_time=0.7)
        self.play(FadeIn(cn), run_time=0.7)

        # each one earns a small ✗, one at a time
        cd2 = clue_dent([-3.0, 1.0, 0], scale=1.2, crossed=True)
        cs2 = clue_slide([0.0, 1.0, 0], scale=1.2, crossed=True)
        cn2 = clue_sound([3.0, 1.0, 0], scale=1.2, crossed=True)
        self.play(Transform(cd, cd2), run_time=0.6)
        self.play(Transform(cs, cs2), run_time=0.6)
        self.play(Transform(cn, cn2), run_time=0.6)

        # Noura sitting, stuck
        no = make_noura([0, -1.7, 0], scale=0.9, facing=1)
        self.play(FadeIn(no), run_time=1.0)
        # a held, quiet beat — she just sits with it
        self.wait(DUR - 6.1)
