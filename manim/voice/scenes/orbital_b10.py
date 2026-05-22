from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             radius_line, make_clock, clock_wedge, clock_hand,
                             divider, label, make_equation, PLANET, PLANET_D,
                             DIM, RED, CHALK)

# "No codes. T, the year. r, the orbit's size. m-sun, what it circles. G,
#  gravity's constant. The cube and the root — distance ruling time. Read
#  it: the law that times the heavens."
DUR = 14.2

LC = np.array([-3.3, 0.7, 0])


class OrbitalS1B10(Scene):
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

        eq = make_equation([3.3, 0.5, 0], scale=1.3)
        eq.set_color(CHALK)
        self.add(eq)
        self.wait(0.8)

        # T + clock pulse together.
        new_wedge = clock_wedge(clk, 0.45, color=RED)
        self.play(eq.T.animate.scale(1.3).set_color(RED),
                  Transform(wedge, new_wedge), run_time=1.0)
        self.play(eq.T.animate.scale(1 / 1.3).set_color(CHALK), run_time=0.4)

        # r + orbit pulse together.
        self.play(eq.rcube.animate.set_color(RED),
                  rline.animate.set_stroke(RED, width=6),
                  ring.animate.set_stroke(RED, opacity=0.9), run_time=1.0)
        self.play(eq.rcube.animate.set_color(CHALK),
                  rline.animate.set_stroke(CHALK, width=4),
                  ring.animate.set_stroke(DIM, opacity=0.5), run_time=0.4)

        # m_s + sun pulse together.
        self.play(eq.ms.animate.set_color(RED),
                  Flash(LC, color="#FFD27F", line_length=0.3,
                        flash_radius=0.7), run_time=1.0)
        self.play(eq.ms.animate.set_color(CHALK), run_time=0.4)

        # G pulses.
        self.play(eq.G.animate.scale(1.3).set_color(RED), run_time=0.8)
        self.play(eq.G.animate.scale(1 / 1.3).set_color(CHALK), run_time=0.4)

        read = label("the law that times the heavens", [3.3, -1.7, 0],
                     size=22, color=DIM)
        self.play(FadeIn(read), run_time=1.0)
        self.wait(max(0.4, DUR - 8.0))
