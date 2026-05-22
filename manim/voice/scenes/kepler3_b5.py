from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from kepler3_helpers import (make_sun, make_planet, orbit_ring, make_clock,
                             clock_wedge, clock_hand, divider, label,
                             NEUTRAL, DIM, RED, CHALK)

# "Then the time it takes to go all the way around, once. Call it T — the
#  planet's year."
DUR = 7.6

LC = np.array([-3.5, 0.6, 0])


class Kepler3S1B5(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        sun = make_sun(LC, scale=0.55)
        self.add(sun)

        r0 = 1.6
        ring = orbit_ring(LC, r=r0)
        self.add(ring)
        ang0 = PI / 2
        planet = make_planet(
            LC + np.array([r0 * np.cos(ang0), r0 * np.sin(ang0), 0]),
            r=0.15, color=NEUTRAL)
        self.add(planet)

        clk = make_clock([-3.5, -2.5, 0], r=0.55)
        self.add(clk)
        Tlabel = label("T", [-2.6, -2.5, 0], size=30, color=RED)
        T_sym = MathTex("T", color=RED).scale(1.3).move_to([3.3, 0.2, 0])
        self.play(FadeIn(Tlabel), FadeIn(T_sym, scale=0.7), run_time=0.8)

        # One loop while the clock fills; loop-arc + T glow red together.
        prog = ValueTracker(0.0)
        wedge = always_redraw(
            lambda: clock_wedge(clk, prog.get_value(), color=RED))
        hand = always_redraw(
            lambda: clock_hand(clk, prog.get_value()))
        self.add(wedge, hand)
        # the orbit-arc traced so far, in red
        arc = always_redraw(lambda: self._arc(LC, r0, ang0, prog.get_value()))
        self.add(arc)
        planet.add_updater(lambda m: m.move_to(
            LC + np.array([r0 * np.cos(ang0 - 2 * np.pi * prog.get_value()),
                           r0 * np.sin(ang0 - 2 * np.pi * prog.get_value()),
                           0])))
        self.play(prog.animate.set_value(1.0), run_time=DUR - 2.4,
                  rate_func=linear)
        planet.clear_updaters()
        self.wait(0.3)

    @staticmethod
    def _arc(center, r, start, frac):
        if frac <= 0.0:
            return VMobject()
        pts = []
        n = max(2, int(80 * frac))
        for i in range(n + 1):
            ang = start - 2 * np.pi * frac * (i / n)
            pts.append(center + np.array([r * np.cos(ang),
                                          r * np.sin(ang), 0]))
        m = VMobject().set_points_smoothly(pts)
        m.set_stroke(RED, width=4)
        return m
