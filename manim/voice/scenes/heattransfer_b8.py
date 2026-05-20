from manim import *
import numpy as np
from heattransfer_helpers import (make_sun_void, make_earth, glow_path,
                                  small_label)

# "But step into sunlight. The Sun's heat crossed a hundred million
#  miles of empty space. No metal. No fluid. Nothing to carry it."
DUR = 10.6


class HeattransferS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        sun = make_sun_void([-5.4, 0.4, 0], scale=1.15)
        earth = make_earth([5.3, -0.2, 0], scale=0.85)
        self.play(FadeIn(sun), run_time=1.2)
        self.play(FadeIn(earth), run_time=1.0)
        self.wait(0.6)

        gp = glow_path([-4.4, 0.4, 0], [4.95, -0.2, 0])
        self.play(FadeIn(gp), run_time=1.2)

        void = small_label("empty space — nothing to carry it",
                           [0, -2.6, 0], color="#7E8A96", size=24)
        self.play(FadeIn(void), run_time=1.2)
        self.wait(DUR - 6.2)
