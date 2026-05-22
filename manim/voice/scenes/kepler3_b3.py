from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, divider,
                             label, NEUTRAL, DIM, FAINT, CHALK, RED)

# "It's not chaos. There's a rule — one clean rule, tying every planet's
#  distance to its year. Find it, and one planet can tell you about
#  another. Here's how."
DUR = 12.7

LC = np.array([-3.5, 0.2, 0])


class Kepler3S1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        sun = make_sun(LC, scale=0.6)
        self.add(sun)

        # scattered planets settle into clean ordered orbits
        rng = [(1.0, PI * 0.3, "#C9B07A", 0.10),
               (1.7, PI * 1.1, NEUTRAL, 0.15),
               (2.5, PI * 1.7, "#9BD6B0", 0.16)]
        planets = VGroup()
        for r, ang, col, pr in rng:
            planets.add(make_planet(
                LC + np.array([r * np.cos(ang), r * np.sin(ang), 0]),
                r=pr, color=col))
        self.add(planets)

        # The blank equation frame on the RIGHT pulses once, confidently.
        frame = RoundedRectangle(width=4.6, height=2.6, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.2, 0])
        self.add(frame)
        self.play(frame.animate.set_stroke(RED, width=3), run_time=0.6)
        self.play(frame.animate.set_stroke(FAINT, width=2), run_time=0.8)
        self.wait(0.6)

        # On the LEFT the planets settle into clean ordered circular orbits.
        target_rs = [1.0, 1.9, 2.8]
        rings = VGroup(*[orbit_ring(LC, r=tr) for tr in target_rs])
        anims = []
        for p, tr, (r, ang, col, pr) in zip(planets, target_rs, rng):
            anims.append(p.animate.move_to(
                LC + np.array([tr * np.cos(PI / 2), tr * np.sin(PI / 2), 0])))
        self.play(Create(rings), *anims, run_time=2.4,
                  rate_func=rate_functions.ease_in_out_sine)
        self.wait(DUR - 6.6)
