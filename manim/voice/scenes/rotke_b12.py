from manim import *
import numpy as np
from rotke_helpers import (make_flywheel, axis_pin, mass_disk,
                           small_label)

# "Computing rotational kinetic energy from the moment of inertia and
#  the angular speed — that's yours."
DUR = 8.7


class RotkeS1B12(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        FC = np.array([-3.0, 0.4, 0])
        fw = make_flywheel(FC, radius=1.5)
        self.add(fw, axis_pin(FC, scale=1.0))
        fw.add_updater(lambda m, dt: m.rotate(-1.2 * dt, about_point=FC))

        # omega arc + symbol
        omega = MathTex(r"\omega", color="#F0C674").scale(1.3)
        omega.move_to(FC + np.array([0, 2.3, 0]))
        arc = Arc(radius=1.85, start_angle=PI * 0.18,
                  angle=PI * 0.55, color="#F0C674",
                  stroke_width=4).move_arc_center_to(FC)
        arc.add_tip(tip_length=0.18)
        self.play(Create(arc), FadeIn(omega), run_time=1.2)

        # mass-distribution sketch on the right
        disk = mass_disk(np.array([3.0, 0.4, 0]), radius=1.4,
                         at_rim=True)
        self.play(FadeIn(disk), run_time=1.0)
        self.add(small_label("mass distribution",
                             [3.0, -1.6, 0], size=22, color="#8C98A6"))

        # terms left open
        expr = small_label("rotational kinetic energy  =  ?",
                           [0, -3.0, 0], size=28, color="#EAE4D5")
        self.play(Write(expr), run_time=1.4)
        self.wait(DUR - 3.6)
        fw.clear_updaters()
