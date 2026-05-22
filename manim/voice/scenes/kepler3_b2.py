from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, divider,
                             qmark, label, NEUTRAL, DIM, FAINT, CHALK)

# "Is that just chaos — every planet doing its own thing? Or is a planet's
#  distance quietly setting how long its year is? There's only one way to
#  find out. Measure."
DUR = 13.1

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # Scattered planets, a question mark over them.
        sun = make_sun(LC, scale=0.6)
        self.add(sun)
        scatter = VGroup()
        rng = [(1.0, PI * 0.3, "#C9B07A", 0.10),
               (1.7, PI * 1.1, NEUTRAL, 0.15),
               (2.5, PI * 1.7, "#9BD6B0", 0.16)]
        for r, ang, col, pr in rng:
            scatter.add(make_planet(
                LC + np.array([r * np.cos(ang), r * np.sin(ang), 0]),
                r=pr, color=col))
        self.play(FadeIn(scatter), run_time=1.0)
        q = qmark(LC + np.array([0.2, 1.9, 0]), size=70)
        self.play(FadeIn(q, shift=DOWN * 0.2), run_time=1.0)
        self.wait(1.5)

        # The frame splits: planets already on the left; reveal divider.
        self.play(Create(divider()), run_time=0.8)

        # A blank equation frame fades in on the RIGHT — empty slots.
        frame = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.2, 0])
        slots = VGroup()
        for x in [-1.1, 0.0, 1.1]:
            slots.add(DashedVMobject(
                RoundedRectangle(width=0.8, height=0.8, corner_radius=0.1),
                num_dashes=14).set_stroke(DIM, width=1.5, opacity=0.6
                ).move_to([3.3 + x, 0.2, 0]))
        self.play(Create(frame), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(s) for s in slots],
                              lag_ratio=0.3), run_time=1.4)
        cap = label("a rule will go here", [3.3, -1.45, 0], size=22,
                    color=DIM, opacity=0.85)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(DUR - 8.3)
