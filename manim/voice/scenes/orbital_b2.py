from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             make_clock, clock_wedge, clock_hand, divider,
                             label, qmark, PLANET, PLANET_D, FAINT, DIM,
                             CHALK)

# "A planet circles the sun, year after year — never falling in, never
#  flying off. What sets the length of its year?"
DUR = 9.6

LC = np.array([-3.5, 0.6, 0])


class OrbitalS1B2(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.55))

        r0 = 1.7
        ring = orbit_ring(LC, r=r0)
        planet = make_planet(planet_at(LC, r0, 0.0), color=PLANET,
                             edge=PLANET_D)
        self.add(ring, planet)

        clk = make_clock([-3.5, -2.5, 0], r=0.55)
        self.add(clk)

        # RIGHT: blank period-equation frame with a '?'.
        frame = RoundedRectangle(width=4.6, height=2.2, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.4, 0])
        f_eq = MathTex(r"T", r"=", r"?", color=CHALK).scale(1.5
                       ).move_to([3.3, 0.4, 0])
        f_eq[2].set_color(DIM)
        self.play(Create(frame), Write(f_eq[0]), Write(f_eq[1]), run_time=1.0)
        self.play(FadeIn(f_eq[2], scale=1.3), run_time=0.7)

        # Planet loops; clock fills in step; '?' over it.
        prog = ValueTracker(0.0)
        planet.add_updater(lambda m: m.move_to(
            planet_at(LC, r0, prog.get_value())))
        wedge = always_redraw(
            lambda: clock_wedge(clk, prog.get_value(), color=PLANET))
        hand = always_redraw(lambda: clock_hand(clk, prog.get_value()))
        self.add(wedge, hand)
        q = qmark([-3.5, -1.3, 0], size=44)
        self.play(FadeIn(q), run_time=0.6)
        self.play(prog.animate.set_value(1.0),
                  run_time=max(1.0, DUR - 2.9), rate_func=linear)
        planet.clear_updaters()
        self.wait(0.3)
