from manim import *
import numpy as np
from weightless_helpers import (make_earth, make_station, orbit_circle,
                                small_label)

# "That explanation is wrong. At the space station's height, Earth's
#  gravity is almost as strong as it is on the ground."
DUR = 10.0


class WeightlessS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        C = np.array([0, -1.6, 0])
        earth = make_earth(C).scale(4.4)
        self.play(FadeIn(earth), run_time=1.0)

        R_surf = 1.67  # ~ earth visual radius (0.38*4.4)
        R_orb = R_surf + 0.85   # station orbit drawn CLOSE to surface
        orbit = orbit_circle(C, R_orb, dashed=True)
        self.play(Create(orbit), run_time=1.4)

        station = make_station(C + np.array([0, R_orb, 0]), scale=0.42)
        self.play(FadeIn(station), run_time=0.8)

        # surface gravity arrow
        surf_pt = C + np.array([-1.05, R_surf, 0])
        a_surf = Arrow(surf_pt, surf_pt + np.array([0, -1.5, 0]),
                       color="#7FB8E8", stroke_width=5, buff=0,
                       max_tip_length_to_length_ratio=0.22)
        # gravity arrow at station height — nearly as long
        sta_pt = C + np.array([1.05, R_orb, 0])
        a_sta = Arrow(sta_pt, sta_pt + np.array([0, -1.35, 0]),
                      color="#7FB8E8", stroke_width=5, buff=0,
                      max_tip_length_to_length_ratio=0.22)
        self.play(GrowArrow(a_surf), run_time=0.9)
        self.play(GrowArrow(a_sta), run_time=0.9)
        self.add(small_label("surface", surf_pt + np.array([-0.95, -0.7, 0]),
                             size=20),
                 small_label("station", sta_pt + np.array([1.0, -0.6, 0]),
                             size=20))
        self.wait(DUR - 6.9)
