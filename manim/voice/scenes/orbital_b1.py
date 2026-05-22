from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             divider, label, PLANET, PLANET_D, FAINT, DIM,
                             CHALK)

# "Newton gave you the force. Kepler gave you a pattern in the planets.
#  Watch them meet."
DUR = 7.6

LC = np.array([-3.5, 0.2, 0])


class OrbitalS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())

        sun = make_sun(LC, scale=0.6)
        self.play(FadeIn(sun, scale=0.8), run_time=0.8)
        r0 = 1.9
        ring = orbit_ring(LC, r=r0)
        self.play(Create(ring), run_time=1.0)
        planet = make_planet(planet_at(LC, r0, 0.0), color=PLANET,
                             edge=PLANET_D)
        self.add(planet)

        # Faint ghosts of the two laws that are about to meet.
        ghostN = MathTex(r"F = G\frac{m_1 m_2}{r^2}",
                         color=DIM).scale(0.7).move_to([3.3, 2.6, 0])
        ghostK = MathTex(r"T^2 \propto r^3",
                         color=DIM).scale(0.7).move_to([3.3, -2.6, 0])
        for g in (ghostN, ghostK):
            g.set_opacity(0.45)
        frame = RoundedRectangle(width=4.6, height=2.4, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.2, 0])
        self.play(FadeIn(ghostN), FadeIn(ghostK), Create(frame),
                  run_time=1.2)

        # Planet loops while the ghosts hover.
        prog = ValueTracker(0.0)
        planet.add_updater(lambda m: m.move_to(
            planet_at(LC, r0, prog.get_value())))
        self.play(prog.animate.set_value(1.0),
                  run_time=max(1.0, DUR - 3.4), rate_func=linear)
        planet.clear_updaters()
        self.wait(0.3)
