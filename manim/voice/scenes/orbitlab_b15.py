from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, make_moon, gravity_arrow,
                              straight_arrow, small_label)

# "What launch speed makes the pull and the straight line match — so
#  the trace closes into a circle, not a spiral, not an escape?"
DUR = 10.6


class OrbitlabS1B15(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        blank = small_label("v_launch  =  ?", [0, 2.7, 0],
                            color="#EAE4D5", size=36)
        self.play(FadeIn(blank, shift=UP * 0.15), run_time=1.0)
        self.wait(0.4)

        # a small balance sketch: pull vs straight-line
        c = np.array([0, -0.4, 0])
        planet = make_planet(c, r=0.55)
        mpos = c + np.array([0, 1.5, 0])
        moon = make_moon(mpos, r=0.13)
        self.add(planet, moon)
        ga = gravity_arrow(mpos, c, length=0.85, color="#D98C5F")
        sa = straight_arrow(mpos, [1, 0, 0], length=0.95,
                            color="#E8C46B")
        self.play(GrowArrow(ga), GrowArrow(sa), run_time=1.2)
        bal = small_label("pull  ↔  straight line", [0, -2.4, 0],
                          color="#8C8576", size=24)
        self.play(FadeIn(bal), run_time=0.8)
        self.wait(0.4)
        opts = small_label("circle?   spiral?   escape?", [0, 1.8, 0],
                           color="#5A5446", size=20)
        self.play(FadeIn(opts), run_time=0.8)
        self.wait(DUR - 5.6)
