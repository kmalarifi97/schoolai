from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, divider,
                             label, make_equation, PLANET_A, PLANET_AD,
                             PLANET_B, PLANET_BD, CHALK, DIM, FAINT)

# "That's what Kepler did, poring over Brahe's measurements. He wrote down
#  r and T for planet after planet — and went hunting for the rule."
DUR = 11.3


class Kepler3S1B7(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        # LEFT: the two mini-systems, dimmed.
        TopC = np.array([-3.5, 1.5, 0]); BotC = np.array([-3.5, -1.6, 0])
        left = VGroup(
            make_sun(TopC, scale=0.35), orbit_ring(TopC, r=1.3),
            make_planet(TopC + np.array([0, 1.3, 0]), r=0.16,
                        color=PLANET_A, edge=PLANET_AD),
            make_sun(BotC, scale=0.35), orbit_ring(BotC, r=1.0),
            make_planet(BotC + np.array([0, 1.0, 0]), r=0.14,
                        color=PLANET_B, edge=PLANET_BD))
        self.add(left)
        self.play(left.animate.set_opacity(0.4), run_time=0.8)

        # RIGHT: a handwritten-style table fills with r and T columns.
        head = VGroup(
            label("planet", [2.0, 1.7, 0], size=24, color=DIM),
            label("r", [3.4, 1.7, 0], size=26, color=CHALK),
            label("T", [4.6, 1.7, 0], size=26, color=CHALK))
        rows = [("Mercury", "0.39", "0.24"),
                ("Earth",   "1.00", "1.00"),
                ("Mars",    "1.52", "1.88"),
                ("Jupiter", "5.20", "11.9")]
        line = Line([1.4, 1.45, 0], [5.1, 1.45, 0],
                    color=FAINT, stroke_width=1.5)
        self.play(FadeIn(head), Create(line), run_time=1.0)
        row_groups = []
        for k, (nm, rv, tv) in enumerate(rows):
            y = 1.0 - k * 0.62
            g = VGroup(
                label(nm, [2.0, y, 0], size=22, color=CHALK),
                label(rv, [3.4, y, 0], size=22, color=CHALK),
                label(tv, [4.6, y, 0], size=22, color=CHALK))
            row_groups.append(g)
        self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.15)
                                for g in row_groups],
                              lag_ratio=0.4), run_time=DUR - 4.5)
        self.wait(0.5)
