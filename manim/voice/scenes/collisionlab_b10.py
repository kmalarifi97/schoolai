from manim import *
import numpy as np
from collisionlab_helpers import energy_bar, loss_shimmer, small_label

# "And the energy of motion? That can drop — into the dent, the sound,
#  the heat. How much it drops tells her what kind of collision this
#  was."
DUR = 11.4


class CollisionlabS1B10(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        full = energy_bar("motion energy", 0.92, [-3.6, -0.1, 0],
                          color="#E8C46B", max_h=3.0)
        self.play(FadeIn(full), run_time=1.2)
        self.wait(0.6)

        # the impact: the bar drops
        dropped = energy_bar("motion energy", 0.52, [-3.6, -0.1, 0],
                             color="#E8C46B", max_h=3.0)
        flash = Dot([-3.6, 0.6, 0], radius=0.05, color="#EAE4D5")
        self.play(Transform(full, dropped),
                  flash.animate.scale(7).set_opacity(0.0),
                  run_time=1.6)

        # the lost part leaves as dent + sound + heat shimmer
        arr = Arrow([-2.0, 0.4, 0], [-0.4, 0.4, 0], color="#8C8576",
                    stroke_width=3, buff=0.1,
                    max_tip_length_to_length_ratio=0.2)
        shim = loss_shimmer([1.6, 0.4, 0], scale=1.0)
        shim.set_opacity(0.0)
        self.play(GrowArrow(arr), run_time=1.0)
        self.play(shim.animate.set_opacity(0.85), run_time=1.4)
        cap = small_label("how much it drops = what kind of collision",
                          [0, -2.3, 0], color="#EAE4D5", size=22)
        self.play(FadeIn(cap), run_time=1.2)
        self.wait(DUR - 7.0)
