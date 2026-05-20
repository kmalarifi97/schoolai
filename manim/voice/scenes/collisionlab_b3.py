from manim import *
import numpy as np
from collisionlab_helpers import make_cart, clue_dent, small_label, qmark

# "She looks at the dent. The bigger dent must mean the harder hit.
#  Right?"
DUR = 6.6


class CollisionlabS1B3(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # close on the dented cart
        c2 = make_cart([-1.2, 0.0, 0], scale=1.7, color="#E8C46B",
                       dented=True, facing=1)
        self.play(FadeIn(c2), run_time=1.0)

        # zoom focus ring on the dent
        ring = Circle(radius=0.7, color="#C98A6B", stroke_width=2.5
                      ).move_to([0.05, 0.0, 0]).set_opacity(0.0)
        self.play(ring.animate.set_opacity(0.7).scale(0.8),
                  run_time=1.0)

        guess = small_label("bigger dent = harder hit", [1.9, 1.0, 0],
                            color="#EAE4D5", size=22)
        q = qmark([1.9, 0.1, 0], size=40)
        self.play(FadeIn(guess), run_time=1.2)
        self.play(FadeIn(q, scale=1.2), run_time=0.8)
        self.wait(DUR - 4.0)
