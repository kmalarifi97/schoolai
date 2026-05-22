from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d, make_sun as grav_sun
from orbital_helpers import (make_planet, make_equation_full, label,
                             PLANET, PLANET_D, DIM, RED, CHALK)

# "And look — this IS Kepler's third law. What he found by staring at data,
#  Newton's gravity now explains. Same bend, same rule — measured once,
#  derived now."
DUR = 12.6


class OrbitalS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The gravity bend underneath, on the LEFT.
        fabric = make_fabric_3d(dip_amount=1.0).shift(LEFT * 3.2)
        self.play(Create(fabric), run_time=2.0, lag_ratio=0.02)
        sun = grav_sun().scale(0.55).move_to([-3.2, -0.7, 0])
        self.add(sun)
        center = np.array([-3.2, -0.7, 0])
        near = make_planet(center + np.array([1.0, 0.15, 0]), r=0.13,
                           color=PLANET, edge=PLANET_D)
        far = make_planet(center + np.array([-2.4, 0.4, 0]), r=0.15,
                          color="#9BD6B0", edge=DIM)
        self.play(FadeIn(near), FadeIn(far), run_time=0.8)

        # Our period equation, top-right; morph to T^2 ∝ r^3.
        eq = make_equation_full([3.3, 2.2, 0], scale=0.85)
        eq.set_color(CHALK)
        self.add(eq)
        self.wait(0.4)
        kep = MathTex(r"T^2", r"\propto", r"r^3", color=CHALK
                      ).scale(1.3).move_to([3.3, 0.6, 0])
        kep[0].set_color(RED); kep[2].set_color(RED)
        self.play(TransformFromCopy(eq, kep), run_time=1.6)

        # Kepler3's own ratio law ghosts in, in agreement.
        ghost = MathTex(r"\left(\frac{r_A}{r_B}\right)^3 = "
                        r"\left(\frac{T_A}{T_B}\right)^2",
                        color=DIM).scale(0.8).move_to([3.3, -1.0, 0])
        ghost.set_opacity(0.6)
        self.play(FadeIn(ghost, shift=UP * 0.2), run_time=1.2)
        agree = label("Kepler's third law — in agreement", [3.3, -2.2, 0],
                      size=20, color=DIM)
        self.play(FadeIn(agree), run_time=0.9)
        self.wait(max(0.3, DUR - 8.8))
