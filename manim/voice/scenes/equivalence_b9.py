from manim import *
import numpy as np
from equivalence_helpers import side_panel, big_text, small_label, INK

# "Not a coincidence, said Einstein. A clue."
DUR = 4.5


class EquivalenceS1B9(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        panel = side_panel([0, 0, 0], w=8.0, h=5.0, title="Einstein")
        self.play(Create(panel[0]), FadeIn(panel[1]), run_time=1.0)
        eqn = MathTex(r"m_i \;=\; m_g", color=INK).scale(1.4
                     ).move_to([0, 0.3, 0])
        self.play(Write(eqn), run_time=1.0)
        # the cancellation glows as if meaningful
        glow = eqn.copy().set_color("#FFE08A")
        self.play(Transform(eqn, glow), run_time=0.6,
                  rate_func=rate_functions.there_and_back)
        self.play(Flash(eqn, color="#FFE08A", line_length=0.3,
                        num_lines=14, flash_radius=1.0), run_time=0.7)
        cap = small_label("a clue", [0, -1.1, 0],
                          color="#FFE08A", size=24)
        self.play(FadeIn(cap), run_time=0.6)
        self.wait(DUR - 3.9)
