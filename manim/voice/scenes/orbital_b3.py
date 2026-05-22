from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from orbital_helpers import (make_sun, make_planet, orbit_ring, planet_at,
                             divider, label, PLANET, PLANET_D, FAINT, DIM,
                             RED, CHALK)

# "Gravity is the leash. The inward pull is exactly the force needed to
#  bend a straight path into a circle. Set those two equal, and the year
#  falls out."
DUR = 12.2

LC = np.array([-3.5, 0.2, 0])


class OrbitalS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.add(divider())
        self.add(make_sun(LC, scale=0.55))

        r0 = 1.9
        ring = orbit_ring(LC, r=r0)
        ppos = planet_at(LC, r0, 0.0)   # at 12 o'clock
        planet = make_planet(ppos, color=PLANET, edge=PLANET_D)
        self.add(ring, planet)

        # Inward gravity arrow (planet -> sun).
        grav = Arrow(ppos, ppos + (LC - ppos) * 0.45, color=RED,
                     stroke_width=6, buff=0.0,
                     max_tip_length_to_length_ratio=0.3)
        grav_lbl = label("gravity, inward", ppos + np.array([1.6, -0.3, 0]),
                         size=20, color=RED)
        self.play(GrowArrow(grav), FadeIn(grav_lbl), run_time=1.2)

        # The "turning" centripetal need — same direction, inward.
        cent = Arrow(ppos + RIGHT * 0.05, ppos + (LC - ppos) * 0.45 + RIGHT * 0.05,
                     color="#7FB3E0", stroke_width=6, buff=0.0,
                     max_tip_length_to_length_ratio=0.3)
        cent_lbl = label("the turn a circle needs",
                         ppos + np.array([1.9, 0.4, 0]), size=20,
                         color="#7FB3E0")
        self.play(GrowArrow(cent), FadeIn(cent_lbl), run_time=1.2)
        self.wait(0.4)

        # They overlap and snap to an equals sign on the RIGHT.
        balance = MathTex(r"F_{\text{grav}}", r"=", r"F_{\text{turn}}",
                          color=CHALK).scale(1.0).move_to([3.3, 0.6, 0])
        balance[0].set_color(RED)
        balance[2].set_color("#7FB3E0")
        self.play(
            cent.animate.set_color(RED),
            Transform(cent_lbl.copy(), balance[2]),
            FadeIn(balance[0]), FadeIn(balance[1]), FadeIn(balance[2]),
            run_time=1.4)
        self.play(Flash(balance[1].get_center(), color=RED, line_length=0.2),
                  run_time=0.6)
        note = label("set them equal -> the year", [3.3, -0.6, 0],
                     size=22, color=DIM)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(max(0.3, DUR - 7.6))
