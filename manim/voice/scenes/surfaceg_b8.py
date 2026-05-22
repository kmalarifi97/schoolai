from manim import *
import numpy as np
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from grav_helpers import make_fabric_3d
from surfaceg_helpers import (make_person, divider, label,
                              make_equation_reduced, CHALK, DIM, RED)

# "It's the same bend. A heavier world digs a deeper well — and g is how
#  steep that well is right at the surface."
DUR = 11.2


class SurfacegS1B8(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # The curved-space bend, on the LEFT (callback to the gravity series).
        dip = ValueTracker(0.8)
        fabric = always_redraw(
            lambda: make_fabric_3d(dip_amount=dip.get_value()
                                   ).shift(LEFT * 3.2))
        self.play(Create(make_fabric_3d(dip_amount=0.8).shift(LEFT * 3.2)),
                  run_time=2.0, lag_ratio=0.02)
        self.add(fabric)

        # A person standing on the slope at the surface.
        center = np.array([-3.2, -0.35, 0])
        person = make_person(scale=0.6)
        person.move_to(center + np.array([1.3, 0.05, 0]))
        self.add(person)
        person.add_updater(lambda m: m.move_to(
            center + np.array([1.3, 0.05 - 0.55 * (dip.get_value() - 0.8), 0])))

        # RIGHT: the equation; g highlighted as the slope's steepness.
        eq = make_equation_reduced([3.3, 1.8, 0], scale=1.0)
        eq.get_part_by_tex("m_E").set_color(RED)
        eq.get_part_by_tex("r_E").set_color(RED)
        self.add(eq)

        g_bar = label("g = steepness at the surface", [3.3, 0.6, 0],
                      size=22, color=DIM)
        self.play(FadeIn(g_bar), run_time=1.0)

        # A heavier world -> deeper well -> larger g.
        gval = always_redraw(lambda: MathTex(
            r"g = " + f"{9.8 * dip.get_value() / 0.8:.1f}",
            color=RED).scale(1.1).move_to([3.3, -0.6, 0]))
        self.add(gval)
        heavier = label("heavier world", [3.3, -1.6, 0], size=22, color=RED)
        deeper = label("deeper well, steeper slope", [3.3, -2.3, 0],
                       size=20, color=DIM)
        self.play(FadeIn(heavier), run_time=0.6)
        self.play(dip.animate.set_value(1.6), FadeIn(deeper),
                  run_time=2.6, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.6)
        person.clear_updaters()
        self.wait(max(0.3, DUR - 8.4))
