from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, radius_line,
                             make_clock, clock_wedge, clock_hand, divider,
                             label, make_equation, PLANET_A, PLANET_B,
                             RED, CHALK, DIM)

# "So what's it for? Know how far a planet is, and you can predict its
#  year — without ever timing it. Or measure its year, and pin down its
#  distance. One world tells you another — not its mass, not the shape of
#  its path, just how distance and time trade off."
DUR = 19.9

LC = np.array([-3.5, 0.6, 0])


class Kepler3S1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.5))

        r0 = 2.0
        ring = orbit_ring(LC, r=r0)
        planet = make_planet(LC + np.array([0, r0, 0]), r=0.16, color=CHALK,
                             edge=DIM)
        self.add(ring, planet)

        # Known r filled in for the target planet.
        rline = radius_line(LC, PI / 2, r0, color=RED, width=4)
        rval = label("r known", LC + np.array([0.95, r0 / 2, 0]),
                     size=22, color=RED)
        self.play(Create(rline), FadeIn(rval), run_time=1.2)

        # Equation; an arrow runs through it; solved-for T term highlights.
        eq = make_equation([3.3, 1.0, 0], scale=1.0)
        eq.set_color(CHALK)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        self.add(eq)
        arrow = Arrow(eq.lhs.get_left() + LEFT * 0.3,
                      eq.rhs.get_right() + RIGHT * 0.3,
                      color=RED, stroke_width=4, buff=0.0,
                      max_tip_length_to_length_ratio=0.06).shift(DOWN * 1.0)
        self.play(GrowArrow(arrow), run_time=1.4)
        self.play(VGroup(eq.lp_r, eq.tfrac, eq.rp_r, eq.square)
                  .animate.set_color(RED), run_time=0.8)
        for tx, c in [("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)

        # T appears on a clock (the predicted year).
        clk = make_clock([3.3, -1.7, 0], r=0.6)
        self.add(clk)
        self.add(clock_wedge(clk, 0.55, color=RED))
        self.add(clock_hand(clk, 0.55))
        tnote = label("predicted T", [4.7, -1.7, 0], size=20, color=RED)
        self.play(FadeIn(clk), FadeIn(tnote), run_time=1.0)
        self.wait(1.0)

        # Struck-through tags: not mass, not path shape.
        def struck(text, pos):
            t = label(text, pos, size=22, color=DIM)
            ln = Line(t.get_left(), t.get_right(), color=RED,
                      stroke_width=3)
            return VGroup(t, ln)
        m = struck("mass", LC + np.array([0.2, -2.4, 0]))
        ps = struck("path shape", LC + np.array([0.3, -3.0, 0]))
        self.play(FadeIn(m), run_time=0.8)
        self.play(FadeIn(ps), run_time=0.8)
        self.wait(max(0.3, DUR - 9.0))
