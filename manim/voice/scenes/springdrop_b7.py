from manim import *
import numpy as np
from springdrop_helpers import (make_spring, ledger, small_label)

# "He wasn't short of presses. He was short of an account — where the
#  squeeze goes, and what it has to become."
DUR = 9.2


class SpringdropS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # the presses fade away
        presses = VGroup()
        for k in range(5):
            sp = make_spring([-4.6 + k * 0.2, -1.0, 0], height=1.0,
                             compress=0.2 + 0.1 * k)
            presses.add(sp["group"])
        presses.set_opacity(0.4)
        self.play(FadeIn(presses), run_time=1.2)
        self.wait(0.6)
        self.play(FadeOut(presses), run_time=1.6)

        led = ledger([0.4, 0.0, 0], rows=4, w=4.2, scale=1.0)
        self.play(FadeIn(led, shift=UP * 0.1), run_time=1.6)
        cap = small_label("where the squeeze goes",
                          [0.4, 2.0, 0], size=24, color="#8C8576")
        self.play(FadeIn(cap), run_time=1.0)
        self.wait(DUR - 6.0)
