from manim import *
import numpy as np
from collisionlab_helpers import (cl_track, cl_puck, momentum_arrow,
                                  ke_readout, mass_slider, small_label)

# "Collision Lab. She sets the two masses. Turns on the momentum arrows
#  and the kinetic-energy number."
DUR = 8.6


class CollisionlabS1B13(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        title = small_label("Collision Lab", [0, 3.0, 0],
                            color="#8C8576", size=24)
        tr = cl_track([0, 0.2, 0], w=7.4)
        p1 = cl_puck([-2.4, 0.2, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([2.0, 0.2, 0], color="#E8C46B", mass="1")
        self.play(FadeIn(title), FadeIn(tr), run_time=1.0)
        self.play(FadeIn(p1), FadeIn(p2), run_time=1.0)

        # set the masses via a slider
        ms = mass_slider([-3.4, -2.4, 0], frac=0.3, w=2.0,
                         label="mass")
        self.play(FadeIn(ms), run_time=0.8)
        self.play(ms.knob.animate.move_to(
            ms.rail.get_left() + RIGHT * 2.0 * 0.65), run_time=1.0)

        # turn on momentum arrows + KE number
        a1 = momentum_arrow([-2.4, 0.2, 0], 1.0, color="#E8C46B")
        a2 = momentum_arrow([2.0, 0.2, 0], -0.7, color="#7FB8E8")
        ke = ke_readout([2.6, -2.2, 0], scale=0.75)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=1.0)
        self.play(FadeIn(ke), run_time=1.0)
        self.wait(DUR - 5.8)
