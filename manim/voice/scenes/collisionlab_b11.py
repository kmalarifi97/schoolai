from manim import *
import numpy as np
from collisionlab_helpers import momentum_bar, energy_bar, small_label

# "Two rules. One that never changes. One that's allowed to. Together
#  they pin down what really happened."
DUR = 8.8


class CollisionlabS1B11(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        # rule 1: momentum — fixed length
        mom = momentum_bar([-3.0, 0.4, 0], length=3.4, split=0.5,
                           label=None)
        m_lab = small_label("momentum", [-3.0, -0.6, 0],
                            color="#8C8576", size=20)
        m_tag = small_label("always", [-3.0, 1.4, 0], color="#7FB8E8",
                            size=24)
        self.play(FadeIn(mom), FadeIn(m_lab), run_time=1.2)
        self.play(FadeIn(m_tag), run_time=0.8)

        # rule 2: motion energy — allowed to drop
        en = energy_bar("motion energy", 0.85, [2.6, -0.1, 0],
                        color="#E8C46B", max_h=2.4)
        e_tag = small_label("sometimes", [2.6, 1.4, 0],
                            color="#D98C5F", size=24)
        self.play(FadeIn(en), run_time=1.2)
        self.play(FadeIn(e_tag), run_time=0.8)

        cap = small_label("together — what really happened",
                          [0, -2.3, 0], color="#EAE4D5", size=22)
        self.play(FadeIn(cap), run_time=1.2)
        self.wait(DUR - 6.2)
