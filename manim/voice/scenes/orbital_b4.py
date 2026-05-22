from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             divider, label, make_balance, PLANET, PLANET_D,
                             FAINT, DIM, RED, CHALK)

# "On one side, Newton's pull: big G, the sun's mass, the planet's mass,
#  over r squared. On the other, the turn a circle demands — which grows
#  with speed and shrinks with radius."
DUR = 14.1

LC = np.array([-3.5, 0.6, 0])


class OrbitalS1B4(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.5))

        r0 = 1.7
        self.add(orbit_ring(LC, r=r0))
        planet = make_planet(planet_at(LC, r0, 0.0), color=PLANET,
                             edge=PLANET_D)
        self.add(planet)
        self.add(label("m_p", planet_at(LC, r0, 0.0) + np.array([0.6, 0.1, 0]),
                       size=22, color=PLANET))
        self.add(label("m_s", LC + np.array([0.0, -0.7, 0]),
                       size=22, color=DIM))

        # Build the balance: F_grav = F_centripetal.
        bal = make_balance([3.3, 0.6, 0], scale=0.95)
        bal.set_color(CHALK)
        # left side first (Newton's pull)
        self.play(FadeIn(VGroup(bal.lnum, bal.lbar, bal.ldenom),
                         shift=RIGHT * 0.2), run_time=1.4)
        gl = label("G · m_s · m_p / r²", [3.3, -1.0, 0], size=20, color=DIM)
        self.play(FadeIn(gl), run_time=0.8)
        self.wait(0.4)
        # = and right side (the turn the circle demands)
        self.play(Write(bal.eqsign), run_time=0.5)
        self.play(FadeIn(VGroup(bal.rnum, bal.rbar, bal.rdenom),
                         shift=LEFT * 0.2), run_time=1.4)
        gr = label("grows with speed, shrinks with r", [3.3, -1.8, 0],
                   size=20, color=DIM)
        self.play(FadeOut(gl), FadeIn(gr), run_time=0.8)
        self.wait(0.4)

        # m_p appears on BOTH sides, glowing red (about to cancel).
        self.play(bal.mp_left.animate.set_color(RED),
                  bal.mp_right.animate.set_color(RED), run_time=1.0)
        self.play(Indicate(bal.mp_left, color=RED, scale_factor=1.3),
                  Indicate(bal.mp_right, color=RED, scale_factor=1.3),
                  planet.animate.set_stroke(RED, width=5), run_time=1.0)
        self.wait(max(0.3, DUR - 10.5))
