from manim import *
import numpy as np
from thermolaws_helpers import (stone_tablet, tablet_inscribe,
                                tablet_arrow, small_label)

# "Computing an engine's maximum possible efficiency from its hot and
#  cold operating temperatures — that's yours."
# visual: two tablets side by side, clean and final, an open question
# beneath. "[Hold 3s in silence]" is a directive — NOT rendered text.
# We honor it by adding ~3s of held still frame after the action.
BEAT = 7.9          # spoken-beat portion
HOLD = 3.0          # the directed silent hold
DUR = BEAT + HOLD   # total scene run time


class ThermolawsS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        t1 = stone_tablet([-3.0, 0.4, 0], scale=1.0, faint=False)
        t2 = stone_tablet([3.0, 0.4, 0], scale=1.0, faint=False)
        ins1 = tablet_inscribe(t1, "energy is\nconserved", "I")
        roman2 = small_label("II", t2.get_center() + np.array([0, 0.85, 0]),
                             size=46, color="#5C5750")
        arr2 = tablet_arrow(t2)
        self.play(FadeIn(t1), FadeIn(t2), run_time=1.4)
        self.play(Write(ins1), FadeIn(roman2), GrowArrow(arr2),
                  run_time=1.8)
        self.wait(0.6)
        # the open question, handed back to the student
        q = small_label("maximum efficiency from  T_hot , T_cold  =  ?",
                        [0, -2.7, 0], size=30, color="#EAE4D5")
        self.play(Write(q), run_time=1.8)
        # settle to the clean, final still
        self.wait(BEAT - 5.6)
        # honor "[Hold 3s in silence]" — final frame held, no new motion
        self.wait(HOLD)
