from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d
from newton_helpers import (make_mass, divider, label, MASS1, MASS1_D,
                            MASS2, MASS2_D, FAINT, DIM)

# "In the teaser, you felt why two masses pull together — space bends, and
#  they roll in. But how HARD do they pull? A pebble and a planet — surely
#  not the same."
DUR = 12.8


class NewtonS1B1(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Resume the teaser's curved-space bend; two masses roll in.
        fabric = make_fabric_3d(dip_amount=1.0)
        self.play(Create(fabric), run_time=2.2, lag_ratio=0.02)

        center = np.array([0, -0.35, 0])
        m1 = make_mass(center + np.array([-3.0, 1.4, 0]), r=0.42,
                       color=MASS1, edge=MASS1_D)
        m2 = make_mass(center + np.array([3.0, 1.0, 0]), r=0.26,
                       color=MASS2, edge=MASS2_D)
        self.play(FadeIn(m1, scale=0.7), FadeIn(m2, scale=0.7), run_time=0.9)

        # Roll them down the bend toward the center.
        self.play(
            m1.animate.move_to(center + np.array([-0.7, 0.15, 0])),
            m2.animate.move_to(center + np.array([0.7, 0.05, 0])),
            run_time=2.4, rate_func=rate_functions.ease_in_sine)
        self.wait(0.5)

        # Split-frame: slide the world LEFT, reveal divider + blank
        # force-equation frame on the RIGHT.
        world = VGroup(fabric, m1, m2)
        self.play(world.animate.shift(LEFT * 3.0).scale(0.85),
                  run_time=1.5)
        self.play(Create(divider()), run_time=0.7)

        frame = RoundedRectangle(width=4.6, height=2.4, corner_radius=0.18,
                                 stroke_color=FAINT, stroke_width=2,
                                 fill_opacity=0).move_to([3.3, 0.4, 0])
        self.play(Create(frame), run_time=1.0)
        cap = label("the force, soon", [3.3, -1.2, 0], size=22,
                    color=DIM, opacity=0.85)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(max(0.3, DUR - 12.0))
