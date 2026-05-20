from manim import *
import numpy as np
from collisionlab_helpers import (cl_track, cl_puck, momentum_arrow,
                                  ke_readout, play_button)

# "Then she presses play. And she watches the arrows and the energy
#  number — not the carts."
DUR = 7.8


class CollisionlabS1B16(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        tr = cl_track([0, 0.4, 0], w=7.2)
        p1 = cl_puck([-2.6, 0.4, 0], color="#7FB8E8", mass="2")
        p2 = cl_puck([1.4, 0.4, 0], color="#E8C46B", mass="1")
        a1 = momentum_arrow([-2.6, 0.4, 0], 1.0, color="#E8C46B")
        ke = ke_readout([0, 2.2, 0], value="KE = 1.00 J", scale=0.75)
        self.add(tr, p1, p2, a1, ke)

        pb = play_button([0, -2.2, 0], r=0.42)
        self.play(FadeIn(pb), run_time=0.6)
        self.play(pb.animate.scale(0.85).set_opacity(0.4),
                  run_time=0.4)

        # pucks collide; camera holds on arrows + KE value
        self.play(p1.animate.move_to([-0.4, 0.4, 0]),
                  a1.animate.shift(RIGHT * 2.2),
                  run_time=1.4, rate_func=rate_functions.ease_in_sine)
        flash = Dot([0.5, 0.4, 0], radius=0.05, color="#EAE4D5")
        new_ke = ke_readout([0, 2.2, 0], value="KE = 0.41 J",
                            scale=0.75)
        a1b = momentum_arrow([-1.0, 0.4, 0], -0.4, color="#7FB8E8")
        a2b = momentum_arrow([1.0, 0.4, 0], 0.8, color="#E8C46B")
        self.play(
            flash.animate.scale(8).set_opacity(0.0),
            p2.animate.move_to([1.9, 0.4, 0]),
            FadeOut(a1), GrowArrow(a1b), GrowArrow(a2b),
            Transform(ke, new_ke), run_time=1.4)
        self.wait(DUR - 4.2)
