from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d, make_sun as grav_sun
from kepler3_helpers import (make_planet, make_equation, label,
                             PLANET_A, PLANET_B, RED, CHALK, DIM)

# "Remember the bend. The farther out a planet sits, the gentler the
#  slope, the slower it rolls. This equation is that bend — written in
#  numbers."
DUR = 11.7


class Kepler3S1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The teaser's bend, on the LEFT.
        fabric = make_fabric_3d(dip_amount=1.0).shift(LEFT * 3.2)
        self.play(Create(fabric), run_time=2.0, lag_ratio=0.02)
        sun = grav_sun().scale(0.6).move_to([-3.2 + 0, -0.7, 0])
        self.add(sun)

        center = np.array([-3.2, -0.7, 0])
        # A near planet on a steep (inner) slope, a far one on a gentle one.
        near_r, far_r = 1.0, 2.6
        near = make_planet(center + np.array([near_r, 0.15, 0]), r=0.14,
                           color=PLANET_B, edge=DIM)
        far = make_planet(center + np.array([-far_r, 0.4, 0]), r=0.16,
                          color=PLANET_A, edge=DIM)
        self.play(FadeIn(near), FadeIn(far), run_time=0.8)

        # The equation slides over from the right onto the bend.
        eq = make_equation([3.3, 1.6, 0], scale=0.95)
        eq.set_color(CHALK)
        for tx, c in [("r_A", PLANET_A), ("r_B", PLANET_B),
                      ("T_A", PLANET_A), ("T_B", PLANET_B)]:
            eq.get_part_by_tex(tx)[-1].set_color(c)
        self.add(eq)
        self.play(eq.animate.scale(0.85).move_to([-2.0, 2.4, 0]),
                  run_time=1.4)

        # near whips around steep; far rolls slowly down gentle.
        progN = ValueTracker(0.0)
        progF = ValueTracker(0.0)
        near.add_updater(lambda m: m.move_to(center + np.array([
            near_r * np.cos(-2 * np.pi * progN.get_value()),
            0.15 + near_r * 0.30 * np.sin(-2 * np.pi * progN.get_value()),
            0])))
        far.add_updater(lambda m: m.move_to(center + np.array([
            -far_r * np.cos(2 * np.pi * progF.get_value()),
            0.4 + far_r * 0.30 * np.sin(2 * np.pi * progF.get_value()),
            0])))
        self.play(progN.animate.set_value(3.0),
                  progF.animate.set_value(1.0),
                  run_time=max(1.0, DUR - 5.5), rate_func=linear)
        near.clear_updaters(); far.clear_updaters()
        self.wait(0.3)
