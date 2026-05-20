from manim import *
import numpy as np
from tempvsthermal_helpers import (particle_swarm, make_thermometer,
                                   small_label)

# "Temperature measures how violently each particle jiggles, on
#  average. Just the average. Per particle."
DUR = 8.8


class TempvsthermalS1B6(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        swarm = particle_swarm([-2.4, 0.0, 0], n=16, radius=1.7,
                               hot=False, seed=6, dot_r=0.10)
        self.add(swarm)
        therm = make_thermometer([3.4, -0.1, 0], scale=0.95,
                                 fill_frac=0.04)
        self.play(FadeIn(therm), run_time=0.8)

        # highlight one particle
        hi = swarm[7]
        ringmark = Circle(radius=0.26, color="#FFD27A", stroke_width=3
                          ).move_to(hi.get_center())
        self.play(hi.animate.set_color("#FFD27A"), Create(ringmark),
                  run_time=1.0)
        link = DashedLine(hi.get_center(), therm.get_center(),
                          color="#5A6E80", stroke_width=2).set_opacity(0.6)
        self.play(Create(link), run_time=0.8)

        # its amplitude rises -> thermometer rises
        home = hi.get_center().copy()
        therm_hi = make_thermometer([3.4, -0.1, 0], scale=0.95,
                                    fill_frac=0.65)
        self.play(
            Succession(
                hi.animate.move_to(home + RIGHT * 0.30),
                hi.animate.move_to(home + LEFT * 0.30),
                hi.animate.move_to(home),
            ),
            Transform(therm, therm_hi),
            ringmark.animate.move_to(home),
            run_time=1.8,
        )
        self.add(small_label("temperature = average jiggle", [0, 3.3, 0],
                             size=24, color="#FFD27A"))
        self.wait(DUR - 5.2)
