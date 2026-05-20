from manim import *
import numpy as np
from orbitlab_helpers import (make_planet, make_moon, gravity_arrow,
                              straight_arrow, small_label)

# "He wasn't short of tries. He was short of the balance underneath —
#  fall against fling."
DUR = 7.7


class OrbitlabS1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        c = np.array([0, 0, 0])
        planet = make_planet(c, r=0.85)
        self.add(planet)
        mpos = c + np.array([2.4, 0, 0])
        moon = make_moon(mpos, r=0.16)
        self.play(FadeIn(moon), run_time=0.8)

        ga = gravity_arrow(mpos, c, length=1.0, color="#D98C5F")
        sa = straight_arrow(mpos, [0, 1, 0], length=1.05,
                            color="#E8C46B")
        self.play(GrowArrow(ga), run_time=1.0)
        lf = small_label("fall", ga.get_end() + np.array([-0.5, -0.1, 0]),
                         color="#D98C5F", size=22)
        self.play(FadeIn(lf), run_time=0.5)
        self.play(GrowArrow(sa), run_time=1.0)
        ls = small_label("fling", sa.get_end() + np.array([0.55, 0, 0]),
                         color="#E8C46B", size=22)
        self.play(FadeIn(ls), run_time=0.5)
        self.wait(DUR - 4.8)
