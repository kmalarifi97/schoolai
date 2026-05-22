from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_earth
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             divider, label, make_equation_full, PLANET,
                             PLANET_D, DIM, RED, CHALK)

# "T equals two-pi times the square root of r cubed, over G times the
#  sun's mass. Hand it an orbit's size and the sun's mass, and it predicts
#  the year — for any planet, any satellite, any exoplanet you'll never
#  visit."
DUR = 16.9

LC = np.array([-3.5, 1.2, 0])


class OrbitalS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.45))
        self.add(orbit_ring(LC, r=1.2))
        self.add(make_planet(planet_at(LC, 1.2, 0.0), r=0.15, color=PLANET,
                             edge=PLANET_D))

        # The equation completes, assembled cleanly.
        eq = make_equation_full([3.3, 1.4, 0], scale=1.3)
        eq.set_color(CHALK)
        self.play(Write(eq.T), Write(eq.eqsign), run_time=0.8)
        self.play(FadeIn(eq.coeff, scale=0.7), run_time=0.7)
        self.play(Write(eq.rad), run_time=1.4)
        self.wait(0.3)
        box = SurroundingRectangle(eq, color=RED, buff=0.25,
                                   corner_radius=0.1)
        self.play(Create(box), run_time=0.5)
        self.play(FadeOut(box), run_time=0.5)

        # Quick examples on the LEFT, each with a predicted period.
        # 1. a satellite around Earth
        earth = make_earth([-5.0, -1.3, 0]).scale(0.6)
        sat_ring = orbit_ring([-5.0, -1.3, 0], r=0.7, color=DIM, width=1.5)
        sat = Dot([-5.0, -0.6, 0], radius=0.06, color=CHALK)
        s1 = VGroup(earth, sat_ring, sat)
        v1 = MathTex(r"T \approx 90\ \text{min}", color=CHALK
                     ).scale(0.6).move_to([-2.6, -0.7, 0])
        self.play(FadeIn(s1), FadeIn(v1), run_time=1.4)

        # 2. an exoplanet around a distant star
        star = make_sun([-5.0, -3.0, 0], scale=0.3)
        exo_ring = orbit_ring([-5.0, -3.0, 0], r=0.9, color=DIM, width=1.5)
        exo = Dot([-5.0, -2.1, 0], radius=0.07, color="#BCA6E0")
        s2 = VGroup(star, exo_ring, exo)
        v2 = MathTex(r"T \approx 400\ \text{days}", color=CHALK
                     ).scale(0.6).move_to([-2.6, -2.7, 0])
        self.play(FadeIn(s2), FadeIn(v2), run_time=1.4)

        pred = label("predicts the year — anywhere", [3.3, -1.4, 0],
                     size=22, color=DIM)
        self.play(FadeIn(pred), run_time=1.0)
        self.wait(max(0.3, DUR - 9.4))
