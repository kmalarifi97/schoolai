from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             radius_line, make_clock, clock_wedge, clock_hand,
                             divider, label, make_equation, PLANET, PLANET_D,
                             DIM, RED, CHALK)

# "Here, T is the planet's year. r, the size of its orbit. m-sun, the mass
#  it circles. And G again, gravity's constant."
DUR = 9.9

LC = np.array([-3.3, 0.7, 0])


class OrbitalS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        sun = make_sun(LC, scale=0.5)
        self.add(sun)

        r0 = 1.6
        ring = orbit_ring(LC, r=r0)
        rline = radius_line(LC, PI / 2, r0, color=CHALK, width=4)
        planet = make_planet(planet_at(LC, r0, 0.0), color=PLANET,
                             edge=PLANET_D)
        clk = make_clock([-4.4, -2.4, 0], r=0.5)
        wedge = clock_wedge(clk, 0.45, color=CHALK)
        hand = clock_hand(clk, 0.45)
        self.add(ring, rline, planet, clk, wedge, hand)

        eq = make_equation([3.3, 0.5, 0], scale=1.15)
        eq.set_color(CHALK)
        self.add(eq)
        self.wait(0.5)

        # T + clock glow red together.
        new_wedge = clock_wedge(clk, 0.45, color=RED)
        self.play(eq.T.animate.set_color(RED).scale(1.3),
                  Transform(wedge, new_wedge), run_time=1.0)
        self.play(eq.T.animate.scale(1 / 1.3), run_time=0.4)
        self.wait(0.2)

        # r + orbit ring + radius line glow red together.
        self.play(eq.rcube.animate.set_color(RED),
                  rline.animate.set_stroke(RED, width=6),
                  ring.animate.set_stroke(RED, opacity=0.9), run_time=1.0)
        self.wait(0.2)

        # m_s + sun glow red together.
        self.play(eq.ms.animate.set_color(RED),
                  Flash(LC, color="#FFD27F", line_length=0.3,
                        flash_radius=0.7), run_time=1.0)
        self.wait(0.2)

        # G pulses red.
        self.play(eq.G.animate.set_color(RED).scale(1.3), run_time=0.8)
        self.play(eq.G.animate.scale(1 / 1.3), run_time=0.4)
        self.wait(max(0.3, DUR - 7.5))
