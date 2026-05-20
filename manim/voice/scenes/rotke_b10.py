from manim import *
import numpy as np
from rotke_helpers import (make_flywheel, axis_pin, make_potters_wheel,
                           energy_bar, small_label)

# "It's why a flywheel can store energy, and a potter's wheel keeps
#  turning long after the last push."
DUR = 8.6


class RotkeS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        FC = np.array([-3.4, 0.6, 0])
        fw = make_flywheel(FC, radius=1.5)
        self.add(fw, axis_pin(FC, scale=1.0))
        fw.add_updater(lambda m, dt: m.rotate(-1.5 * dt, about_point=FC))
        self.add(small_label("flywheel — stores energy",
                             FC + np.array([0, -2.2, 0]), size=22,
                             color="#8C98A6"))

        # energy fed out smoothly: a steady bar that holds
        base = np.array([-3.4, -3.1, 0])
        bar = energy_bar(0.02, base, width=0.5)
        self.add(bar)
        self.play(Transform(bar, energy_bar(1.6, base, width=0.5)),
                  run_time=1.4)

        PC = np.array([3.2, 0.2, 0])
        pw = make_potters_wheel(PC, scale=1.15)
        self.play(FadeIn(pw), run_time=1.0)
        self.add(small_label("potter's wheel — coasts on",
                             PC + np.array([0, -1.6, 0]), size=22,
                             color="#8C98A6"))
        # spin shown by a marker orbiting the flat plate (foreshortened),
        # decelerating slowly after one push
        marker = Dot(radius=0.10, color="#FFD27A")
        ang = [0.0]
        spin = [2.0]
        rx, ry = 1.05 * 1.15, 0.36 * 1.15

        def orbit(m, dt):
            ang[0] -= spin[0] * dt
            m.move_to(PC + np.array([rx * np.cos(ang[0]),
                                     ry * np.sin(ang[0]) + 0.40, 0]))
        marker.add_updater(orbit)
        self.add(marker)
        self.wait(1.0)
        spin[0] = 1.3
        self.wait(1.0)
        spin[0] = 0.85
        self.wait(DUR - 5.4)
        fw.clear_updaters()
        marker.clear_updaters()
