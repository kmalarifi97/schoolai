from manim import *
import numpy as np
from springdrop_helpers import callback_bow, small_label

# "And if this felt familiar — it should. Do you remember the drawn bow
#  that didn't move, holding energy in its bend?"
DUR = 9.7


class SpringdropS1B21(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.wait(1.2)
        bow = callback_bow([0, 0.1, 0], scale=1.9, opacity=0.0)
        self.play(bow.animate.set_opacity(0.9), run_time=1.6)
        cap = small_label("elastic PE — energy in the bend",
                          [0, -2.4, 0], size=22, color="#8C8576")
        self.play(FadeIn(cap), run_time=1.0)
        # it holds, still — energy stored, nothing moving
        self.wait(DUR - 5.8)
        self.play(bow.animate.set_opacity(0.0),
                  cap.animate.set_opacity(0.0), run_time=1.0)
